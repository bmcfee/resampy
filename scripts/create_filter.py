#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Construct resampy filters by Bayesian parameter search"""

import sys
import functools

from argparse import ArgumentParser

import numpy as np
import scipy
import scipy.signal

import optuna

import resampy


def parse_arguments(args):

    parser = ArgumentParser(description=__doc__)

    parser.add_argument(
        "-n",
        "--num-trials",
        dest="n_trials",
        default=1500,
        help="Number of trials",
        type=int,
    )

    parser.add_argument(
        "-z",
        "--num-zeros",
        dest="num_zeros",
        required=True,
        type=int,
        help="Number of zero-crossings",
    )

    parser.add_argument(
        "--min-rolloff",
        dest="min_rolloff",
        default=0.9,
        help="Minimum rolloff frequency (fraction of Nyquist)",
        type=float,
    )

    parser.add_argument(
        "-p",
        "--precision",
        dest="precision",
        default=13,
        help="Precision for filter interpolation",
        type=int,
    )

    parser.add_argument(
        "--min-beta",
        dest="min_beta",
        default=8,
        help="Minimum beta for kaiser filter",
        type=float,
    )

    parser.add_argument(
        "--max-beta",
        dest="max_beta",
        default=20,
        help="Maximum beta for kaiser filter",
        type=float,
    )

    parser.add_argument(
        "--attenuation",
        dest="attenuation",
        default=-120,
        help="Stop-band attenuation",
        type=float,
    )
    parser.add_argument(dest="output_file", type=str, help="Path to store filter")

    return parser.parse_args(args)


def get_window(beta=None, rolloff=None, num_zeros=None):
    """Build the full window from a specification"""
    win = functools.partial(scipy.signal.windows.kaiser, beta=beta)
    fil = resampy.filters.sinc_window(
        num_zeros=num_zeros, precision=1, window=win, rolloff=rolloff
    )[0]

    # The windowed filter
    fil = np.concatenate([fil[-1:0:-1], fil])

    return fil


def _objective(beta, rolloff, attenuation=-120, num_zeros=40):
    """Internal objective function:

    Minimize the mean passband-deviation from unity gain +
    maximum stop-band gain above target attenuation
    """
    fil = get_window(beta, rolloff, num_zeros=num_zeros)

    W, H = scipy.signal.freqz(fil, worN=2048)

    H = np.abs(H)
    H_pass = H[W < 0.5 * np.pi]
    H_stop = H[W >= 0.5 * np.pi]

    err_pass = 20 * np.mean(np.abs(np.log10(H_pass)))
    err_stop = np.max(
        np.abs(np.maximum(20 * np.log10(H_stop), attenuation) - attenuation)
    )
    return err_pass + err_stop


def objective(trial, num_zeros, min_beta, max_beta, min_rolloff, attenuation):
    """Objective wrapper for the optimizer"""

    beta = trial.suggest_float("beta", min_beta, max_beta)
    rolloff = trial.suggest_float("rolloff", min_rolloff, 1.0)

    loss = _objective(beta, rolloff, num_zeros=num_zeros, attenuation=attenuation)

    return loss


if __name__ == "__main__":
    params = parse_arguments(sys.argv[1:])

    optuna.logging.set_verbosity(optuna.logging.WARNING)

    sampler = optuna.samplers.TPESampler(seed=20220629)
    study = optuna.create_study(direction="minimize", sampler=sampler)

    func = functools.partial(
        objective,
        num_zeros=params.num_zeros,
        min_beta=params.min_beta,
        max_beta=params.max_beta,
        min_rolloff=params.min_rolloff,
        attenuation=params.attenuation,
    )

    study.optimize(func, n_trials=params.n_trials, show_progress_bar=True)

    print(f"Parameters for {params.output_file}:")
    print("-" * 40)
    print(f"\tbeta        = {study.best_params['beta']:g}")
    print(f"\troll        = {study.best_params['rolloff']:g}")
    print(f"\t# zeros     = {params.num_zeros}")
    print(f"\tprecision   = {params.precision}")
    print(f"\tattenuation = {params.attenuation}")
    print("-" * 40)
    print(f"Objective value: {study.best_value:g}")

    window = functools.partial(scipy.signal.windows.kaiser, beta=study.best_params["beta"])
    half_win, precision, roll = resampy.filters.sinc_window(
        num_zeros=params.num_zeros,
        precision=params.precision,
        window=window,
        rolloff=study.best_params["rolloff"],
    )

    np.savez(
        params.output_file, half_window=half_win, precision=precision, rolloff=roll
    )

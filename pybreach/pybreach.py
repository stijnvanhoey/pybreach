# -*- coding: utf-8 -*-


import numpy as np


def left_reach(perf_meas, i, pct_beh):
    """calculate the left reach
    For all model realisations, given a data evaluation point index, get the
    left reach for all realisations and derive the maximum

    Parameters
    ----------
    perf_meas : 2-D numpy ndarray
        Input array of shape NxM with N the number of model realisations and M
        the number of model evaluation points (time steps, measured values)
    i : int
        the index of the array defining the current model evaluation point to
        calculate the left reach
    pct_beh : float [0-1]
        tolerance level, defining the percentage of points that do not comply
        in order to continue the reach calculation

    Returns
    -------
    overzichtl : numpy ndarray
        Nx5 output array with on the individual columns (1) the index,
        (2) a zero column used for internal calculation, (3) the number of
        failures, (4) the reach and (5) the span for each of the model
        realisations
    maxreachl : int
        maximum left reach of all model realisations
    """
    par_size, data_size = perf_meas.shape
    # prepare the left reach overview array
    overzichtl = np.array([np.arange(par_size),
                           np.ones(par_size),
                           np.zeros(par_size),
                           np.empty(par_size),
                           np.empty(par_size)]
                          ).transpose().astype(float)
    overzichtl[:, 3:5] = np.nan

    # derive for each par_set the length of the reach
    aantl = 0
    while (aantl <= i) & (sum(overzichtl[:, 1].astype(int)) != 0):
        overzichtl[(overzichtl[:, 1] == 1) &
                   (np.abs(perf_meas[:, i - aantl]) == 0), 2] = \
            overzichtl[(overzichtl[:, 1] == 1) &
                       (np.abs(perf_meas[:, i - aantl]) == 0),
                       2] + 1  # vwe 2x
        aantl += 1
        overzichtl[overzichtl[:, 2] > pct_beh / 100. * aantl, 1] = 0
        overzichtl[overzichtl[:, 1] == 1, 3] = aantl

    # correct the reach length on end-of-line zeros
    if all(np.isnan(overzichtl[:, 3])):
        maxreachl = i
    else:
        maxreachl = i - (np.nanmax(overzichtl[:, 3], axis=0)).astype(int) + 1
        while np.all(np.abs(perf_meas[i - overzichtl[:, 3].astype(
                int) + 1 == maxreachl, maxreachl]) == 0):  # vwe
            overzichtl[i - overzichtl[:, 3].astype(int) + 1 ==
                       maxreachl, 2:4] = \
                overzichtl[i - overzichtl[:, 3].astype(int) + 1 ==
                           maxreachl, 2:4] - 1
            maxreachl += 1

    overzichtl[~np.isnan(overzichtl[:, 3]), 4] = i - \
                                                 overzichtl[~np.isnan(
                                                     overzichtl[:, 3]), 3] + 1

    return overzichtl, maxreachl


def right_reach(perf_meas, i, pct_beh):
    """calculate the right reach
    For all model realisations, given a data evaluation point index, get the
    right reach for all realisations and derive the maximum

    Parameters
    ----------
    perf_meas : 2-D numpy ndarray
        Input array of shape NxM with N the number of model realisations and M
        the number of model evaluation points (time steps, measured values)
    i : int
        the index of the array defining the current model evaluation point to
        calculate the left reach
    pct_beh : float [0-1]
        tolerance level, defining the percentage of points that do not comply
        in order to continue the reach calculation

    Returns
    -------
    overzichtr : numpy ndarray
        Nx5 output array with on the individual columns (1) the index,
        (2) a zero column used for internal calculation, (3) the number of
        failures, (4) the reach and (5) the span for each of the model
        realisations
    maxreachr : int
        maximum right reach of all model realisations
    """
    par_size, data_size = perf_meas.shape
    # prepare the right reach overview array
    overzichtr = np.array([np.arange(par_size),
                           np.ones(par_size),
                           np.zeros(par_size),
                           np.empty(par_size),
                           np.empty(par_size)]
                          ).transpose().astype(float)
    overzichtr[:, 3:5] = np.nan

    # derive for each par_set the length of the reach
    aantr = 0
    while (i + aantr < data_size) & \
            (sum(overzichtr[:, 1].astype(int)) != 0):
        overzichtr[(overzichtr[:, 1] == 1) &
                   (np.abs(perf_meas[:, i + aantr]) == 0), 2] = \
            overzichtr[(overzichtr[:, 1] == 1) &
                       (np.abs(perf_meas[:, i + aantr]) == 0),
                       2] + 1  # vwe 2x
        aantr += 1
        overzichtr[overzichtr[:, 2] > pct_beh / 100. * aantr, 1] = 0
        overzichtr[overzichtr[:, 1] == 1, 3] = aantr

    # correct the reach length o end-of-line zeros
    if all(np.isnan(overzichtr[:, 3])):
        maxreachr = i
    else:
        maxreachr = i + (np.nanmax(overzichtr[:, 3], axis=0)).astype(int) - 1
        while np.all(np.abs(perf_meas[i + overzichtr[:, 3].astype(
                int) - 1 == maxreachr, maxreachr]) == 0):  # vwe
            overzichtr[i + overzichtr[:, 3].astype(int) - 1 ==
                       maxreachr, 2:4] = \
                overzichtr[i + overzichtr[:, 3].astype(int) - 1 ==
                           maxreachr, 2:4] - 1
            maxreachr -= 1

    overzichtr[~np.isnan(overzichtr[:, 3]), 4] = i + \
                                overzichtr[~np.isnan(overzichtr[:, 3]), 3] - 1

    return overzichtr, maxreachr


def breach_run(perf_meas, pcten): #, vwe
    """derive breach for a given performance matrix

    Parameters
    ----------
    perf_meas : 2-D numpy ndarray
        Input array of shape NxM with N the number of model realisations and M
        the number of model evaluation points (time steps, measured values)
    pcten: list
        list of tolerance levels, defining the percentage of points
        that are allowed to fail
    vwe: Not yet implemented!

    Returns
    -------
    breach : numpy ndarray
        For each of the tolerance levels, the left and right reach for each
        of the data points
    """

    breach = np.empty((perf_meas.shape[1], 2 * pcten.size), dtype=int)
    par_size, data_size = perf_meas.shape
    # par_maxreach

    for i in range(data_size):
        for j, pct_beh in enumerate(pcten):

            # ----- LEFT REACH ------
            overzichtl, maxreachl = left_reach(perf_meas, i, pct_beh)
            breach[i, 2 * j] = maxreachl

            # ----- RIGHT REACH ------
            overzichtr, maxreachr = right_reach(perf_meas, i, pct_beh)
            breach[i, 2 * j + 1] = maxreachr

    return breach  # par_maxreach
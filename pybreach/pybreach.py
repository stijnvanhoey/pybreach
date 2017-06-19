# -*- coding: utf-8 -*-


import numpy as np


def breach_run(perf_meas, pcten):
    """

    Parameters
    ----------
    perf_meas
    pcten: list
        Percentages to calculate to use as tolerance level
    vwe: Not yet implemented!

    Returns
    -------

    """


    breach = np.empty((perf_meas.shape[1], 2 * pcten.size), dtype=int)
    par_size, data_size = perf_meas.shape
    # par_maxreach =

    for i in range(data_size):
        for j, pct_beh in enumerate(pcten):

            # ----- LEFT REACH ------
            # prepare the left reach overview array
            overzichtl = np.array([np.arange(par_size),
                                   np.ones(par_size),
                                   np.zeros(par_size),
                                   np.empty(par_size),
                                   np.empty(par_size)]
                                  ).transpose().astype(float)
            overzichtl[:, 3:5] = np.nan

            aantl = 0  # count the number of data points
            while (aantl <= i) & (sum(overzichtl[:, 1].astype(int)) != 0):
                overzichtl[(overzichtl[:, 1] == 1) &
                           (np.abs(perf_meas[:, i - aantl]) == 0), 2] = \
                    overzichtl[(overzichtl[:, 1] == 1) &
                               (np.abs(perf_meas[:, i - aantl]) == 0),
                               2] + 1 # vwe 2x
                aantl += 1
                overzichtl[overzichtl[:, 2] > pct_beh / 100. * aantl, 1] = 0
                overzichtl[overzichtl[:, 1] == 1, 3] = aantl # or -1(distance?!)
                #overzichtl[overzichtl[:, 1] == 1, 4] = \
                    # overzichtl[overzichtl[:, 1] == 1, 3]

            # maxreachl is a position
            maxreachl = i - (np.nanmax(overzichtl[:, 3],
                                       axis=0)).astype(int) + 1

            if np.isnan(maxreachl):
                maxreachl = i
            else:
                while np.all(np.abs(perf_meas[i - overzichtl[:, 3].astype(
                        int) + 1 == maxreachl, maxreachl]) == 0): # vwe
                    overzichtl[i - overzichtl[:, 3].astype(int) + 1 ==
                               maxreachl, 2:4] = \
                        overzichtl[i - overzichtl[:,3].astype(int) + 1 ==
                                   maxreachl, 2:4] - 1
                    maxreachl += 1

            overzichtl[~np.isnan(overzichtl[:, 3]), 4] = i - \
                                overzichtl[~np.isnan(overzichtl[:, 3]), 3] + 1

            breach[i, 2 * j] = maxreachl

            # ----- RIGHT REACH ------



    return overzichtl, maxreachl
    #return breach, par_maxreach

# -------------------------------
# Running the testdata
# -------------------------------
perf_matrix = np.genfromtxt("/home/stijn_vanhoey/projecten/2015_breach_katrien"
                            "/2017_development/testdata/testdata_subset/"
                            "21_101_acc.csv",
                            delimiter=",", dtype=int)
rel_levels = np.array([40]) # 0 5 10 20

overzichtl, maxreachl = breach_run(perf_matrix, rel_levels) # vwe

print(overzichtl)
print("Maxreach: ", maxreachl)
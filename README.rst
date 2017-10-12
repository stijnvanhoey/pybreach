===============================
Bidirectional Reach (BReach)
===============================


.. image:: https://img.shields.io/pypi/v/pybreach.svg
        :target: https://pypi.python.org/pypi/pybreach

.. image:: https://img.shields.io/travis/stijnvanhoey/pybreach.svg
        :target: https://travis-ci.org/stijnvanhoey/pybreach

.. image:: https://readthedocs.org/projects/pybreach/badge/?version=latest
        :target: https://pybreach.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/stijnvanhoey/pybreach/shield.svg
     :target: https://pyup.io/repos/github/stijnvanhoey/pybreach/
     :alt: Updates
     
.. image:: https://zenodo.org/badge/88784240.svg
   :target: https://zenodo.org/badge/latestdoi/88784240


This Python Package provides an implementation of the methodology presented in Identification of temporal consistency in rating curve data: Bidirectional Reach (BReach_). BReach identifies the consistency of rating curve data based on a quality analysis of model results. Results of this analysis enable the detection of changes in data consistency.

.. _BReach: http://dx.doi.org/10.1002/2016WR018692

* Free software: MIT license
* Documentation: https://pybreach.readthedocs.io.

Features
--------

The BReach methodology consists of different steps, that are described in `Van Eerdenbrugh et al., 2016`_ :

* Step 1: Selection of a model structure for the analysis;
* Step 2: Sampling of the parameter space;
* Step 3: Assessment of acceptable model results;
* Step 4: Assessment of different degrees of tolerance;
* Step 5: Assessment of the bidirectional reach for all degrees of tolerance;
* Step 6: Identification of consistent data periods.

.. _`Van Eerdenbrugh et al., 2016`: http://dx.doi.org/10.1002/2016WR018692

The current scope of the package is to support the execution of steps 4, 5 and 6. Based on a two-dimensional matrix of performance measures (calculated for each data point and a given number of parameter sets), the package calculates the maximum left and right reaches in each data point for different degrees of tolerance and provides the visualisation(s) to interpret the data.

Input
-----

A user has thus to prepare steps 1 - 3 of the methodology prior to the use of the pybreach package. Inputs for the package are:

* A two-dimensional matrix (numpy ndarray) of shape NxM with N the number of model realisations and M the number of model evaluation points (time steps, measured values). This matrix contains binary information that results from step 3 (value '1' = acceptable model result, value '0' = nonacceptable model result).
* A list containing different degrees of tolerance, defining the percentage of points that are allowed to be nonacceptable in the BReach analysis. In both `Van Eerdenbrugh et al., 2016`_ and `Van Eerdenbrugh et al., 2017`_, degrees of tolerance of 0 %, 5 %, 10 %, 20 % and 40 % are used.

.. _`Van Eerdenbrugh et al., 2017`: https://www.hydrol-earth-syst-sci-discuss.net/hess-2017-265/

Ouput
-----

The script pybreach.py_ calculates the maximum left and right reach for a given matrix with model evaluations. The result is a numpy ndarray of shape NxM in which N is the number of model evaluation points and M is 2 * the amount of degrees of tolerance. Columns (2*i-1) contain the maximum left reaches and columns 2*i contain the maximum right reaches for all data points and degree of tolerance i.

.. _pybreach.py: https://github.com/stijnvanhoey/pybreach/blob/v0.3.0/pybreach/pybreach.py

The script breachplot.py_ returns a BReach plot for a given BReach result.

.. _breachplot.py: https://github.com/stijnvanhoey/pybreach/blob/v0.3.0/pybreach/breachplot.py

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


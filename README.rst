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


This Python Package provides an implementation of the methodology presented in Identification of temporal consistency in rating curve data: Bidirectional Reach (BReach_). BReach identifies the consistency of rating curve data based on a quality analysis of model results. Results of this analysis enable the detection of changes in data consistency.

.. _BReach: http://dx.doi.org/10.1002/2016WR018692


* Free software: MIT license
* Documentation: https://pybreach.readthedocs.io.


Features
--------
The current scope of the package is to ensure that based on a 2-D matrix of performance measures (calculated for each data point and a given number of parameter sets), the package calculates both reaches and provides the visualisation(s) to interpret the data.

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


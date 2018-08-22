## Notes

### Kay Diederichs [22/08/2018]


Output of ``xdscc12 -w insulin_XDS_ASCII.HKL`` and ``xdscc12 -w insulin_XDS_ASCII.HKL``, respectively.

- ``-w`` means unweighted by sigma, which is what you want to compare your own implementation against.
- ``-z`` means "do not Fisher-transform the CC1/2 values before calculating their difference".


Without ``-z`` the values are better comparable over a range of CC1/2 values.

The log files in this directory are what ``xdscc12`` produces for the insulin ``XDS_ASCII.HKL``. They should be useful for anyone implementing delta-CC1/2.

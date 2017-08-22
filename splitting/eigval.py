#!/usr/bin/env python

"""
The eigenvalue method of Silver and Chan (1991)
"""

from . import core as c
import numpy as np

def eigcov(pair):
    """get eigenvalues of covariance matrix"""
    return np.sort(np.linalg.eigvals(np.cov(pair,rowvar=True)))
    
def grideigcov(pair,maxshift,window=None, stepang=None,stepshift=None):

    # set some defaults
    if stepshift is None:
        stepshift = 2 * int(np.max([1,maxshift/40]))
    if stepang is None:
        stepang = 2
    if window is None:
        # by default whatevers smaller,
        # half trace length or 10 * max shift
        window = int(np.min([pair.shape[1] * 0.5,maxshift * 10]))

    deg, lag = np.meshgrid(np.arange(0,180,stepang),
                             np.arange(0,maxshift,stepshift).astype(int))

    shape = deg.shape
    lam1 = np.zeros(shape)
    lam2 = np.zeros(shape)
    for ii in np.arange(shape[1]):
        temp = c.rotate(pair,deg[0,ii])
        for jj in np.arange(shape[0]):
            # remove splitting so use inverse operator (negative lag)
            temp2 = c.lag(temp,-lag[jj,ii])
            temp3 = c.window(temp2,window)
            lam2[jj,ii], lam1[jj,ii] = eigcov(temp3)
    return deg, lag, lam1, lam2
import numpy as np 

def amp_ml(ml,r):
    return 10**(ml-1.17*np.log10(r)-0.0514*r+3)

def amp_hutton(ml,r):
    return 10**(ml-1.11*np.log10(r)-0.00189*r+2.09)

def amp_luckett(ml,r):
    return 10**(ml-1.11*np.log10(r)-0.00189*r+2.09+1.16*np.exp(-0.2*r))

def ml_hutton(a,r):
    """Equation to calculte local magnitude using the Luckett scale"""
    mag=(np.log10(a))+(1.11*np.log10(r))+(0.00185*r)-2.09

    return mag

def ml_luc(a,r):
    """Equation to calculte local magnitude using the Luckett scale"""
    mag=(np.log10(a))+(1.11*np.log10(r))+(0.00185*r)-2.09-1.16*np.exp(-0.2*r)

    return mag

def ml_nol(a,r):
    """Equation to calculte local magnitude using the Luckett scale"""
    mag=(np.log10(a))+(1.17*np.log10(r))+(0.0514*r)-3.0
    return mag
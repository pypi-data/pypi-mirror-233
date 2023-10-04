import numpy as np
import scipy.stats as spst

def bs_price(strike, spot, sigma, texp, cp=1, intr=0.0, divr=0.0, is_fwd=False):
    """
    Black-Scholes-Merton model call/put option pricing formula

    Args:
        strike: strike price
        spot: spot (or forward)
        sigma: model volatility
        texp: time to expiry
        cp: 1/-1 for call/put option
        intr: interest rate (domestic interest rate)
        divr: dividend/convenience yield (foreign interest rate)
        is_fwd: if True, treat `spot` as forward price. False by default.

    Returns:
        Vanilla option price
    """
    disc_fac = np.exp(-texp*intr)
    fwd = np.array(spot)*(1.0 if is_fwd else np.exp(-texp*divr)/disc_fac)

    sigma_std = np.maximum(np.array(sigma)*np.sqrt(texp), np.finfo(float).tiny)

    # don't directly compute d1 just in case sigma_std is infty
    d1 = np.log(fwd/strike)/sigma_std
    d2 = d1 - 0.5*sigma_std
    d1 += 0.5*sigma_std

    cp = np.array(cp)
    price = fwd*spst.norm._cdf(cp*d1) - strike*spst.norm._cdf(cp*d2)
    price *= cp*disc_fac
    return price

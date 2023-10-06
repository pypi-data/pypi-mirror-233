import numpy as np

def v1m_cal(WS, height):
    v1m = (np.log10(1.1/0.01)/np.log10(height/0.01)) * WS
    return v1m

def VP_RH_exchange(Ta, RH=None, VP=None):
    """Convert RH to VP if RH is given; Convert VP to RH if RH is given

    Args:
        Ta (float): Air temperature
        RH (float, optional): Relative Humidity. Defaults to None.
        VP (float, optional): Vapor pressure. Defaults to None.

    Returns:
        dict: Contains converted value or both
    """
    # Value checking
    if not Ta:
        raise ValueError("Ta is required.")
    if not any([RH, VP]):
        raise ValueError(f"At least you should give one of RH or VP")
    if RH and VP:
        if VP - 6.1078 * np.exp(17.1 * Ta / (235.0 + Ta)) * (RH / 100) > 1E-6:
            raise ValueError(f"Input RH:{RH} and VP:{VP} mismatched, please check your value")
        else:
            return {"RH": RH, "VP": VP}
    if RH:
        VP = 6.1078 * np.exp(17.1 * Ta / (235.0 + Ta)) * (RH / 100)
        return {"VP": VP}
    elif VP:
        RH = (VP / 6.1078 * np.exp(17.1 * Ta / (235.0 + Ta))) * 100
        return {"RH": RH}

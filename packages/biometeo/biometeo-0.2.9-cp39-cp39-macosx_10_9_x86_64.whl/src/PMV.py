# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 10:13:26 2017

@author: bearsheep

Calculation of Predicted Mean Vote (PMV) (Fanger, 1970)
"""

"""
----------------------------------------------------------------------
		 Predicted Mean Vote nach Fanger (1972)/Jendritzky(1978 + 1990)
         + Luftbelastungsindex nach Naumler et al. (1984)             
		 TP-Version      : 18.08.1992  Andreas Matzarakis
         Python-Version  : 28.03.2017  Yung-Chang Chen
----------------------------------------------------------------------+
"""

import math


class PMVData:
    def __init__(self, pmv, teq, hclo):
        self.pmv = pmv
        self.teq = teq
        self.hclo = hclo


def pmv(ta, vpa, v, tmrt, icl=0.6, work=80, ht=1.75, mbody=75, age=35, sex=1):
    """
    Input:
        ta: Air temperature in screen level (C).
        vpa: Vapor pressure in screen level (hPa).
        tmrt: Mean radiant temperature in screen level (C).
        v: Wind speed in screen level (m/s).
        icl: clothing insulation
        work: activity of subject
        ht: height of subject
        mbody: weight of subject
        age: age of subject
        sex: 1:male 2:female

    Output
        PMV:  Predicted Mean Vote (PMV) in -3.0 to 3.0

    Using example:
        PMV_v  = PMV_func.pmv(ta, vpa, v, tmrt, icl, work, ht, mbody, age, sex)
    """
    # KONSTANTEN
    sigm = 5.67 * math.exp(math.log(10) * -8)
    adu = 0.203 * math.exp(math.log(mbody) * 0.425) * math.exp(math.log(ht) * 0.725)
    tcl = 30.005
    eps = 0.97
    fcl = 1.0 + icl * 0.15
    p = 1013.25
    # alphair = 0.7  #unkown parameter
    eta = 0.0
    if v < 0.1:
        v = 0.1

    # INNERE KOERPERENERGIE
    metbf = 3.19 * math.exp(math.log(mbody) * (3. / 4.)) * (1. + 0.004 * (30. - age) +
                                                            0.018 * (
                                                                    (ht * 100.0 / (math.exp(math.log(mbody)) * (
                                                                            1. / 3.))) - 42.1))

    metbm = 3.45 * math.exp(math.log(mbody) * (3. / 4.)) * (1. + 0.004 * (30. - age) +
                                                            0.010 * (
                                                                (ht * 100.0 / (
                                                                    math.exp(math.log(mbody) * (1. / 3.))) - 43.4)))

    metm = work + metbm
    metf = work + metbf

    if sex == 1:
        met = metm
    if sex == 2:
        met = metf

    h = met * (1.0 - eta)
    aef = 0.71 * fcl * adu
    # rtv = 5.16 * met  #unkown parameter

    for l in range(1, 3):
        if l == 1:
            hc = 12.06 * math.exp(math.log(v) * 0.5)
        k = 1
        tcl1 = 30.005

        while k <= 100:
            if l == 2:
                hc = 2.38 * math.exp(math.log((math.fabs(tcl1 - ta))) * 0.25)

            tcl2 = 35.7 - 0.032 * (met / (adu * 1.16)) * (1. - eta) - \
                   0.155 * icl * (3.94 * 0.00000001 * fcl * (
                    math.exp(math.log(tcl1 + 273.2) * 4) - math.exp(math.log(tmrt + 273.2) * 4))
                                  + fcl * hc * (tcl1 - ta))

            diff = math.fabs(tcl1 - tcl2)

            if diff < 0.01:
                break
            if l == 1:
                abhc = 0
            if l == 2:
                abhc = 0.6 * math.exp(math.log(math.fabs(tcl1 - ta)) * (-0.75))

            abtcl = -0.155 * icl * (4. * 3.94 * math.exp(math.log(10) * (-8)) * fcl *
                                    math.exp(math.log(tcl1 + 273.2) * 3) + fcl * hc - fcl * (tcl1 - ta) * abhc) - 1.0

            tcl1 = tcl1 - (tcl2 - tcl1) / abtcl
            k = k + 1

        tcl = tcl1
        h = met * (1 - eta)
        tsk = 35.7 - (0.028 * h / adu)
        esw = 0.42 * adu * (h / adu - 58.08)

        if esw < 0:
            esw = 0

        hclo = adu * ((tsk - tcl) / (0.18 * icl))

        rsum = aef * eps * sigm * (math.exp(math.log(tcl + 273.2) * 4) -
                                   math.exp(math.log(tmrt + 273.2) * 4))

        csum = adu * fcl * hc * (tcl - ta)

        erel = 0.0023 * met * (44. - 0.75 * vpa)

        eres = 0.0014 * met * (34. - ta)

        ere = erel + eres

        ed = 0.406 * adu * (1.92 * tsk - 25.3 - 0.75 * vpa)

        load = h - ed - ere - esw - rsum - csum

        load2 = load / adu

        pmv = (0.303 * math.exp(-0.036 * (met / adu)) + 0.028) * load2

        teq = ta + 0.622 * vpa / (p - vpa) * (2500.78 - 2.325734 *
                                              ta) / (1.00482 + 0.622 * vpa / (p - vpa) * 4.18674)

        difhc = 12.06 * math.exp(math.log(v) * 0.5) - 2.38 * math.exp(math.log((math.fabs(ta - tcl)) * 0.25))

        if l == 1 and difhc > 0:
            break
    return PMVData(pmv, teq, hclo)
    # return {"pmv": pmv, "teq": teq, "hclo": hclo}

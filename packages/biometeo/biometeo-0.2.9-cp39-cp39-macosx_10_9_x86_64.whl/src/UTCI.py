# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a UTCI-approx f calculation script file.
Ta: Air temperature in screen level (C).
ehPa: Vapor pressure in screen level (hPa).
Tmrt: Mean radiant temperature in screen level (C).
va: Wind speed in screen level (m/s).
UTCI_approx: Univeseral Thernal Climate Index (C).
"""
import math

"""
def esf(Ta):
   g=[-2.8365744E3, -6.028076559E3, 1.954263612E1, -2.737830188E-2, 
      1.6261698E-5, 7.0229056E-10, -1.8680009E-13, 2.7150305]
   tk=Ta+273.15
   es=g[7]*math.log10(tk)
   for i in range(0,7):
     es=es+g[i]*math.pow(tk, (i-2))
   es=math.exp(es)*0.01
   return es
"""


def UTCI_app_cal(Ta, ehPa, Tmrt, va):
    """
    Input:
        Ta: Air temperature in screen level (C).
        ehPa: Vapor pressure in screen level (hPa).
        Tmrt: Mean radiant temperature in screen level (C).
        va: Wind speed in screen level (m/s).
        ErrV: error value

    Output:
        UTCI_approx: Univeseral Thernal Climate Index (C).

    Using example:
        UTCI_v = UTCI_apporf.UTCI_app_cal(Ta, VP, Tmrt, v, -9999)
    """

    def utci_approxf(Ta, ehPa, Tmrt, va):
        # calculate the delta of Ta and Tmrt
        D_Tmrt = Tmrt - Ta
        # transfer Vapor pressue in unit hPa to kPa
        Pa = ehPa / 10.0
        # do approxiatie calculation of UTCI
        ta_ = Ta + (6.07562052E-01) + (-2.27712343E-02) * Ta + (8.06470249E-04) * Ta ** 2 + (
            -1.54271372E-04) * Ta ** 3 + (-3.24651735E-06) * Ta ** 4 + (7.32602852E-08) * Ta ** 5 + (
                  1.35959073E-09) * Ta ** 6
        ta_va = (-2.25836520E+00) * va + (8.80326035E-02) * Ta * va + (2.16844454E-03) * Ta ** 2 * va + (
            -1.53347087E-05) * Ta ** 3 * va + (-5.72983704E-07) * Ta ** 4 * va + (-2.55090145E-09) * Ta ** 5 * va
        va_va = (-7.51269505E-01) * va ** 2 + (-4.08350271E-03) * Ta * va ** 2 + (
            -5.21670675E-05) * Ta ** 2 * va ** 2 + (1.94544667E-06) * Ta ** 3 * va ** 2 + (
                    1.14099531E-08) * Ta ** 4 * va ** 2 + (1.58137256E-01) * va * va * va
        va_ = (-6.57263143E-05) * Ta * va ** 3 + (2.22697524E-07) * Ta ** 2 * va ** 3 + (
            -4.16117031E-08) * Ta ** 3 * va ** 3 + (-1.27762753E-02) * va ** 4 + (9.66891875E-06) * Ta * va ** 4
        e_va_ = (2.52785852E-09) * Ta ** 2 * va ** 4 + (4.56306672E-04) * va ** 5 + (-1.74202546E-07) * Ta * va ** 5 + (
            -5.91491269E-06) * va ** 6
        tmrt = (3.98374029E-01) * D_Tmrt + (1.83945314E-04) * Ta * D_Tmrt + (-1.73754510E-04) * Ta ** 2 * D_Tmrt + (
            -7.60781159E-07) * Ta ** 3 * D_Tmrt + (3.77830287E-08) * Ta ** 4 * D_Tmrt + (
                   5.43079673E-10) * Ta ** 5 * D_Tmrt
        d_tmrt = (-2.00518269E-02) * va * D_Tmrt + (8.92859837E-04) * Ta * va * D_Tmrt + (
            3.45433048E-06) * Ta * Ta * va * D_Tmrt + (-3.77925774E-07) * Ta ** 3 * va * D_Tmrt + (
                     -1.69699377E-09) * Ta ** 4 * va * D_Tmrt + (1.69992415E-04) * va * va * D_Tmrt
        va_d_tmrt = (-4.99204314E-05) * Ta * va * va * D_Tmrt + (2.47417178E-07) * Ta * Ta * va * va * D_Tmrt + (
            1.07596466E-08) * Ta ** 3 * va ** 2 * D_Tmrt + (8.49242932E-05) * va ** 3 * D_Tmrt + (
                        1.35191328E-06) * Ta * va * va * va * D_Tmrt
        tmrt_ = (-6.21531254E-09) * Ta * Ta * va ** 3 * D_Tmrt + (-4.99410301E-06) * va ** 4 * D_Tmrt + (
            -1.89489258E-08) * Ta * va ** 4 * D_Tmrt + (8.15300114E-08) * va ** 5 * D_Tmrt + (
                    7.55043090E-04) * D_Tmrt ** 2
        d_tmrt_ = (-5.65095215E-05) * Ta * D_Tmrt ** 2 + (-4.52166564E-07) * Ta * Ta * D_Tmrt ** 2 + (
            2.46688878E-08) * Ta ** 3 * D_Tmrt ** 2 + (2.42674348E-10) * Ta ** 4 * D_Tmrt ** 2 + (
                      1.54547250E-04) * va * D_Tmrt ** 2
        tmrt_d_tmrt = (5.24110970E-06) * Ta * va * D_Tmrt ** 2 + (
            -8.75874982E-08) * Ta * Ta * va * D_Tmrt ** 2 + (
                          -1.50743064E-09) * Ta * Ta * Ta * va * D_Tmrt ** 2 + (
                          -1.56236307E-05) * va * va * D_Tmrt ** 2 + (
                          -1.33895614E-07) * Ta * va * va * D_Tmrt ** 2
        d_tmrt_d_tmrt = (2.49709824E-09) * Ta * Ta * va * va * D_Tmrt ** 2 + (
            6.51711721E-07) * va * va * va * D_Tmrt ** 2 + (
                            1.94960053E-09) * Ta * va * va * va * D_Tmrt ** 2 + (
                            -1.00361113E-08) * va * va * va * va * D_Tmrt ** 2
        tmrt_d_tmrt_d_tmrt = (-1.21206673E-05) * D_Tmrt ** 3 + (
            -2.18203660E-07) * Ta * D_Tmrt ** 3 + (7.51269482E-09) * Ta * Ta * D_Tmrt ** 3 + (
                                 9.79063848E-11) * Ta * Ta * Ta * D_Tmrt ** 3 + (
                                 1.25006734E-06) * va * D_Tmrt ** 3
        d_tmrt_d_tmrt_d_tmrt = (-1.81584736E-09) * Ta * va * D_Tmrt ** 3 + (
            -3.52197671E-10) * Ta * Ta * va * D_Tmrt ** 3 + (
                                   -3.36514630E-08) * va * va * D_Tmrt ** 3 + (
                                   1.35908359E-10) * Ta * va * va * D_Tmrt ** 3 + (
                                   4.17032620E-10) * va * va * va * D_Tmrt ** 3
        tmrt1 = (-1.30369025E-09) * D_Tmrt ** 3 * D_Tmrt + (
            4.13908461E-10) * Ta * D_Tmrt ** 3 * D_Tmrt + (
                    9.22652254E-12) * Ta * Ta * D_Tmrt ** 3 * D_Tmrt + (
                    -5.08220384E-09) * va * D_Tmrt ** 3 * D_Tmrt
        tmrt2 = (-2.24730961E-11) * Ta * va * D_Tmrt ** 3 * D_Tmrt + (
            1.17139133E-10) * va * va * D_Tmrt ** 3 * D_Tmrt + (
                    6.62154879E-10) * D_Tmrt ** 3 * D_Tmrt ** 2 + (
                    4.03863260E-13) * Ta * D_Tmrt ** 3 * D_Tmrt ** 2
        pa = (1.95087203E-12) * va * D_Tmrt ** 3 * D_Tmrt ** 2 + (
            -4.73602469E-12) * D_Tmrt ** 3 * D_Tmrt ** 3 + (5.12733497E+00) * Pa + (
                 -3.12788561E-01) * Ta * Pa + (-1.96701861E-02) * Ta * Ta * Pa + (9.99690870E-04) * Ta * Ta * Ta * Pa
        va_pa = (9.51738512E-06) * Ta * Ta * Ta * Ta * Pa + (-4.66426341E-07) * Ta * Ta * Ta * Ta * Ta * Pa + (
            5.48050612E-01) * va * Pa + (-3.30552823E-03) * Ta * va * Pa + (-1.64119440E-03) * Ta * Ta * va * Pa
        va_va_pa = (-5.16670694E-06) * Ta * Ta * Ta * va * Pa + (9.52692432E-07) * Ta * Ta * Ta * Ta * va * Pa + (
            -4.29223622E-02) * va * va * Pa + (5.00845667E-03) * Ta * va * va * Pa
        va_va_va_pa = (1.00601257E-06) * Ta * Ta * va * va * Pa + (-1.81748644E-06) * Ta * Ta * Ta * va * va * Pa + (
            -1.25813502E-03) * va * va * va * Pa + (-1.79330391E-04) * Ta * va * va * va * Pa
        va_va_va_va_pa = (2.34994441E-06) * Ta * Ta * va * va * va * Pa + (1.29735808E-04) * va * va * va * va * Pa + (
            1.29064870E-06) * Ta * va * va * va * va * Pa + (-2.28558686E-06) * va * va * va * va * va * Pa
        tmrt_pa = (-3.69476348E-02) * D_Tmrt * Pa + (1.62325322E-03) * Ta * D_Tmrt * Pa + (
            -3.14279680E-05) * Ta * Ta * D_Tmrt * Pa + (2.59835559E-06) * Ta * Ta * Ta * D_Tmrt * Pa
        d_tmrt_pa = (-4.77136523E-08) * Ta * Ta * Ta * Ta * D_Tmrt * Pa + (8.64203390E-03) * va * D_Tmrt * Pa + (
            -6.87405181E-04) * Ta * va * D_Tmrt * Pa + (-9.13863872E-06) * Ta * Ta * va * D_Tmrt * Pa
        va_d_tmrt_pa = (5.15916806E-07) * Ta * Ta * Ta * va * D_Tmrt * Pa + (
            -3.59217476E-05) * va * va * D_Tmrt * Pa + (3.28696511E-05) * Ta * va * va * D_Tmrt * Pa + (
                           -7.10542454E-07) * Ta * Ta * va * va * D_Tmrt * Pa + (
                           -1.24382300E-05) * va * va * va * D_Tmrt * Pa
        tmrt_d_tmrt_pa = (-7.38584400E-09) * Ta * va * va * va * D_Tmrt * Pa + (
            2.20609296E-07) * va * va * va * va * D_Tmrt * Pa + (-7.32469180E-04) * D_Tmrt ** 2 * Pa + (
                             -1.87381964E-05) * Ta * D_Tmrt ** 2 * Pa + (
                             4.80925239E-06) * Ta * Ta * D_Tmrt ** 2 * Pa
        d_tmrt_d_tmrt_pa = (-8.75492040E-08) * Ta * Ta * Ta * D_Tmrt ** 2 * Pa + (
            2.77862930E-05) * va * D_Tmrt ** 2 * Pa + (-5.06004592E-06) * Ta * va * D_Tmrt ** 2 * Pa + (
                               1.14325367E-07) * Ta * Ta * va * D_Tmrt ** 2 * Pa
        tmrt_d_tmrt_d_tmrt_pa = (2.53016723E-06) * va * va * D_Tmrt ** 2 * Pa + (
            -1.72857035E-08) * Ta * va * va * D_Tmrt ** 2 * Pa + (
                                    -3.95079398E-08) * va * va * va * D_Tmrt ** 2 * Pa + (
                                    -3.59413173E-07) * D_Tmrt ** 3 * Pa
        d_tmrt_d_tmrt_d_tmrt_pa = (7.04388046E-07) * Ta * D_Tmrt ** 3 * Pa + (
            -1.89309167E-08) * Ta * Ta * D_Tmrt ** 3 * Pa + (
                                      -4.79768731E-07) * va * D_Tmrt ** 3 * Pa + (
                                      7.96079978E-09) * Ta * va * D_Tmrt ** 3 * Pa
        pa1 = (1.62897058E-09) * va * va * D_Tmrt ** 3 * Pa + (
            3.94367674E-08) * D_Tmrt ** 3 * D_Tmrt * Pa + (
                  -1.18566247E-09) * Ta * D_Tmrt ** 3 * D_Tmrt * Pa + (
                  3.34678041E-10) * va * D_Tmrt ** 3 * D_Tmrt * Pa
        pa_pa = (-1.15606447E-10) * D_Tmrt ** 3 * D_Tmrt ** 2 * Pa + (-2.80626406E+00) * Pa * Pa + (
            5.48712484E-01) * Ta * Pa * Pa + (-3.99428410E-03) * Ta * Ta * Pa * Pa + (
                    -9.54009191E-04) * Ta * Ta * Ta * Pa * Pa
        va_pa_pa = (1.93090978E-05) * Ta * Ta * Ta * Ta * Pa * Pa + (-3.08806365E-01) * va * Pa * Pa + (
            1.16952364E-02) * Ta * va * Pa * Pa + (4.95271903E-04) * Ta * Ta * va * Pa * Pa + (
                       -1.90710882E-05) * Ta * Ta * Ta * va * Pa * Pa
        va_va_pa_pa = (2.10787756E-03) * va * va * Pa * Pa + (-6.98445738E-04) * Ta * va * va * Pa * Pa + (
            2.30109073E-05) * Ta * Ta * va * va * Pa * Pa + (4.17856590E-04) * va * va * va * Pa * Pa + (
                          -1.27043871E-05) * Ta * va * va * va * Pa * Pa
        tmrt_pa_pa = (-3.04620472E-06) * va * va * va * va * Pa * Pa + (5.14507424E-02) * D_Tmrt * Pa * Pa + (
            -4.32510997E-03) * Ta * D_Tmrt * Pa * Pa + (8.99281156E-05) * Ta * Ta * D_Tmrt * Pa * Pa
        d_tmrt_pa_pa = (-7.14663943E-07) * Ta * Ta * Ta * D_Tmrt * Pa * Pa + (
            -2.66016305E-04) * va * D_Tmrt * Pa * Pa + (2.63789586E-04) * Ta * va * D_Tmrt * Pa * Pa + (
                           -7.01199003E-06) * Ta * Ta * va * D_Tmrt * Pa * Pa
        tmrt_d_tmrt_pa_pa = (-1.06823306E-04) * va * va * D_Tmrt * Pa * Pa + (
            3.61341136E-06) * Ta * va * va * D_Tmrt * Pa * Pa + (2.29748967E-07) * va * va * va * D_Tmrt * Pa * Pa + (
                                3.04788893E-04) * D_Tmrt ** 2 * Pa * Pa
        d_tmrt_d_tmrt_pa_pa = (-6.42070836E-05) * Ta * D_Tmrt ** 2 * Pa * Pa + (
            1.16257971E-06) * Ta * Ta * D_Tmrt ** 2 * Pa * Pa + (
                                  7.68023384E-06) * va * D_Tmrt ** 2 * Pa * Pa + (
                                  -5.47446896E-07) * Ta * va * D_Tmrt ** 2 * Pa * Pa
        e_d_tmrt_pa_pa = (-3.59937910E-08) * va ** 2 * D_Tmrt ** 2 * Pa * Pa + (
            -4.36497725E-06) * D_Tmrt ** 3 * Pa * Pa + (1.68737969E-07) * Ta * D_Tmrt ** 3 * Pa * Pa + (
                             2.67489271E-08) * va * D_Tmrt ** 3 * Pa * Pa + (3.23926897E-09) * D_Tmrt ** 4 * Pa * Pa
        pa_ = (-3.53874123E-02) * Pa ** 3 + (-2.21201190E-01) * Ta * Pa ** 3 + (1.55126038E-02) * Ta * Ta * Pa ** 3 + (
            -2.63917279E-04) * Ta ** 3 * Pa ** 3 + (4.53433455E-02) * va * Pa ** 3 + (
                  -4.32943862E-03) * Ta * va * Pa ** 3
        tmrt_pa_ = (1.45389826E-04) * Ta ** 2 * va * Pa ** 3 + (2.17508610E-04) * va ** 2 * Pa ** 3 + (
            -6.66724702E-05) * Ta * va ** 2 * Pa ** 3 + (3.33217140E-05) * va ** 3 * Pa ** 3 + (
                       -2.26921615E-03) * D_Tmrt * Pa ** 3
        d_tmrt_pa_ = (3.80261982E-04) * Ta * D_Tmrt * Pa ** 3 + (-5.45314314E-09) * Ta * Ta * D_Tmrt * Pa ** 3 + (
            -7.96355448E-04) * va * D_Tmrt * Pa ** 3 + (2.53458034E-05) * Ta * va * D_Tmrt * Pa ** 3
        e_d_tmrt_pa_ = (-6.31223658E-06) * va * va * D_Tmrt * Pa ** 3 + (3.02122035E-04) * D_Tmrt ** 2 * Pa ** 3 + (
            -4.77403547E-06) * Ta * D_Tmrt ** 2 * Pa ** 3 + (1.73825715E-06) * va * D_Tmrt ** 2 * Pa ** 3 + (
                           -4.09087898E-07) * D_Tmrt ** 3 * Pa ** 3
        va_pa_ = (6.14155345E-01) * Pa ** 4 + (-6.16755931E-02) * Ta * Pa ** 4 + (
            1.33374846E-03) * Ta * Ta * Pa ** 4 + (3.55375387E-03) * va * Pa ** 4 + (
                     -5.13027851E-04) * Ta * va * Pa ** 4
        pa___e_d_tmrt_pa_ = (1.02449757E-04) * va * va * Pa ** 4 + (-1.48526421E-03) * D_Tmrt * Pa ** 4 + (
            -4.11469183E-05) * Ta * D_Tmrt * Pa ** 4 + (-6.80434415E-06) * va * D_Tmrt * Pa ** 4 + (
                                -9.77675906E-06) * D_Tmrt ** 2 * Pa ** 4
        e_pa_ = (8.82773108E-02) * Pa ** 4 * Pa + (-3.01859306E-03) * Ta * Pa ** 4 * Pa + (
            1.04452989E-03) * va * Pa ** 4 * Pa + (2.47090539E-04) * D_Tmrt * Pa ** 5 + (1.48348065E-03) * Pa ** 6
        tmrt_va_d_tmrt = ta_ + ta_va + va_va + va_ + e_va_ + tmrt + d_tmrt + va_d_tmrt
        tmrt3 = tmrt_ + d_tmrt_ + tmrt_d_tmrt + d_tmrt_d_tmrt + tmrt_d_tmrt_d_tmrt + d_tmrt_d_tmrt_d_tmrt
        pa_tmrt_pa = pa + va_pa + va_va_pa + va_va_va_pa + va_va_va_va_pa + tmrt_pa
        pa_tmrt_d_tmrt_d_tmrt_pa = d_tmrt_pa + va_d_tmrt_pa + tmrt_d_tmrt_pa + d_tmrt_d_tmrt_pa + tmrt_d_tmrt_d_tmrt_pa
        pa_tmrt_d_tmrt_pa_pa = d_tmrt_d_tmrt_d_tmrt_pa + pa1 + pa_pa + va_pa_pa + va_va_pa_pa + tmrt_pa_pa + d_tmrt_pa_pa + tmrt_d_tmrt_pa_pa
        pa__e_d_tmrt_pa_ = d_tmrt_d_tmrt_pa_pa + e_d_tmrt_pa_pa + pa_ + tmrt_pa_ + d_tmrt_pa_ + e_d_tmrt_pa_
        pa__e_pa_ = va_pa_ + pa___e_d_tmrt_pa_ + e_pa_
        UTCI_approx = tmrt_va_d_tmrt + tmrt3 + tmrt1 + tmrt2 + pa_tmrt_pa + pa_tmrt_d_tmrt_d_tmrt_pa + pa_tmrt_d_tmrt_pa_pa + pa__e_d_tmrt_pa_ + pa__e_pa_
        return UTCI_approx

    ## valid wind speed from 1.1 m to 10 m;
    va = (math.log10(10/0.01)/math.log10(1.1/0.01))*va

    if Ta < -50 or Ta > 50:
        raise ValueError(f"Ta value: {Ta}, Ta should not below -50 or above 50 ")
    elif Tmrt < (Ta - 30) or Tmrt > (Ta + 70):
        raise ValueError(f"Tmrt value: {Tmrt}, Ta value: {Ta}, Tmrt should not below Ta - 30 or above Ta + 70 ")
    elif va < 0.5 or va > 30:
        raise ValueError(f"Va value: {va}, Wind speed should not below 0.5 or above 30 ")
    elif ehPa < 0 or ehPa > 50:
        raise ValueError(f"ehpa value: {ehPa}, vapor pressure shoud not below 0 or above 50 ")
    else:
        return utci_approxf(Ta, ehPa, Tmrt, va)

# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 18:28:26 2017

@author: Yung-Chang Chen ycchen0422@gmail.com

This is a PET calculation script file.
Ta: Air temperature in screen level (C).
vpa: Vapor pressure in screen level (hPa).
Tmrt: Mean radiant temperature in screen level (C).
v: Wind speed in screen level (m/s).
icl: clothing insulation
work: activity of subject
ht: height of subject
mbody: weight of subject
age: age of subject
sex # 1:male 2:female
pos # 1:standing 2:sitting
PET: Pysiologically Equivalent Temperature (C).

"""

import math
import numpy as np


def mPET(ta, vpa, WS, tmrt, icl=0.9, work=80, ht=1.75, mbody=75, age=35, sex=1, pos=1, clo_auto=True):
    """
    Input:
        Ta: Air temperature in screen level (C).
        VP: Vapor pressure in screen level (hPa).
        Tmrt: Mean radiant temperature in screen level (C).
        v: Wind speed in screen level (m/s).
        icl: clothing insulation
        work: activity of subject
        ht: height of subject
        mbody: weight of subject
        age: age of subject
        sex: 1:male 2:female
        pos: 1:standing 2:sitting
        clo_auto: boolean value, if true, applying default clothing insulation

    Output:
        mPET: modified Pysiologically Equivalent Temperature (C).
        T_core: core temperature of subject (C).
        Tsk_mm: mean skin temperature of subject (C). 
        Tcl: mean clothing temperature of subject (C).
        Vpts: mean skin vapor pressure (hPa)
        sk_wetted_mm: mean skin wettedness.
        wetsk: saturated ration of skin.
        h: metabolic rate (W/m^2).
        Ere: respiratory energy fluxes  (W/m^2).
        csum: convective energy fluxes (W/m^2). 
        rsum: radiative energy fluxes (W/m^2).
        wetsum: all evaporative energy fluxes of skin (W/m^2)

    Using example:
        {mPET, T_core, tsk_mm, tcl, vpts, wetsk, icl, sk_wetted_mm, h, wet_sum, csum, rsum, enbal2} = biometeo.mPET(Ta, VP, v, Tmrt, icl, work, ht, mbody, age, sex, pos, clo_auto)

    """
    # general parameters
    time = 1.0    # {s}
    TI = 20.0
    # Set physiological parameters
    M_k = 0.42    # {W/(m*K)}     conductivity of muscels
    M_d = 1085.0  # {kg/m^3}      density
    M_c = 3786.0  # {J/(kg*k)}    heat capacity
    M_w = 0.0005380 / time  # {1/s}         blood perfusion

    fat_k = 0.16    # {W/(m*K)}
    fat_d = 850.0   # {kg/m^3}
    fat_c = 2300.0  # {J/(kg*k)}
    fat_w = 0.0000036 / time  # {1/s}

    sk_k = 0.47    # {W/(m*K)}
    sk_d = 1085.0  # {kg/m^3}
    sk_c = 3680.0  # {J/(kg*k)}
    sk_w = 0.0015  # {1/s}
    sk_br_w = 0.00548 / time  # {1/s}

    br_k = 0.49    # {W/(m*K)}
    br_d = 1080.0  # {kg/m^3};
    br_c = 3850    # {J/(kg*k)}
    br_w = 0.0101320 / time  # {1/s}

    bl_d = 1069.0  # {kg/m^3}   blood density
    bl_c = 3650.0  # {J/(kg*k)}   blood conductivity

    T_core_i = 36.5  # definition of initial core temperature
    T_sk_i   = 33.0    # definition of initial skin temperature
    #T_sk_i: = (T_sk_0 + Ta) / 2;
    h        = 0.0
    eta      = 0.1
    met      = 0.0
    enbal2   = 0.0
    wetsk    = 0.0

    #Environmental parameters

    p     = 1013.25  #(hPa)
    p0    = 1013.25  #(hPa)
    # Limitation of vpa
    #if vpa > 50:
    #    vpa = 50


    e_sk  = 0.99
    e_cl  = 0.95
    sigma = 5.67 * math.pow(10, -8.0)

    if pos == 2:
        feff = 0.696
    else:
        feff = 0.725

    evap  = 2.42 * math.pow(10, 6.0)

    if WS < 0.1:
        WS = 0.1

    if ta >= 0:
        VPa_s = 6.1078 * math.exp((17.0809 * ta) / (234.175 + ta))
    if ta < 0:
        VPa_s = 6.1078 * math.exp((17.8436 * ta) / (245.425 + ta))

    RH = vpa/VPa_s

    if RH > 1.0:
        RH = 1.0
        vpa = VPa_s
    if RH < 0.0:
        RH = 0.0
        vpa = 0.0


    I_a = 0.0853  # (m ^ 2 * k / w) outer air insulation
    clo_air_in = 0.033  # set air insulation inside clothing close to skin

    br_sk_c = 0.08

    hc  = 2.67 + (6.5 * math.pow(WS, 0.67))
    hc0 = 2.67 + (6.5 * math.pow(0.1, 0.67))

    #hc = 4.0 * WS + 0.35 * WS * TI - 0.0008 * math.pow(WS * TI, 2) + 3.4;
    #hc = 12.1 * math.pow((WS + 0.0052 * (work - 58)), 0.5)

    hc  = hc * math.pow((p / p0), 0.55)
    hc0 = hc0 * math.pow((p / p0), 0.55)


    Re_factor = 1.0

    def insidebody(ta, vpa, work, ht, mbody, age, sex):

        #global adu, h, h0, cair, rad_brain, rad_brain_skin, rad_brain_fat, rad_brain_inside, ht_brain, ht_body, rad_body, rad_body_skin, rad_body_fat, rad_body_inside, rtv, ere

        metbf = 3.19 * math.pow(mbody, (3. / 4)) * (
            1. + 0.004 * (30. - age) + 0.018 * ((ht * 100. / (math.pow(mbody, (1. / 3)))) - 42.1))
        metbm = 3.45 * math.pow(mbody, (3. / 4)) * (
            1. + 0.004 * (30. - age) + 0.010 * ((ht * 100. / (math.pow(mbody, (1. / 3)))) - 43.4))

        metm = work + metbm
        metf = work + metbf
        BMI = mbody / (math.pow(ht, 2))
        adu = 0.203 * math.pow(mbody, 0.425) * math.pow(ht, 0.725)

        # Fat-procent modification due to age
        if age < 20:
            fat_pm = 0.17
            fat_pf = 0.22
        # end
        if (age >= 20) and (age < 30):
            fat_pm = 0.18
            fat_pf = 0.23
        # end
        if (age >= 30) and (age < 40):
            fat_pm = 0.19
            fat_pf = 0.24
        # end
        if (age >= 40) and (age < 50):
            fat_pm = 0.20
            fat_pf = 0.25
        # end
        if (age >= 50):
            fat_pm = 0.21
            fat_pf = 0.26
        # end

        # Fat-procent modication due to BMI
        if (BMI < 16):
            fat_pm = fat_pm + 0.01 * (BMI - 16) + 0.015 * (16 - 18) + 0.025 * (18 - 20)
            fat_pf = fat_pf + 0.01 * (BMI - 16) + 0.015 * (16 - 18) + 0.025 * (18 - 20)
        # end
        if (BMI < 18) and (BMI >= 16):
            fat_pm = fat_pm + 0.015 * (BMI - 18) + 0.025 * (18 - 20)
            fat_pf = fat_pf + 0.015 * (BMI - 18) + 0.025 * (18 - 20)
        # end
        if (BMI < 20) and (BMI >= 18):
            fat_pm = fat_pm + 0.025 * (BMI - 20)
            fat_pf = fat_pf + 0.025 * (BMI - 20)
        # end
        if (BMI > 25) and (BMI <= 30):
            fat_pm = fat_pm + 0.01 * (BMI - 25)
            fat_pf = fat_pf + 0.01 * (BMI - 25)
        # end
        if (BMI > 30) and (BMI <= 35):
            fat_pm = fat_pm + 0.015 * (BMI - 30) + 0.01 * (30 - 25)
            fat_pf = fat_pf + 0.015 * (BMI - 30) + 0.01 * (30 - 25)
        # end
        if (BMI > 35) and (BMI <= 40):
            fat_pm = fat_pm + 0.02 * (BMI - 35) + 0.015 * (35 - 30) + 0.01 * (30 - 25)
            fat_pf = fat_pf + 0.02 * (BMI - 35) + 0.015 * (35 - 30) + 0.01 * (30 - 25)
        # end
        if (BMI > 40):
            fat_pm = fat_pm + 0.03 * (BMI - 40) + 0.02 * (40 - 35) + 0.015 * (35 - 30) + 0.01 * (30 - 25)
            fat_pf = fat_pf + 0.03 * (BMI - 40) + 0.02 * (40 - 35) + 0.015 * (35 - 30) + 0.01 * (30 - 25)
        # end

        if sex == 1:
            met = metm
            fat_p = fat_pm
            met0 = 80 + metbm
        # end
        if sex == 2:
            met = metf
            fat_p = fat_pf
            met0 = 80 + metbf
        # end

        # Size of body's cylinder
        rad_brain = 0.105  # radius (m)
        rad_brain_skin = 0.002
        rad_brain_fat = 0.01
        rad_brain_inside = rad_brain - rad_brain_fat - rad_brain_skin

        ht_brain = 0.24  # ht_brain: hight of brain
        ht_body = ht - ht_brain  # ht_body: hight of torso and legs

        rad_body_fat = math.sqrt(fat_p * mbody / (850 * math.pi * ht_body))
        rad_body_inside = math.sqrt((1 - fat_p) * mbody / (1100 * math.pi * ht_body))
        rad_body_skin = 0.002
        rad_body = rad_body_fat + rad_body_inside + rad_body_skin

        h = met * (1 - eta)  # h: heat production by metabolism
        h0 = met0 * 1.0
        #h0 = met0 * (1 - eta)
        # h:=work*(1-eta)

        # SENSIBLE RESPIRATIONS ENERGIE
        cair = 1.01 * 1000
        tex = 0.47 * ta + 21.0
        # rtv   = 1.44 * 10. ** (-6.) * met
        rtv = 1.44 * math.pow(10., -6) * met
        eres = cair * (ta - tex) * rtv
        # LATENTE RESPIRATIONSENERGIE
        # vpex  := 6.11 * 10. ** (7.45 * tex / (235. +tex));
        vpex = 6.11 * math.pow(10., (7.45 * tex / (235. + tex)))
        erel = 0.623 * evap / p * (vpa - vpex) * rtv
        #       SUMME DER ERGEBNISSE
        ere = eres + erel

        return adu, h, h0, cair, rad_brain, rad_brain_skin, rad_brain_fat, rad_brain_inside, ht_brain, ht_body, rad_body, rad_body_skin, rad_body_fat, rad_body_inside, rtv, ere
    # End of inside body

    def Auto_Icl_define(ta, clo_auto, icl):
        if clo_auto == True:
            icl = 1.372 - 0.01866 * ta - 0.0004849 * math.pow(ta, 2) - 0.000009333 * math.pow(ta, 3)
        # end

        # Limitation of Icl (clo)
        if icl < 0.3:
            icl = 0.3
        if icl > 2.5:
            icl = 2.5
        # end of limitation of Icl

        fcl = 1 + 1.81 * icl * 0.155
        return icl, fcl

    def Icl_define_i(icl, I_a, br_sk_c): # for I_a as initial setting of clothing insulation

        #global icl_catel, facl, fcl, body_cover_1, body_cover_2, body_cover_3, br_sk_1, clo_1, clo_2, clo_3, clo_cap, \
        #    clo_1_T, clo_2_T, clo_3_T, clo_cap_T, body_cover_arr

        body_cover_1 = 0.0
        body_cover_2 = 0.0
        body_cover_3 = 0.0
        br_sk_1      = 0.0
        clo_1        = 0.0
        clo_2        = 0.0
        clo_3        = 0.0
        clo_cap      = 0.0
        clo_1_T      = 0.0
        clo_2_T      = 0.0
        clo_3_T      = 0.0
        clo_cap_T    = 0.0




        if icl <= 0.6:
            icl_catel = 1
            facl = 0.62

            body_cover_1 = 0.62  # ratio covered by clothing

            clo_1 = icl * 0.155
            clo_1_T = clo_1 + I_a / (1 + 1.81 * clo_1)

            body_cover_arr = np.array([body_cover_1, br_sk_c, 1 - body_cover_1 - br_sk_c ])

        elif 0.6 < icl <= 0.9:
            icl_catel = 2
            facl = 0.81

            body_cover_1 = 0.45
            body_cover_2 = 0.36

            clo_1 = 0.155 * (0.9 * icl + 0.3733)
            clo_1_T = clo_1 + I_a / (1 + 1.81 * clo_1)

            clo_2 = 0.155 * (0.9 * icl - 0.1133)
            clo_2_T = clo_2 + I_a / (1 + 1.81 * clo_2)

            body_cover_arr = np.array([body_cover_1, br_sk_c, body_cover_2, 1 - body_cover_1 - body_cover_2 - br_sk_c])

        elif 0.9 < icl <= 1.2:
            icl_catel = 3
            facl = 0.87

            body_cover_1 = 0.45
            body_cover_2 = 0.42

            clo_1 = 0.155 * (-9 * math.pow(icl, 2) + 21 * icl - 10.38)
            clo_1_T = clo_1 + I_a / (1 + 1.81 * clo_1)

            clo_2 = 0.155 * (2 * math.pow(icl, 2) - 3.6 * icl + 2.31)
            clo_2_T = clo_2 + I_a / (1 + 1.81 * clo_2)

            body_cover_arr = np.array([body_cover_1, br_sk_c, body_cover_2, 1 - body_cover_1 - body_cover_2 - br_sk_c])
        elif 1.2 < icl <= 1.6:
            icl_catel = 4
            facl = 0.87

            body_cover_1 = 0.35
            body_cover_2 = 0.22
            body_cover_3 = 0.30

            clo_1 = 0.155 * (6.6667 * math.pow(icl, 3) - 26 * math.pow(icl, 2) + 33.933 * icl - 12.27)
            clo_1_T = clo_1 + I_a / (1 + 1.81 * clo_1)

            clo_2 = 0.155 * (6.6667 * math.pow(icl, 3) - 28 * math.pow(icl, 2) + 39.433 * icl - 16.82)
            clo_2_T = clo_2 + I_a / (1 + 1.81 * clo_2)

            clo_3 = 0.155 * (-0.25 * math.pow(icl, 2) + 1.495 * icl - 0.7715)
            clo_3_T = clo_3 + I_a / (1 + 1.81 * clo_3)

            body_cover_arr = np.array([body_cover_1, br_sk_c, body_cover_2, body_cover_3 , 1 - body_cover_1 - body_cover_2 - body_cover_3 - br_sk_c])
        elif 1.6 < icl <= 2.0:
            icl_catel = 5
            facl = 0.93

            body_cover_1 = 0.45
            body_cover_2 = 0.22
            body_cover_3 = 0.26

            clo_1 = 0.155 * (30 * math.pow(icl, 3) - 164 * math.pow(icl, 2) + 299 * icl - 178.93)
            clo_1_T = clo_1 + I_a / (1 + 1.81 * clo_1)

            clo_2 = 0.155 * (0.25 * math.pow(icl, 2) - 0.695 * icl + 2.3895)
            clo_2_T = clo_2 + I_a / (1 + 1.81 * clo_2)

            clo_3 = 0.155 * (-0.25 * math.pow(icl, 2) + 1.875 * icl - 1.4975)
            clo_3_T = clo_3 + I_a / (1 + 1.81 * clo_3)

            body_cover_arr = np.array([body_cover_1, br_sk_c, body_cover_2, body_cover_3, 1 - body_cover_1 - body_cover_2 - body_cover_3 - br_sk_c])
        else:
            icl_catel = 6
            facl = 0.97

            body_cover_1 = 0.55
            body_cover_2 = 0.25
            body_cover_3 = 0.12
            br_sk_1 = 0.05

            clo_1 = 0.155 * (icl + 1.2)
            clo_1_T = clo_1 + I_a / (1 + 1.81 * clo_1)

            clo_2 = 0.155 * (0.5 * icl + 1.05)
            clo_2_T = clo_2 + I_a / (1 + 1.81 * clo_2)

            clo_3 = 0.155 * (0.5 * icl + 0.25)
            clo_3_T = clo_3 + I_a / (1 + 1.81 * clo_3)

            clo_cap = 0.155 * (icl - 1.5)
            clo_cap_T = clo_cap + I_a / (1 + 1.81 * clo_cap)

            body_cover_arr = np.array([body_cover_1, br_sk_c - br_sk_1, body_cover_2, body_cover_3, br_sk_1])
            # end of catelogrizing icl

        return icl_catel, facl, body_cover_1, body_cover_2, body_cover_3, br_sk_1, clo_1, clo_2, clo_3, clo_cap, clo_1_T, clo_2_T, clo_3_T, clo_cap_T, body_cover_arr
    # end of Icl_define


    def Icl_define(icl, I_a_M, br_sk_c): # for I_a_M as changing I_a_M of clothing insulation

        #global icl_catel, facl, body_cover_1, body_cover_2, body_cover_3, br_sk_1, clo_1, clo_2, clo_3, clo_cap, clo_1_T, clo_2_T, clo_3_T, clo_cap_T, body_cover_arr

        body_cover_1 = 0.0
        body_cover_2 = 0.0
        body_cover_3 = 0.0
        br_sk_1 = 0.0
        clo_1 = 0.0
        clo_2 = 0.0
        clo_3 = 0.0
        clo_cap = 0.0
        clo_1_T = 0.0
        clo_2_T = 0.0
        clo_3_T = 0.0
        clo_cap_T = 0.0

        body_cover_arr = np.array([])
        if icl <= 0.6:
            icl_catel = 1
            facl = 0.62

            body_cover_1 = 0.62  # ratio covered by clothing

            clo_1 = icl * 0.155
            clo_1_T = clo_1 + I_a_M[0] / (1 + 1.81 * clo_1)

            body_cover_arr = np.array([body_cover_1, br_sk_c, 1 - body_cover_1 - br_sk_c])
        elif 0.6 < icl and icl <= 0.9:
            icl_catel = 2
            facl = 0.81

            body_cover_1 = 0.45
            body_cover_2 = 0.36

            clo_1 = 0.155 * (0.9 * icl + 0.3733)
            clo_1_T = clo_1 + I_a_M[0] / (1 + 1.81 * clo_1)

            clo_2 = 0.155 * (0.9 * icl - 0.1133)
            clo_2_T = clo_2 + I_a_M[2] / (1 + 1.81 * clo_2)

            body_cover_arr = np.array([body_cover_1, br_sk_c, body_cover_2, 1 - body_cover_1 - body_cover_2 - br_sk_c])
        elif 0.9 < icl and icl <= 1.2:
            icl_catel = 3
            facl = 0.87

            body_cover_1 = 0.45
            body_cover_2 = 0.42

            clo_1 = 0.155 * (-9 * math.pow(icl, 2) + 21 * icl - 10.38)
            clo_1_T = clo_1 + I_a_M[0] / (1 + 1.81 * clo_1)

            clo_2 = 0.155 * (2 * math.pow(icl, 2) - 3.6 * icl + 2.31)
            clo_2_T = clo_2 + I_a_M[2] / (1 + 1.81 * clo_2)

            body_cover_arr = np.array([body_cover_1, br_sk_c, body_cover_2, 1 - body_cover_1 - body_cover_2 - br_sk_c])
        elif 1.2 < icl and icl <= 1.6:
            icl_catel = 4
            facl = 0.87

            body_cover_1 = 0.35
            body_cover_2 = 0.22
            body_cover_3 = 0.30

            clo_1 = 0.155 * (6.6667 * math.pow(icl, 3) - 26 * math.pow(icl, 2) + 33.933 * icl - 12.27)
            clo_1_T = clo_1 + I_a_M[0] / (1 + 1.81 * clo_1)

            clo_2 = 0.155 * (6.6667 * math.pow(icl, 3) - 28 * math.pow(icl, 2) + 39.433 * icl - 16.82)
            clo_2_T = clo_2 + I_a_M[2] / (1 + 1.81 * clo_2)

            clo_3 = 0.155 * (-0.25 * math.pow(icl, 2) + 1.495 * icl - 0.7715)
            clo_3_T = clo_3 + I_a_M[3] / (1 + 1.81 * clo_3)

            body_cover_arr = np.array([body_cover_1, br_sk_c, body_cover_2, body_cover_3,
                                       1 - body_cover_1 - body_cover_2 - body_cover_3 - br_sk_c])
        elif 1.6 < icl <= 2.0:
            icl_catel = 5
            facl = 0.93

            body_cover_1 = 0.45
            body_cover_2 = 0.22
            body_cover_3 = 0.26

            clo_1 = 0.155 * (30 * math.pow(icl, 3) - 164 * math.pow(icl, 2) + 299 * icl - 178.93)
            clo_1_T = clo_1 + I_a_M[0] / (1 + 1.81 * clo_1)

            clo_2 = 0.155 * (0.25 * math.pow(icl, 2) - 0.695 * icl + 2.3895)
            clo_2_T = clo_2 + I_a_M[2] / (1 + 1.81 * clo_2)

            clo_3 = 0.155 * (-0.25 * math.pow(icl, 2) + 1.875 * icl - 1.4975)
            clo_3_T = clo_3 + I_a_M[3] / (1 + 1.81 * clo_3)

            body_cover_arr = np.array([body_cover_1, br_sk_c, body_cover_2, body_cover_3,
                                       1 - body_cover_1 - body_cover_2 - body_cover_3 - br_sk_c])
        else:
            icl_catel = 6
            facl = 0.97

            body_cover_1 = 0.55
            body_cover_2 = 0.25
            body_cover_3 = 0.12
            br_sk_1 = 0.05

            clo_1 = 0.155 * (icl + 1.2)
            clo_1_T = clo_1 + I_a_M[0] / (1 + 1.81 * clo_1)

            clo_2 = 0.155 * (0.5 * icl + 1.05)
            clo_2_T = clo_2 + I_a_M[2] / (1 + 1.81 * clo_2)

            clo_3 = 0.155 * (0.5 * icl + 0.25)
            clo_3_T = clo_3 + I_a_M[3] / (1 + 1.81 * clo_3)

            clo_cap = 0.155 * (icl - 1.5)
            clo_cap_T = clo_cap + I_a_M[4] / (1 + 1.81 * clo_cap)

            body_cover_arr = np.array([body_cover_1, br_sk_c - br_sk_1, body_cover_2, body_cover_3, br_sk_1])

            # end of catelogrizing icl
        return icl_catel, facl, body_cover_1, body_cover_2, body_cover_3, br_sk_1, clo_1, clo_2, clo_3, clo_cap, clo_1_T, clo_2_T, clo_3_T, clo_cap_T, body_cover_arr
    # end of Icl_define

    def initial_body_T(icl_catel, T_core_i, T_sk_i, h, ere, M_w, fat_w, sk_w, br_w, sk_br_w, bl_d, bl_c, time, br_sk_c, br_sk_1, rad_brain, rad_brain_skin, rad_brain_fat, rad_brain_inside, ht_brain, ht_body, rad_body, rad_body_skin, rad_body_fat, rad_body_inside):

        #global T_M_i, T_M_1, Vol, D_M_i, D_M, beta_i, beta, Q_M
        T_M_1 = np.array([])
        # Dedination of blood beta elements
        trunk_b = np.array([
                            [M_w * bl_d * bl_c * time],  # blood energy transfer in different trunk's layers
                            [M_w * bl_d * bl_c * time],
                            [fat_w * bl_d * bl_c * time],
                            [sk_w * bl_d * bl_c * time],
                            [sk_w * bl_d * bl_c * time]
                           ])

        head_b = np.array([[br_w * bl_d * bl_c * time],  # blood energy transfer in different head's layers
                           [br_w * bl_d * bl_c * time],
                           [fat_w * bl_d * bl_c * time],
                           [sk_br_w * bl_d * bl_c * time],
                           [sk_br_w * bl_d * bl_c * time]
                          ])


        if icl_catel == 1:

            T_M_1 = np.array([
                             [T_core_i],  # read out GUI (core temperature1)
                             [T_core_i],  # core temperature 2
                             [(T_core_i + T_sk_i) / 2],  # fat temperature
                             [T_sk_i],  # skin temperature (inside)
                             [T_sk_i],  # skin temperature (outside)
                             [T_core_i],  # read out GUI (brain temperature1)
                             [T_core_i],  # brain temperature 2
                             [(T_core_i + T_sk_i) / 2],  # brain fat temperature
                             [T_sk_i],  # brain skin temperature (inside)
                             [T_sk_i],  # brain skin temperature (outside)
                             [T_core_i - 0.0],  # external muscle temperature1
                             [T_core_i - 0.0],  # external muscle temperature 2
                             [(T_core_i + T_sk_i) / 2 - 0.0],  # external fat temperature
                             [T_sk_i - 0.0],  # external skin temperature (inside)
                             [T_sk_i - 0.0],  # external skin temperature (outside)
                             [0.8 * T_core_i + 0.2 * T_sk_i] # blood temperature
                             ])

            #T_M_i = T_M_1

            Vol = np.array([
                           [math.pi * ht_body * body_cover_1 * (math.pow(rad_body_inside / 2, 2))],
                           # Volume of body covered by clothing #
                           [math.pi * ht_body * body_cover_1 * (
                               math.pow(rad_body_inside, 2) - math.pow(rad_body_inside / 2, 2))],
                           [math.pi * ht_body * body_cover_1 * (
                               math.pow((rad_body_inside + rad_body_fat), 2) - math.pow(rad_body_inside, 2))],
                           [math.pi * ht_body * body_cover_1 * (
                               math.pow((rad_body - rad_body_skin / 2), 2) - math.pow(rad_body_inside + rad_body_fat,
                                                                                      2))],
                           [math.pi * ht_body * body_cover_1 * (
                               math.pow((rad_body), 2) - math.pow(rad_body_inside + rad_body_fat + rad_body_skin / 2,
                                                                  2))],
                           [math.pi * ht_brain * (math.pow(rad_brain_inside / 2, 2))],  # Volume of head #
                           [math.pi * ht_brain * (math.pow(rad_brain_inside, 2) - math.pow(rad_brain_inside / 2, 2))],
                           [math.pi * ht_brain * (
                               math.pow((rad_brain_inside + rad_brain_fat), 2) - math.pow(rad_brain_inside, 2))],
                           [math.pi * ht_brain * (
                               math.pow((rad_brain - rad_brain_skin / 2), 2) - math.pow(
                                   rad_brain_inside + rad_brain_fat,
                                   2))],
                           [math.pi * ht_brain * (
                               math.pow((rad_brain), 2) - math.pow(
                                   rad_brain_inside + rad_brain_fat + rad_brain_skin / 2,
                                   2))],
                           [math.pi * ht_body * (1 - body_cover_1 - br_sk_c) * (math.pow(rad_body_inside / 2, 2))],
                           # Volume of body uncovered by clothing #
                           [math.pi * ht_body * (1 - body_cover_1 - br_sk_c) * (
                               math.pow(rad_body_inside, 2) - math.pow(rad_body_inside / 2, 2))],
                           [math.pi * ht_body * (1 - body_cover_1 - br_sk_c) * (
                               math.pow((rad_body_inside + rad_body_fat), 2) - math.pow(rad_body_inside, 2))],
                           [math.pi * ht_body * (1 - body_cover_1 - br_sk_c) * (
                               math.pow((rad_body - rad_body_skin / 2), 2) - math.pow(rad_body_inside + rad_body_fat,
                                                                                      2))],
                           [math.pi * ht_body * (1 - body_cover_1 - br_sk_c) * (
                               math.pow((rad_body), 2) - math.pow(rad_body_inside + rad_body_fat + rad_body_skin / 2,
                                                                  2))]
                           ])

            D_M = np.array([
                           ((684.0 * 2 + h / (Vol[0] + Vol[1] + Vol[5] + Vol[6] + Vol[10] + Vol[11]) - ere / (
                               Vol[0] + Vol[1])) * time),
                           ((684.0 * 2 + h / (Vol[0] + Vol[1] + Vol[5] + Vol[6] + Vol[10] + Vol[11]) - ere / (
                               Vol[0] + Vol[1])) * time),
                           [58.0 * 2 * time],
                           [368.0 * 2 * time],
                           [368.0 * 2 * time],
                           ((13400.0 * 2 + h / (Vol[0] + Vol[1] + Vol[5] + Vol[6] + Vol[10] + Vol[11])) * time),
                           ((13400.0 * 2 + h / (Vol[0] + Vol[1] + Vol[5] + Vol[6] + Vol[10] + Vol[11])) * time),
                           [58.0 * 2 * time],
                           [368.0 * 2 * time],
                           [368.0 * 2 * time],
                           ((684.0 * 2 + h / (Vol[0] + Vol[1] + Vol[5] + Vol[6] + Vol[10] + Vol[11])) * time),
                           ((684.0 * 2 + h / (Vol[0] + Vol[1] + Vol[5] + Vol[6] + Vol[10] + Vol[11])) * time),
                           [58.0 * 2 * time],
                           [368.0 * 2 * time],
                           [368.0 * 2 * time]
                           ])

            Q_M = np.array([
                [0.0],
                [684.0],
                [58.0],
                [368.0],
                [368.0],
                [13400.0],
                [13400.0],
                [58.0],
                [368.0],
                [368.0],
                [684.0],
                [684.0],
                [58.0],
                [368.0],
                [368.0]
            ])

            beta = np.vstack((trunk_b, head_b, trunk_b))


        if icl_catel == 2 or icl_catel == 3:

            T_M_1 = np.array([
                             [T_core_i],  # read out GUI (core temperature1)
                             [T_core_i],  # core temperature 2
                             [(T_core_i + T_sk_i) / 2],  # fat temperature
                             [T_sk_i],  # skin temperature (inside)
                             [T_sk_i],  # skin temperature (outside)
                             [T_core_i],  # read out GUI (brain temperature1)
                             [T_core_i],  # brain temperature 2
                             [(T_core_i + T_sk_i) / 2],  # brain fat temperature
                             [T_sk_i],  # brain skin temperature (inside)
                             [T_sk_i],  # brain skin temperature (outside)
                             [T_core_i - 0.0],  # 1 layer muscle temperature1
                             [T_core_i - 0.0],  # 1 layer muscle temperature 2
                             [(T_core_i + T_sk_i) / 2 - 0.0],  # 1 layer fat temperature
                             [T_sk_i - 0.0],  # 1 layer skin temperature (inside)
                             [T_sk_i - 0.0],  # 1 layer skin temperature (outside)
                             [T_core_i - 0.0],  # external muscle temperature1
                             [T_core_i - 0.0],  # external muscle temperature 2
                             [(T_core_i + T_sk_i) / 2 - 0.0],  # external fat temperature
                             [T_sk_i - 0.0],  # external skin temperature (inside)
                             [T_sk_i - 0.0],  # external skin temperature (outside)
                             [0.8 * T_core_i + 0.2 * T_sk_i]# blood temperature
                             ])

            #T_M_i = T_M_1

            Vol = np.array([
                           [math.pi * ht_body * body_cover_1 * (math.pow(rad_body_inside / 2, 2))],
                           # Volume of body covered by 2 layer clothing
                           [math.pi * ht_body * body_cover_1 * (
                               math.pow(rad_body_inside, 2) - math.pow(rad_body_inside / 2, 2))],
                           [math.pi * ht_body * body_cover_1 * (
                               math.pow((rad_body_inside + rad_body_fat), 2) - math.pow(rad_body_inside, 2))],
                           [math.pi * ht_body * body_cover_1 * (
                               math.pow((rad_body - rad_body_skin / 2), 2) - math.pow(rad_body_inside + rad_body_fat,
                                                                                      2))],
                           [math.pi * ht_body * body_cover_1 * (
                               math.pow((rad_body), 2) - math.pow(rad_body_inside + rad_body_fat + rad_body_skin / 2,
                                                                  2))],
                           [math.pi * ht_brain * (math.pow(rad_brain_inside / 2, 2))],  # Volume of head
                           [math.pi * ht_brain * (math.pow(rad_brain_inside, 2) - math.pow(rad_brain_inside / 2, 2))],
                           [math.pi * ht_brain * (
                               math.pow((rad_brain_inside + rad_brain_fat), 2) - math.pow(rad_brain_inside, 2))],
                           [math.pi * ht_brain * (
                               math.pow((rad_brain - rad_brain_skin / 2), 2) - math.pow(
                                   rad_brain_inside + rad_brain_fat,
                                   2))],
                           [math.pi * ht_brain * (
                               math.pow((rad_brain), 2) - math.pow(
                                   rad_brain_inside + rad_brain_fat + rad_brain_skin / 2,
                                   2))],
                           [math.pi * ht_body * body_cover_2 * (math.pow(rad_body_inside / 2, 2))],
                           # Volume of body covered by 1 layer clothing
                           [math.pi * ht_body * body_cover_2 * (
                               math.pow(rad_body_inside, 2) - math.pow(rad_body_inside / 2, 2))],
                           [math.pi * ht_body * body_cover_2 * (
                               math.pow((rad_body_inside + rad_body_fat), 2) - math.pow(rad_body_inside, 2))],
                           [math.pi * ht_body * body_cover_2 * (
                               math.pow((rad_body - rad_body_skin / 2), 2) - math.pow(rad_body_inside + rad_body_fat,
                                                                                      2))],
                           [math.pi * ht_body * body_cover_2 * (
                               math.pow((rad_body), 2) - math.pow(rad_body_inside + rad_body_fat + rad_body_skin / 2,
                                                                  2))],
                           [math.pi * ht_body * (1 - body_cover_1 - body_cover_2 - br_sk_c) * (
                               math.pow(rad_body_inside / 2, 2))],  # Volume of nude body
                           [math.pi * ht_body * (1 - body_cover_1 - body_cover_2 - br_sk_c) * (
                               math.pow(rad_body_inside, 2) - math.pow(rad_body_inside / 2, 2))],
                           [math.pi * ht_body * (1 - body_cover_1 - body_cover_2 - br_sk_c) * (
                               math.pow((rad_body_inside + rad_body_fat), 2) - math.pow(rad_body_inside, 2))],
                           [math.pi * ht_body * (1 - body_cover_1 - body_cover_2 - br_sk_c) * (
                               math.pow((rad_body - rad_body_skin / 2), 2) - math.pow(rad_body_inside + rad_body_fat,
                                                                                      2))],
                           [math.pi * ht_body * (1 - body_cover_1 - body_cover_2 - br_sk_c) * (
                               math.pow((rad_body), 2) - math.pow(rad_body_inside + rad_body_fat + rad_body_skin / 2,
                                                                  2))]
                           ])

            D_M = np.array([
                           ((684.0 * 2 + h / (
                            Vol[0] + Vol[1] + Vol[5] + Vol[6] + Vol[10] + Vol[11] + Vol[15] + Vol[16]) - ere / (
                                 Vol[0] + Vol[1])) * time),
                           ((684.0 * 2 + h / (
                               Vol[0] + Vol[1] + Vol[5] + Vol[6] + Vol[10] + Vol[11] + Vol[15] + Vol[16]) - ere / (
                                 Vol[0] + Vol[1])) * time),
                           [58.0 * 2 * time],
                           [368.0 * 2 * time],
                           [368.0 * 2 * time],
                           ((13400.0 * 2 + h / (
                               Vol[0] + Vol[1] + Vol[5] + Vol[6] + Vol[10] + Vol[11] + Vol[15] + Vol[16])) * time),
                           ((13400.0 * 2 + h / (
                               Vol[0] + Vol[1] + Vol[5] + Vol[6] + Vol[10] + Vol[11] + Vol[15] + Vol[16])) * time),
                           [58.0 * 2 * time],
                           [368.0 * 2 * time],
                           [368.0 * 2 * time],
                           ((684.0 * 2 + h / (
                               Vol[0] + Vol[1] + Vol[5] + Vol[6] + Vol[10] + Vol[11] + Vol[15] + Vol[16])) * time),
                           ((684.0 * 2 + h / (
                               Vol[0] + Vol[1] + Vol[5] + Vol[6] + Vol[10] + Vol[11] + Vol[15] + Vol[16])) * time),
                           [58.0 * 2 * time],
                           [368.0 * 2 * time],
                           [368.0 * 2 * time],
                           ((684.0 * 2 + h / (
                               Vol[0] + Vol[1] + Vol[5] + Vol[6] + Vol[10] + Vol[11] + Vol[15] + Vol[16])) * time),
                           ((684.0 * 2 + h / (
                               Vol[0] + Vol[1] + Vol[5] + Vol[6] + Vol[10] + Vol[11] + Vol[15] + Vol[16])) * time),
                           [58.0 * 2 * time],
                           [368.0 * 2 * time],
                           [368.0 * 2 * time]
                           ])
            #D_M_i = D_M
            Q_M = np.array([
                           [0.0],
                           [684.0 ],
                           [58.0],
                           [368.0],
                           [368.0],
                           [13400.0],
                           [13400.0],
                           [58.0],
                           [368.0],
                           [368.0],
                           [684.0],
                           [684.0],
                           [58.0],
                           [368.0],
                           [368.0],
                           [684.0],
                           [684.0],
                           [58.0],
                           [368.0],
                           [368.0]
                           ])

            beta = np.vstack((trunk_b, head_b, trunk_b, trunk_b))

            #beta_i = beta

        if icl_catel == 4 or icl_catel == 5:

            T_M_1 = np.array([
                             [T_core_i],  # read out GUI (core temperature1)
                             [T_core_i],  # core temperature 2
                             [(T_core_i + T_sk_i) / 2],  # fat temperature
                             [T_sk_i],  # skin temperature (inside)
                             [T_sk_i],  # skin temperature (outside)
                             [T_core_i],  # read out GUI (brain temperature1)
                             [T_core_i],  # brain temperature 2
                             [(T_core_i + T_sk_i) / 2],  # brain fat temperature
                             [T_sk_i],  # brain skin temperature (inside)
                             [T_sk_i],  # brain skin temperature (outside)
                             [T_core_i - 0.0],  # 2 layer muscle temperature1
                             [T_core_i - 0.0],  # 2 layer muscle temperature 2
                             [(T_core_i + T_sk_i) / 2 - 0.0],  # 2 layer fat temperature
                             [T_sk_i - 0.0],  # 2 layer skin temperature (inside)
                             [T_sk_i - 0.0],  # 2 layer skin temperature (outside)
                             [T_core_i - 0.0],  # 1 layer muscle temperature1
                             [T_core_i - 0.0],  # 1 layer muscle temperature 2
                             [(T_core_i + T_sk_i) / 2 - 0.0],  # 1 layer fat temperature
                             [T_sk_i - 0.0],  # 1 layer skin temperature (inside)
                             [T_sk_i - 0.0],  # 1 layer skin temperature (outside)
                             [T_core_i - 0.0],  # external muscle temperature1
                             [T_core_i - 0.0],  # external muscle temperature 2
                             [(T_core_i + T_sk_i) / 2 - 0.0],  # external fat temperature
                             [T_sk_i - 0.0],  # external skin temperature (inside)
                             [T_sk_i - 0.0],  # external skin temperature (outside)
                             [0.8 * T_core_i + 0.2 * T_sk_i] # blood temperature
                             ])

            Vol = np.array([
                           [math.pi*ht_body*body_cover_1*(math.pow(rad_body_inside/2,2))], # Volume of body covered by 3 layer clothing
                           [math.pi*ht_body*body_cover_1*(math.pow(rad_body_inside,2)-math.pow(rad_body_inside/2,2))],
                           [math.pi*ht_body*body_cover_1*(math.pow((rad_body_inside+rad_body_fat),2)-math.pow(rad_body_inside,2))],
                           [math.pi*ht_body*body_cover_1*(math.pow((rad_body - rad_body_skin/2),2)-math.pow(rad_body_inside+rad_body_fat,2))],
                           [math.pi*ht_body*body_cover_1*(math.pow((rad_body),2)-math.pow(rad_body_inside+rad_body_fat+rad_body_skin/2,2))],
                           [math.pi*ht_brain*(math.pow(rad_brain_inside/2,2))], # Volume of head
                           [math.pi*ht_brain*(math.pow(rad_brain_inside,2)-math.pow(rad_brain_inside/2,2))],
                           [math.pi*ht_brain*(math.pow((rad_brain_inside+rad_brain_fat),2)-math.pow(rad_brain_inside,2))],
                           [math.pi*ht_brain*(math.pow((rad_brain - rad_brain_skin/2),2)-math.pow(rad_brain_inside+rad_brain_fat,2))],
                           [math.pi*ht_brain*(math.pow((rad_brain),2)-math.pow(rad_brain_inside+rad_brain_fat+rad_brain_skin/2,2))],
                           [math.pi*ht_body*body_cover_2*(math.pow(rad_body_inside/2,2))], # Volume of body covered by 2 layer clothing
                           [math.pi*ht_body*body_cover_2*(math.pow(rad_body_inside,2)-math.pow(rad_body_inside/2,2))],
                           [math.pi*ht_body*body_cover_2*(math.pow((rad_body_inside+rad_body_fat),2)-math.pow(rad_body_inside,2))],
                           [math.pi*ht_body*body_cover_2*(math.pow((rad_body - rad_body_skin/2),2)-math.pow(rad_body_inside+rad_body_fat,2))],
                           [math.pi*ht_body*body_cover_2*(math.pow((rad_body),2)-math.pow(rad_body_inside+rad_body_fat+rad_body_skin/2,2))],
                           [math.pi*ht_body*body_cover_3*(math.pow(rad_body_inside/2,2))], # Volume of body covered by 1 layer clothing
                           [math.pi*ht_body*body_cover_3*(math.pow(rad_body_inside,2)-math.pow(rad_body_inside/2,2))],
                           [math.pi*ht_body*body_cover_3*(math.pow((rad_body_inside+rad_body_fat),2)-math.pow(rad_body_inside,2))],
                           [math.pi*ht_body*body_cover_3*(math.pow((rad_body - rad_body_skin/2),2)-math.pow(rad_body_inside+rad_body_fat,2))],
                           [math.pi*ht_body*body_cover_3*(math.pow((rad_body),2)-math.pow(rad_body_inside+rad_body_fat+rad_body_skin/2,2))],
                           [math.pi*ht_body*(1-body_cover_1-body_cover_2-body_cover_3-br_sk_c)*(math.pow(rad_body_inside/2,2))], # Volume of nude body
                           [math.pi*ht_body*(1-body_cover_1-body_cover_2-body_cover_3-br_sk_c)*(math.pow(rad_body_inside,2)-math.pow(rad_body_inside/2,2))],
                           [math.pi*ht_body*(1-body_cover_1-body_cover_2-body_cover_3-br_sk_c)*(math.pow((rad_body_inside+rad_body_fat),2)-math.pow(rad_body_inside,2))],
                           [math.pi*ht_body*(1-body_cover_1-body_cover_2-body_cover_3-br_sk_c)*(math.pow((rad_body - rad_body_skin/2),2)-math.pow(rad_body_inside+rad_body_fat,2))],
                           [math.pi*ht_body*(1-body_cover_1-body_cover_2-body_cover_3-br_sk_c)*(math.pow((rad_body),2)-math.pow(rad_body_inside+rad_body_fat+rad_body_skin/2,2))]
                           ])

            D_M = np.array([
                           ((684.0*2+h/(Vol[0]+Vol[1]+Vol[5]+Vol[6]+Vol[10]+Vol[11]+Vol[15]+Vol[16]+Vol[20]+Vol[21])-ere/(Vol[0]+Vol[1]))*time),
                           ((684.0*2+h/(Vol[0]+Vol[1]+Vol[5]+Vol[6]+Vol[10]+Vol[11]+Vol[15]+Vol[16]+Vol[20]+Vol[21])-ere/(Vol[0]+Vol[1]))*time),
                           [58.0*2*time],
                           [368.0*2*time],
                           [368.0*2*time],
                           ((13400.0*2+h/(Vol[0]+Vol[1]+Vol[5]+Vol[6]+Vol[10]+Vol[11]+Vol[15]+Vol[16]+Vol[20]+Vol[21]))*time),
                           ((13400.0*2+h/(Vol[0]+Vol[1]+Vol[5]+Vol[6]+Vol[10]+Vol[11]+Vol[15]+Vol[16]+Vol[20]+Vol[21]))*time),
                           [58.0*2*time],
                           [368.0*2*time],
                           [368.0*2*time],
                           ((684.0*2+h/(Vol[0]+Vol[1]+Vol[5]+Vol[6]+Vol[10]+Vol[11]+Vol[15]+Vol[16]+Vol[20]+Vol[21]))*time),
                           ((684.0*2+h/(Vol[0]+Vol[1]+Vol[5]+Vol[6]+Vol[10]+Vol[11]+Vol[15]+Vol[16]+Vol[20]+Vol[21]))*time),
                           [58.0*2*time],
                           [368.0*2*time],
                           [368.0*2*time],
                           ((684.0*2+h/(Vol[0]+Vol[1]+Vol[5]+Vol[6]+Vol[10]+Vol[11]+Vol[15]+Vol[16]+Vol[20]+Vol[21]))*time),
                           ((684.0*2+h/(Vol[0]+Vol[1]+Vol[5]+Vol[6]+Vol[10]+Vol[11]+Vol[15]+Vol[16]+Vol[20]+Vol[21]))*time),
                           [58.0*2*time],
                           [368.0*2*time],
                           [368.0*2*time],
                           ((684.0*2+h/(Vol[0]+Vol[1]+Vol[5]+Vol[6]+Vol[10]+Vol[11]+Vol[15]+Vol[16]+Vol[20]+Vol[21]))*time),
                           ((684.0*2+h/(Vol[0]+Vol[1]+Vol[5]+Vol[6]+Vol[10]+Vol[11]+Vol[15]+Vol[16]+Vol[20]+Vol[21]))*time),
                           [58.0*2*time],
                           [368.0*2*time],
                           [368.0*2*time]
                           ])

            #D_M_i = D_M
            Q_M = np.array([
                [0.0],
                [684.0],
                [58.0],
                [368.0],
                [368.0],
                [13400.0],
                [13400.0],
                [58.0],
                [368.0],
                [368.0],
                [684.0],
                [684.0],
                [58.0],
                [368.0],
                [368.0],
                [684.0],
                [684.0],
                [58.0],
                [368.0],
                [368.0],
                [684.0],
                [684.0],
                [58.0],
                [368.0],
                [368.0]
            ])

            beta = np.vstack((trunk_b, head_b, trunk_b, trunk_b, trunk_b))

            #beta_i = beta

        if icl_catel == 6:

            T_M_1 = np.array([
                             [T_core_i],  # read out GUI (core temperature1)
                             [T_core_i],  # core temperature 2
                             [(T_core_i + T_sk_i) / 2],  # fat temperature
                             [T_sk_i],  # skin temperature (inside)
                             [T_sk_i],  # skin temperature (outside)
                             [T_core_i],  # read out GUI (brain temperature1)
                             [T_core_i],  # brain temperature 2
                             [(T_core_i + T_sk_i) / 2],  # brain fat temperature
                             [T_sk_i],  # brain skin temperature (inside)
                             [T_sk_i],  # brain skin temperature (outside)
                             [T_core_i - 0.0],  # 2 layer muscle temperature1
                             [T_core_i - 0.0],  # 2 layer muscle temperature 2
                             [(T_core_i + T_sk_i) / 2 - 0.0],  # 2 layer fat temperature
                             [T_sk_i - 0.0],  # 2 layer skin temperature (inside)
                             [T_sk_i - 0.0],  # 2 layer skin temperature (outside)
                             [T_core_i - 0.0],  # 1 layer muscle temperature1
                             [T_core_i - 0.0],  # 1 layer muscle temperature 2
                             [(T_core_i + T_sk_i) / 2 - 0.0],  # 1 layer fat temperature
                             [T_sk_i - 0.0],  # 1 layer skin temperature (inside)
                             [T_sk_i - 0.0],  # 1 layer skin temperature (outside)
                             [T_core_i - 0.0],  # cap brain temperature1
                             [T_core_i - 0.0],  # cap brain temperature 2
                             [(T_core_i + T_sk_i) / 2 - 0.0],  # cap fat temperature
                             [T_sk_i - 0.0],  # cap skin temperature (inside)
                             [T_sk_i - 0.0],  # cap skin temperature (outside)
                             [0.8 * T_core_i + 0.2 * T_sk_i] # blood temperature
                             ])

            #T_M_i = T_M_1

            Vol = np.array([
                           [math.pi*ht_body*body_cover_1*(math.pow(rad_body_inside/2,2))], # Volume of body covered by 3 layer clothing
                           [math.pi*ht_body*body_cover_1*(math.pow(rad_body_inside,2)-math.pow(rad_body_inside/2,2))],
                           [math.pi*ht_body*body_cover_1*(math.pow((rad_body_inside+rad_body_fat),2)-math.pow(rad_body_inside,2))],
                           [math.pi*ht_body*body_cover_1*(math.pow((rad_body - rad_body_skin/2),2)-math.pow(rad_body_inside+rad_body_fat,2))],
                           [math.pi*ht_body*body_cover_1*(math.pow((rad_body),2)-math.pow(rad_body_inside+rad_body_fat+rad_body_skin/2,2))],
                           [math.pi*ht_brain*(math.pow(rad_brain_inside/2,2))*((br_sk_c-br_sk_1)/br_sk_c)], # Volume of head
                           [math.pi*ht_brain*(math.pow(rad_brain_inside,2)-math.pow(rad_brain_inside/2,2))*((br_sk_c-br_sk_1)/br_sk_c)],
                           [math.pi*ht_brain*(math.pow((rad_brain_inside+rad_brain_fat),2)-math.pow(rad_brain_inside,2))*((br_sk_c-br_sk_1)/br_sk_c)],
                           [math.pi*ht_brain*(math.pow((rad_brain - rad_brain_skin/2),2)-math.pow(rad_brain_inside+rad_brain_fat,2))*((br_sk_c-br_sk_1)/br_sk_c)],
                           [math.pi*ht_brain*(math.pow((rad_brain),2)-math.pow(rad_brain_inside+rad_brain_fat+rad_brain_skin/2,2))*((br_sk_c-br_sk_1)/br_sk_c)],
                           [math.pi*ht_body*body_cover_2*(math.pow(rad_body_inside/2,2))], # Volume of body covered by 2 layer clothing
                           [math.pi*ht_body*body_cover_2*(math.pow(rad_body_inside,2)-math.pow(rad_body_inside/2,2))],
                           [math.pi*ht_body*body_cover_2*(math.pow((rad_body_inside+rad_body_fat),2)-math.pow(rad_body_inside,2))],
                           [math.pi*ht_body*body_cover_2*(math.pow((rad_body - rad_body_skin/2),2)-math.pow(rad_body_inside+rad_body_fat,2))],
                           [math.pi*ht_body*body_cover_2*(math.pow((rad_body),2)-math.pow(rad_body_inside+rad_body_fat+rad_body_skin/2,2))],
                           [math.pi*ht_body*body_cover_3*(math.pow(rad_body_inside/2,2))], # Volume of body covered by 1 layer clothing
                           [math.pi*ht_body*body_cover_3*(math.pow(rad_body_inside,2)-math.pow(rad_body_inside/2,2))],
                           [math.pi*ht_body*body_cover_3*(math.pow((rad_body_inside+rad_body_fat),2)-math.pow(rad_body_inside,2))],
                           [math.pi*ht_body*body_cover_3*(math.pow((rad_body - rad_body_skin/2),2)-math.pow(rad_body_inside+rad_body_fat,2))],
                           [math.pi*ht_body*body_cover_3*(math.pow((rad_body),2)-math.pow(rad_body_inside+rad_body_fat+rad_body_skin/2,2))],
                           [math.pi*ht_brain*(math.pow(rad_brain_inside/2,2))*(br_sk_1/br_sk_c)], # Volume of head covered by cap
                           [math.pi*ht_brain*(math.pow(rad_brain_inside,2)-math.pow(rad_brain_inside/2,2))*(br_sk_1/br_sk_c)],
                           [math.pi*ht_brain*(math.pow((rad_brain_inside+rad_brain_fat),2)-math.pow(rad_brain_inside,2))*(br_sk_1/br_sk_c)],
                           [math.pi*ht_brain*(math.pow((rad_brain - rad_brain_skin/2),2)-math.pow(rad_brain_inside+rad_brain_fat,2))*(br_sk_1/br_sk_c)],
                           [math.pi*ht_brain*(math.pow((rad_brain),2)-math.pow(rad_brain_inside+rad_brain_fat+rad_brain_skin/2,2))*(br_sk_1/br_sk_c)]
                           ])

            D_M = np.array([
                           ((684.0*2+h/(Vol[0]+Vol[1]+Vol[5]+Vol[6]+Vol[10]+Vol[11]+Vol[15]+Vol[16]+Vol[20]+Vol[21])-ere/(Vol[0]+Vol[1]))*time),
                           ((684.0*2+h/(Vol[0]+Vol[1]+Vol[5]+Vol[6]+Vol[10]+Vol[11]+Vol[15]+Vol[16]+Vol[20]+Vol[21])-ere/(Vol[0]+Vol[1]))*time),
                           [58.0*2*time],
                           [368.0*2*time],
                           [368.0*2*time],
                           ((13400.0*2+h/(Vol[0]+Vol[1]+Vol[5]+Vol[6]+Vol[10]+Vol[11]+Vol[15]+Vol[16]+Vol[20]+Vol[21]))*time),
                           ((13400.0*2+h/(Vol[0]+Vol[1]+Vol[5]+Vol[6]+Vol[10]+Vol[11]+Vol[15]+Vol[16]+Vol[20]+Vol[21]))*time),
                           [58.0*2*time],
                           [368.0*2*time],
                           [368.0*2*time],
                           ((684.0*2+h/(Vol[0]+Vol[1]+Vol[5]+Vol[6]+Vol[10]+Vol[11]+Vol[15]+Vol[16]+Vol[20]+Vol[21]))*time),
                           ((684.0*2+h/(Vol[0]+Vol[1]+Vol[5]+Vol[6]+Vol[10]+Vol[11]+Vol[15]+Vol[16]+Vol[20]+Vol[21]))*time),
                           [58.0*2*time],
                           [368.0*2*time],
                           [368.0*2*time],
                           ((684.0*2+h/(Vol[0]+Vol[1]+Vol[5]+Vol[6]+Vol[10]+Vol[11]+Vol[15]+Vol[16]+Vol[20]+Vol[21]))*time),
                           ((684.0*2+h/(Vol[0]+Vol[1]+Vol[5]+Vol[6]+Vol[10]+Vol[11]+Vol[15]+Vol[16]+Vol[20]+Vol[21]))*time),
                           [58.0*2*time],
                           [368.0*2*time],
                           [368.0*2*time],
                           ((13400.0*2+h/(Vol[0]+Vol[1]+Vol[5]+Vol[6]+Vol[10]+Vol[11]+Vol[15]+Vol[16]+Vol[20]+Vol[21]))*time),
                           ((13400.0*2+h/(Vol[0]+Vol[1]+Vol[5]+Vol[6]+Vol[10]+Vol[11]+Vol[15]+Vol[16]+Vol[20]+Vol[21]))*time),
                           [58.0*2*time],
                           [368.0*2*time],
                           [368.0*2*time]
                           ])
            #D_M_i = D_M
            Q_M = np.array([
                [0.0],
                [684.0],
                [58.0],
                [368.0],
                [368.0],
                [13400.0],
                [13400.0],
                [58.0],
                [368.0],
                [368.0],
                [684.0],
                [684.0],
                [58.0],
                [368.0],
                [368.0],
                [684.0],
                [684.0],
                [58.0],
                [368.0],
                [368.0],
                [13400.0],
                [13400.0],
                [58.0],
                [368.0],
                [368.0]
            ])

            beta = np.vstack((trunk_b, head_b, trunk_b, trunk_b, head_b))

            #beta_i = beta
        return T_M_1, Vol, D_M, beta, Q_M
    # end of initial_body_T

    def set_CC_Mat(icl_catel, beta, Vol, M_k, M_d, M_c, fat_k, fat_d, fat_c, sk_k, sk_d, sk_c, br_k, br_c, br_d, rad_brain, rad_brain_skin, rad_brain_fat, rad_brain_inside, rad_body, rad_body_skin, rad_body_fat, rad_body_inside):

        #global CC_M_1, CC_M_2, T_boundary, T_cl_in

        # Dedination of conductive elements

        trunk_CC_1 = np.array([
                               [2 * M_d * M_c / time - 2 * M_k / math.pow((rad_body_inside / 2), 2), M_k / math.pow(rad_body_inside / 2, 2) + M_k / (2 * (rad_body_inside / 2) * (rad_body_inside / 2)), 0.0, 0.0, 0.0],
                               [M_k / math.pow((rad_body_inside / 2), 2) - M_k / (2 * (rad_body_inside / 2) * (rad_body_inside)), 2 * M_d * M_c / time - 2 * M_k / math.pow((rad_body_inside / 2), 2), M_k / math.pow((rad_body_inside / 2), 2) + M_k / (2 * (rad_body_inside / 2) * (rad_body_inside)), 0.0, 0.0],
                               [0.0, fat_k / math.pow((rad_body_fat), 2) - fat_k / (2 * (rad_body_fat) * (rad_body_inside + rad_body_fat)), 2 * fat_d * fat_c / time - 2 * fat_k / math.pow((rad_body_fat), 2), fat_k / math.pow((rad_body_fat), 2) + fat_k / (2 * (rad_body_fat) * (rad_body_inside + rad_body_fat)), 0.0],
                               [0.0, 0.0, sk_k / math.pow((rad_body_skin / 2), 2) - sk_k / ( 2 * (rad_body_skin / 2) * (rad_body_inside + rad_body_fat + rad_body_skin / 2)), 2 * sk_d * sk_c / time - 2 * sk_k / math.pow((rad_body_skin / 2), 2), sk_k / math.pow((rad_body_skin / 2), 2) + sk_k / ( 2 * (rad_body_skin / 2) * (rad_body_inside + rad_body_fat + rad_body_skin / 2))],
                               [0.0, 0.0, 0.0, sk_k / math.pow((rad_body_skin / 2), 2) - sk_k / ( 2 * (rad_body_skin / 2) * (rad_body_inside + rad_body_fat + rad_body_skin)), 2 * sk_d * sk_c / time - 2 * sk_k / math.pow((rad_body_skin / 2), 2)]])

        head_CC_1 = np.array([
                              [2*br_d*br_c/time-2*br_k/math.pow((rad_brain_inside/2),2), br_k/math.pow(rad_brain_inside/2,2)+br_k/(2*(rad_brain_inside/2)*(rad_brain_inside/2)), 0.0, 0.0, 0.0],
                              [br_k/math.pow((rad_brain_inside/2),2)-br_k/(2*(rad_brain_inside/2)*(rad_brain_inside)), 2*br_d*br_c/time-2*M_k/math.pow((rad_brain_inside/2),2), br_k/math.pow((rad_brain_inside/2),2)+br_k/(2*(rad_brain_inside/2)*(rad_brain_inside)), 0.0, 0.0],
                              [0.0, fat_k/math.pow((rad_brain_fat),2)-fat_k/(2*(rad_brain_fat)*(rad_brain_inside+rad_brain_fat)), 2*fat_d*fat_c/time-2*fat_k/math.pow((rad_brain_fat),2), fat_k/math.pow((rad_brain_fat),2)+fat_k/(2*(rad_brain_fat)*(rad_brain_inside+rad_brain_fat)), 0.0],
                              [0.0, 0.0, sk_k/math.pow((rad_brain_skin/2),2)-sk_k/(2*(rad_brain_skin/2)*(rad_brain_inside+rad_brain_fat+rad_brain_skin/2)), 2*sk_d*sk_c/time-2*sk_k/math.pow((rad_brain_skin/2),2), sk_k/math.pow((rad_brain_skin/2),2)+sk_k/(2*(rad_brain_skin/2)*(rad_brain_inside+rad_brain_fat+rad_brain_skin/2))],
                              [0.0, 0.0, 0.0, sk_k/math.pow((rad_brain_skin/2),2)-sk_k/(2*(rad_brain_skin/2)*(rad_brain_inside+rad_brain_fat+rad_brain_skin)), 2*sk_d*sk_c/time-2*sk_k/math.pow((rad_brain_skin/2),2)]
                             ])

        trunk_CC_2 = np.array([
                               [2*M_d*M_c/time + 2*M_k/math.pow((rad_body_inside/2),2), - M_k/math.pow(rad_body_inside/2,2) - M_k/(2*(rad_body_inside/2)*(rad_body_inside/2)), 0.0, 0.0, 0.0],
                               [- M_k/math.pow((rad_body_inside/2),2) + M_k/(2*(rad_body_inside/2)*(rad_body_inside)), 2*M_d*M_c/time + 2*M_k/math.pow((rad_body_inside/2),2), - M_k/math.pow((rad_body_inside/2),2) - M_k/(2*(rad_body_inside/2)*(rad_body_inside)), 0.0, 0.0],
                               [0.0, - fat_k/math.pow((rad_body_fat),2) + fat_k/(2*(rad_body_fat)*(rad_body_inside+rad_body_fat)), 2*fat_d*fat_c/time + 2*fat_k/math.pow((rad_body_fat),2), - fat_k/math.pow((rad_body_fat),2) - fat_k/(2*(rad_body_fat)*(rad_body_inside+rad_body_fat)), 0.0],
                               [0.0, 0.0, - sk_k/math.pow((rad_body_skin/2),2) + sk_k/(2*(rad_body_skin/2)*(rad_body_inside+rad_body_fat+rad_body_skin/2)), 2*sk_d*sk_c/time + 2*sk_k/math.pow((rad_body_skin/2),2), - sk_k/math.pow((rad_body_skin/2),2) - sk_k/(2*(rad_body_skin/2)*(rad_body_inside+rad_body_fat+rad_body_skin/2))],
                               [0.0, 0.0, 0.0, - sk_k/math.pow((rad_body_skin/2),2) + sk_k/(2*(rad_body_skin/2)*(rad_body_inside+rad_body_fat+rad_body_skin)), 2*sk_d*sk_c/time + 2*sk_k/math.pow((rad_body_skin/2),2)]
                              ])

        head_CC_2 = np.array([
                              [2*br_d*br_c/time + 2*br_k/math.pow((rad_brain_inside/2),2), - br_k/math.pow(rad_brain_inside/2,2) - br_k/(2*(rad_brain_inside/2)*(rad_brain_inside/2)), 0.0, 0.0, 0.0],
                              [- br_k/math.pow((rad_brain_inside/2),2) + br_k/(2*(rad_brain_inside/2)*(rad_brain_inside)), 2*br_d*br_c/time + 2*M_k/math.pow((rad_brain_inside/2),2), - br_k/math.pow((rad_brain_inside/2),2) - br_k/(2*(rad_brain_inside/2)*(rad_brain_inside)), 0.0, 0.0],
                              [0.0, - fat_k/math.pow((rad_brain_fat),2) + fat_k/(2*(rad_brain_fat)*(rad_brain_inside+rad_brain_fat)), 2*fat_d*fat_c/time + 2*fat_k/math.pow((rad_brain_fat),2), - fat_k/math.pow((rad_brain_fat),2) - fat_k/(2*(rad_brain_fat)*(rad_brain_inside+rad_brain_fat)), 0.0],
                              [0.0, 0.0, - sk_k/math.pow((rad_brain_skin/2),2) + sk_k/(2*(rad_brain_skin/2)*(rad_brain_inside+rad_brain_fat+rad_brain_skin/2)), 2*sk_d*sk_c/time + 2*sk_k/math.pow((rad_brain_skin/2),2), - sk_k/math.pow((rad_brain_skin/2),2) - sk_k/(2*(rad_brain_skin/2)*(rad_brain_inside+rad_brain_fat+rad_brain_skin/2))],
                              [0.0, 0.0, 0.0, - sk_k/math.pow((rad_brain_skin/2),2) + sk_k/(2*(rad_brain_skin/2)*(rad_brain_inside+rad_brain_fat+rad_brain_skin)), 2*sk_d*sk_c/time + 2*sk_k/math.pow((rad_brain_skin/2),2)]
                             ])


        if icl_catel == 1:
            # Defination of only conducitive coefficient of body elements
            CC_M_1 = np.block([
                              [trunk_CC_1      , np.zeros((5, 5)), np.zeros((5, 5))],
                              [np.zeros((5, 5)), head_CC_1       , np.zeros((5, 5))],
                              [np.zeros((5, 5)), np.zeros((5, 5)), trunk_CC_1      ]
                              ])

            CC_M_2 = np.block([
                              [trunk_CC_2      , np.zeros((5, 5)), np.zeros((5, 5))],
                              [np.zeros((5, 5)), head_CC_2       , np.zeros((5, 5))],
                              [np.zeros((5, 5)), np.zeros((5, 5)), trunk_CC_2      ]
                              ])

            # Appedance of blood transfer coefficient for body elements
            CC_M_1 = CC_M_1 - np.diagflat(beta)
            CC_M_2 = CC_M_2 + np.diagflat(beta)

            # Appedance of whole blood circulation sysetem
            V_beta = Vol * beta

            br = np.empty(shape=(0))

            V_beta.reshape(15)

            for I in range(0, len(V_beta), 5):
                if I // 5 == 0:
                    #            XX = np.array([-((V_beta[I]) / (V_beta[I] + 0.0)) * V_beta[I],
                    #            -((V_beta[I] + V_beta[I+1]) / (V_beta[I] + V_beta[I+1] + 0.0)) * V_beta[I+1],
                    #            -((V_beta[I] + V_beta[I+1] + V_beta[I+2]) / (V_beta[I] + V_beta[I+1] + V_beta[I+2] + 0.0)) * V_beta[I+2],
                    #            -((V_beta[I] + V_beta[I+1] + V_beta[I+2] + V_beta[I+3]) / (V_beta[I] + V_beta[I+1] + V_beta[I+2] + V_beta[I+3] + 0.0)) * V_beta[I+3],
                    #            -((V_beta[I] + V_beta[I+1] + V_beta[I+2] + V_beta[I+3] + V_beta[I+4]) / (V_beta[I] + V_beta[I+1] + V_beta[I+2] + V_beta[I+3] + V_beta[I+4] + 0.0)) * V_beta[I+4]])
                    XX = np.array([-((V_beta[I]) / (V_beta[I] + 0.0)) * V_beta[I],
                                   -(V_beta[I:I+2].sum() / (V_beta[I:I+2].sum() + 0.0)) * V_beta[I + 1],
                                   -(V_beta[I:I+3].sum() / (V_beta[I:I+3].sum() + 0.0)) * V_beta[I + 2],
                                   -(V_beta[I:I+4].sum() / (V_beta[I:I+4].sum() + 0.0)) * V_beta[I + 3],
                                   -(V_beta[I:I+5].sum() / (V_beta[I:I+5].sum() + 0.0)) * V_beta[I + 4]])
                    br = np.append(br, XX)
                if I // 5 == 1:
                    XX = np.array([-((V_beta[I]) / (V_beta[I] + 0.0)) * V_beta[I],
                                   -(V_beta[I:I+2].sum() / (V_beta[I:I+2].sum() + 0.0)) * V_beta[I + 1],
                                   -(V_beta[I:I+3].sum() / (V_beta[I:I+3].sum() + 0.0)) * V_beta[I + 2],
                                   -(V_beta[I:I+4].sum() / (V_beta[I:I+4].sum() + 0.0)) * V_beta[I + 3],
                                   -(V_beta[I:I+5].sum() / (V_beta[I:I+5].sum() + 0.0)) * V_beta[I + 4]])
                    br = np.append(br, XX)
                if I // 5 == 2:
                    XX = np.array([-((V_beta[I]) / (V_beta[I] + 0.0)) * V_beta[I],
                                   -(V_beta[I:I+2].sum() / (V_beta[I:I+2].sum() + 0.0)) * V_beta[I + 1],
                                   -(V_beta[I:I+3].sum() / (V_beta[I:I+3].sum() + 5.4)) * V_beta[I + 2],
                                   -(V_beta[I:I+4].sum() / (V_beta[I:I+4].sum() + 5.4)) * V_beta[I + 3],
                                   -(V_beta[I:I+5].sum() / (V_beta[I:I+5].sum() + 5.4)) * V_beta[I + 4]])
                    br = np.append(br, XX)
            bc  = - br.reshape((15,1))/Vol
            bpl = np.array([math.pow(beta[0:5].sum(), 2)/(beta[0:5].sum()+0.0)+math.pow(beta[5:10].sum(), 2)/(beta[5:10].sum()+0.0)+math.pow(beta[10:15].sum(), 2)/(beta[10:15].sum()+5.4)])
            # assemble of conductive and blood transfer coefficient matrices
            CC_M_1 = np.block([
                              [CC_M_1, bc] ,
                              [br    , bpl]
                              ])

            CC_M_2 = np.block([
                              [CC_M_2, -bc],
                              [br    , bpl]
                              ])

        if icl_catel == 2 or icl_catel == 3:

            # Defination of only conducitive coefficient of body elements
            CC_M_1 = np.block([
                              [trunk_CC_1      , np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5))],
                              [np.zeros((5, 5)), head_CC_1       , np.zeros((5, 5)), np.zeros((5, 5))],
                              [np.zeros((5, 5)), np.zeros((5, 5)), trunk_CC_1      , np.zeros((5, 5))],
                              [np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5)), trunk_CC_1      ]
                              ])

            CC_M_2 = np.block([
                              [trunk_CC_2      , np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5))],
                              [np.zeros((5, 5)), head_CC_2       , np.zeros((5, 5)), np.zeros((5, 5))],
                              [np.zeros((5, 5)), np.zeros((5, 5)), trunk_CC_2      , np.zeros((5, 5))],
                              [np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5)), trunk_CC_2      ]
                              ])

            # Appedance of blood transfer coefficient for body elements

            CC_M_1 = CC_M_1 - np.diagflat(beta)
            CC_M_2 = CC_M_2 + np.diagflat(beta)

            # Appedance of whole blood circulation sysetem
            V_beta = Vol * beta

            br = np.empty(shape=(0))

            V_beta.reshape(20)

            for I in range(0, len(V_beta), 5):
                if I // 5 == (0 or 1):
                    XX = np.array([-((V_beta[I]) / (V_beta[I] + 0.0)) * V_beta[I],
                                   -(V_beta[I:I+2].sum() / (V_beta[I:I+2].sum() + 0.0)) * V_beta[I + 1],
                                   -(V_beta[I:I+3].sum() / (V_beta[I:I+3].sum() + 0.0)) * V_beta[I + 2],
                                   -(V_beta[I:I+4].sum() / (V_beta[I:I+4].sum() + 0.0)) * V_beta[I + 3],
                                   -(V_beta[I:I+5].sum() / (V_beta[I:I+5].sum() + 0.0)) * V_beta[I + 4]])
                    br = np.append(br, XX)

                else:
                    XX = np.array([-((V_beta[I]) / (V_beta[I] + 0.0)) * V_beta[I],
                                   -(V_beta[I:I+2].sum() / (V_beta[I:I+2].sum() + 0.0)) * V_beta[I + 1],
                                   -(V_beta[I:I+3].sum() / (V_beta[I:I+3].sum() + 5.4)) * V_beta[I + 2],
                                   -(V_beta[I:I+4].sum() / (V_beta[I:I+4].sum() + 5.4)) * V_beta[I + 3],
                                   -(V_beta[I:I+5].sum() / (V_beta[I:I+5].sum() + 5.4)) * V_beta[I + 4]])
                    br = np.append(br, XX)

            bc  = - br.reshape((20,1))/Vol

            bpl = np.array([math.pow(beta[0:5].sum(), 2)/(beta[0:5].sum()+0.0)+math.pow(beta[5:10].sum(), 2)/(beta[5:10].sum()+0.0)\
                  +math.pow(beta[10:15].sum(), 2)/(beta[10:15].sum()+5.4)+math.pow(beta[15:20].sum(), 2)/(beta[15:20].sum()+5.4)])

            # assemble of conductive and blood transfer coefficient matrices
            CC_M_1 = np.block([
                              [CC_M_1, bc] ,
                              [br    , bpl]
                              ])

            CC_M_2 = np.block([
                              [CC_M_2, -bc],
                              [br    , bpl]
                              ])

        if icl_catel == 4 or icl_catel == 5:

            # Defination of only conducitive coefficient of body elements
            CC_M_1 = np.block([
                [trunk_CC_1      , np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5))],
                [np.zeros((5, 5)), head_CC_1       , np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5))],
                [np.zeros((5, 5)), np.zeros((5, 5)), trunk_CC_1      , np.zeros((5, 5)), np.zeros((5, 5))],
                [np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5)), trunk_CC_1      , np.zeros((5, 5))],
                [np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5)), trunk_CC_1      ]
            ])

            CC_M_2 = np.block([
                [trunk_CC_2      , np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5))],
                [np.zeros((5, 5)), head_CC_2       , np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5))],
                [np.zeros((5, 5)), np.zeros((5, 5)), trunk_CC_2      , np.zeros((5, 5)), np.zeros((5, 5))],
                [np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5)), trunk_CC_2      , np.zeros((5, 5))],
                [np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5)), trunk_CC_2      ]
            ])

            # Appedance of blood transfer coefficient for body elements
            CC_M_1 = CC_M_1 - np.diagflat(beta)
            CC_M_2 = CC_M_2 + np.diagflat(beta)

            # Appedance of whole blood circulation sysetem
            V_beta = Vol * beta

            br = np.empty(shape=(0))

            V_beta.reshape(25)

            for I in range(0, len(V_beta), 5):
                if I // 5 == (0 or 1):
                    XX = np.array([-((V_beta[I]) / (V_beta[I] + 0.0)) * V_beta[I],
                                   -(V_beta[I:I + 2].sum() / (V_beta[I:I + 2].sum() + 0.0)) * V_beta[I + 1],
                                   -(V_beta[I:I + 3].sum() / (V_beta[I:I + 3].sum() + 0.0)) * V_beta[I + 2],
                                   -(V_beta[I:I + 4].sum() / (V_beta[I:I + 4].sum() + 0.0)) * V_beta[I + 3],
                                   -(V_beta[I:I + 5].sum() / (V_beta[I:I + 5].sum() + 0.0)) * V_beta[I + 4]])
                    br = np.append(br, XX)

                else:
                    XX = np.array([-((V_beta[I]) / (V_beta[I] + 0.0)) * V_beta[I],
                                   -(V_beta[I:I + 2].sum() / (V_beta[I:I + 2].sum() + 0.0)) * V_beta[I + 1],
                                   -(V_beta[I:I + 3].sum() / (V_beta[I:I + 3].sum() + 5.4)) * V_beta[I + 2],
                                   -(V_beta[I:I + 4].sum() / (V_beta[I:I + 4].sum() + 5.4)) * V_beta[I + 3],
                                   -(V_beta[I:I + 5].sum() / (V_beta[I:I + 5].sum() + 5.4)) * V_beta[I + 4]])
                    br = np.append(br, XX)

            bc = - br.reshape((25, 1)) / Vol

            bpl = np.array([math.pow(beta[0:5].sum(), 2) / (beta[0:5].sum() + 0.0) + math.pow(beta[5:10].sum(), 2) / (beta[5:10].sum() + 0.0) \
                  + math.pow(beta[10:15].sum(), 2) / (beta[10:15].sum() + 5.4) + math.pow(beta[15:20].sum(), 2) / (
                  beta[15:20].sum() + 5.4) + math.pow(beta[20:25].sum(), 2) / (beta[20:25].sum() + 5.4)])

            # assemble of conductive and blood transfer coefficient matrices
            CC_M_1 = np.block([
                [CC_M_1, bc],
                [br, bpl]
            ])

            CC_M_2 = np.block([
                [CC_M_2, -bc],
                [br, bpl]
            ])

        if icl_catel == 6:

            # Defination of only conducitive coefficient of body elements
            CC_M_1 = np.block([
                [trunk_CC_1, np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5))],
                [np.zeros((5, 5)), head_CC_1, np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5))],
                [np.zeros((5, 5)), np.zeros((5, 5)), trunk_CC_1, np.zeros((5, 5)), np.zeros((5, 5))],
                [np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5)), trunk_CC_1, np.zeros((5, 5))],
                [np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5)), head_CC_1]
            ])

            CC_M_2 = np.block([
                [trunk_CC_2, np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5))],
                [np.zeros((5, 5)), head_CC_2, np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5))],
                [np.zeros((5, 5)), np.zeros((5, 5)), trunk_CC_2, np.zeros((5, 5)), np.zeros((5, 5))],
                [np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5)), trunk_CC_2, np.zeros((5, 5))],
                [np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5)), np.zeros((5, 5)), head_CC_2]
            ])

            # Appedance of blood transfer coefficient for body elements
            CC_M_1 = CC_M_1 - np.diagflat(beta)
            CC_M_2 = CC_M_2 + np.diagflat(beta)

            # Appedance of whole blood circulation sysetem
            V_beta = Vol * beta

            br = np.empty(shape=(0))

            V_beta.reshape(25)

            for I in range(0, len(V_beta), 5):
                if I // 5 == (0 or 1):
                    XX = np.array([-((V_beta[I]) / (V_beta[I] + 0.0)) * V_beta[I],
                                   -(V_beta[I:I + 2].sum() / (V_beta[I:I + 2].sum() + 0.0)) * V_beta[I + 1],
                                   -(V_beta[I:I + 3].sum() / (V_beta[I:I + 3].sum() + 0.0)) * V_beta[I + 2],
                                   -(V_beta[I:I + 4].sum() / (V_beta[I:I + 4].sum() + 0.0)) * V_beta[I + 3],
                                   -(V_beta[I:I + 5].sum() / (V_beta[I:I + 5].sum() + 0.0)) * V_beta[I + 4]])
                    br = np.append(br, XX)
                elif I // 5 == 4:
                    XX = np.array([-((V_beta[I]) / (V_beta[I] + 0.0)) * V_beta[I],
                                   -(V_beta[I:I + 2].sum() / (V_beta[I:I + 2].sum() + 0.0)) * V_beta[I + 1],
                                   -(V_beta[I:I + 3].sum() / (V_beta[I:I + 3].sum() + 1.2)) * V_beta[I + 2],
                                   -(V_beta[I:I + 4].sum() / (V_beta[I:I + 4].sum() + 1.2)) * V_beta[I + 3],
                                   -(V_beta[I:I + 5].sum() / (V_beta[I:I + 5].sum() + 1.2)) * V_beta[I + 4]])
                    br = np.append(br, XX)
                else:
                    XX = np.array([-((V_beta[I]) / (V_beta[I] + 0.0)) * V_beta[I],
                                   -(V_beta[I:I + 2].sum() / (V_beta[I:I + 2].sum() + 0.0)) * V_beta[I + 1],
                                   -(V_beta[I:I + 3].sum() / (V_beta[I:I + 3].sum() + 5.4)) * V_beta[I + 2],
                                   -(V_beta[I:I + 4].sum() / (V_beta[I:I + 4].sum() + 5.4)) * V_beta[I + 3],
                                   -(V_beta[I:I + 5].sum() / (V_beta[I:I + 5].sum() + 5.4)) * V_beta[I + 4]])
                    br = np.append(br, XX)

            bc = - br.reshape((25, 1)) / Vol

            bpl = np.array([math.pow(beta[0:5].sum(), 2) / (beta[0:5].sum() + 0.0) + math.pow(beta[5:10].sum(), 2) / (beta[5:10].sum() + 0.0) \
                  + math.pow(beta[10:15].sum(), 2) / (beta[10:15].sum() + 5.4) + math.pow(beta[15:20].sum(), 2) / (
                beta[15:20].sum() + 5.4) + math.pow(beta[20:25].sum(), 2) / (beta[20:25].sum() + 1.2)])

            # assemble of conductive and blood transfer coefficient matrices
            CC_M_1 = np.block([
                [CC_M_1, bc],
                [br, bpl]
            ])

            CC_M_2 = np.block([
                [CC_M_2, -bc],
                [br, bpl]
            ])
        return CC_M_1, CC_M_2
    # end of set_CC_mat

    def set_Tcl_out_i(icl_catel, T_M_1, ta, clo_1, clo_2, clo_3, clo_cap, clo_1_T, clo_2_T, clo_3_T, clo_cap_T):

        if icl_catel == 1:
            T_sk_p = np.array([T_M_1[4, 0], T_M_1[9, 0], T_M_1[14, 0]])  # Skin Temperature profile
            T_cl_out_i = np.array([(T_sk_p[0] - (T_sk_p[0]-ta)*((clo_1)/(clo_1_T))), T_sk_p[1], T_sk_p[2]])
        if icl_catel == 2 or icl_catel == 3:
            T_sk_p = np.array([T_M_1[4, 0], T_M_1[9, 0], T_M_1[14, 0], T_M_1[19, 0]]) # Skin Temperature profile
            T_cl_out_i = np.array([(T_sk_p[0] - (T_sk_p[0] - ta) * ((clo_1) / (clo_1_T))), T_sk_p[1], (T_sk_p[2] - (T_sk_p[2]-ta)*((clo_2)/(clo_2_T))), T_sk_p[3]])
        if icl_catel == 4 or icl_catel == 5:
            T_sk_p = np.array([T_M_1[4, 0], T_M_1[9, 0], T_M_1[14, 0], T_M_1[19, 0], T_M_1[24, 0]]) # Skin Temperature profile
            T_cl_out_i = np.array([(T_sk_p[0] - (T_sk_p[0] - ta) * ((clo_1) / (clo_1_T))), T_sk_p[1], (T_sk_p[2] - (T_sk_p[2]-ta)*((clo_2)/(clo_2_T))), (T_sk_p[3] - (T_sk_p[3]-ta)*((clo_3)/(clo_3_T))), T_sk_p[4]])
        if icl_catel == 6:
            T_sk_p = np.array([T_M_1[4, 0], T_M_1[9, 0], T_M_1[14, 0], T_M_1[19, 0], T_M_1[24, 0]]) # Skin Temperature profile
            T_cl_out_i = np.array([(T_sk_p[0] - (T_sk_p[0] - ta) * ((clo_1) / (clo_1_T))), T_sk_p[1], (T_sk_p[2] - (T_sk_p[2]-ta)*((clo_2)/(clo_2_T))), (T_sk_p[3] - (T_sk_p[3]-ta)*((clo_3)/(clo_3_T))), (T_sk_p[4] - (T_sk_p[4]-ta)*((clo_cap)/(clo_cap_T)))])
        return T_cl_out_i

    def set_Tcl_in_i(icl_catel, ta, tmrt, T_M_1, T_cl_out_input, I_a, clo_air_in, hc, clo_1, clo_2, clo_3, clo_cap, e_sk, e_cl, feff, sigma):

        #global T_cl_in, T_cl_out, hr_M, T_sk_p, I_a_M, To_M, Icl_M, e_M, clo_air_in_M

        if icl_catel == 1:

            T_sk_p       = np.array([T_M_1[4, 0], T_M_1[9, 0], T_M_1[14, 0]]) # Skin Temperature profile
            e_M          = np.array([e_cl, e_sk, e_sk])
            Icl_M        = np.array([clo_1, 0.0, 0.0])
            I_a_M        = np.array([I_a, I_a, I_a])
            clo_air_in_M = np.array([clo_air_in, I_a, I_a])
            Icl_t_M      = Icl_M + I_a_M / (1 + 1.81* Icl_M)
            hr_M     = feff*e_M*sigma*(np.power(T_cl_out_input+273.2,3)+np.power(T_cl_out_input+273.2,2)*(tmrt+273.2)+(T_cl_out_input+273.2)*np.power(tmrt+273.2,2)+np.power(tmrt+273.2,3))
            To_M     = (hc*ta +hr_M * tmrt)/(hc + hr_M)
            T_cl_out = T_sk_p - (T_sk_p - To_M) * (Icl_M/Icl_t_M)
            T_cl_in  = T_sk_p - ( T_cl_out - To_M) * (clo_air_in_M/(Icl_t_M - Icl_M))

        if icl_catel == 2 or icl_catel == 3:

            T_sk_p       = np.array([T_M_1[4, 0], T_M_1[9, 0], T_M_1[14, 0], T_M_1[19, 0]]) # Skin Temperature profile
            e_M          = np.array([e_cl, e_sk, e_cl, e_sk])
            Icl_M        = np.array([clo_1, 0.0, clo_2, 0.0])
            I_a_M        = np.array([I_a, I_a, I_a, I_a])
            clo_air_in_M = np.array([clo_air_in, I_a, clo_air_in, I_a])
            Icl_t_M      = Icl_M + I_a_M / (1 + 1.81* Icl_M)

            hr_M     = feff*e_M*sigma*(np.power(T_cl_out_input+273.2,3)+np.power(T_cl_out_input+273.2,2)*(tmrt+273.2)+(T_cl_out_input+273.2)*np.power(tmrt+273.2,2)+np.power(tmrt+273.2,3))
            To_M     = (hc*ta +hr_M * tmrt)/(hc + hr_M)
            T_cl_out = T_sk_p - (T_sk_p - To_M) * (Icl_M/Icl_t_M)
            T_cl_in  = T_sk_p - ( T_cl_out - To_M) * (clo_air_in_M/(Icl_t_M - Icl_M))

        if icl_catel == 4 or icl_catel == 5:

            T_sk_p       = np.array([T_M_1[4, 0], T_M_1[9, 0], T_M_1[14, 0], T_M_1[19, 0], T_M_1[24, 0]]) # Skin Temperature profile
            e_M          = np.array([e_cl, e_sk, e_cl, e_cl, e_sk])
            Icl_M        = np.array([clo_1, 0.0, clo_2, clo_3, 0.0])
            I_a_M        = np.array([I_a, I_a, I_a, I_a, I_a])
            clo_air_in_M = np.array([clo_air_in, I_a, clo_air_in, clo_air_in, I_a])
            Icl_t_M      = Icl_M + I_a_M / (1 + 1.81 * Icl_M)

            hr_M     = feff * e_M * sigma * ( np.power(T_cl_out_input + 273.2, 3) + np.power(T_cl_out_input + 273.2, 2) * (tmrt + 273.2) + ( T_cl_out_input + 273.2) * np.power(tmrt + 273.2, 2) + np.power(tmrt + 273.2, 3))
            To_M     = (hc * ta + hr_M * tmrt) / (hc + hr_M)
            T_cl_out = T_sk_p - (T_sk_p - To_M) * (Icl_M / Icl_t_M)
            T_cl_in  = T_sk_p - (T_cl_out - To_M) * (clo_air_in_M / (Icl_t_M - Icl_M))

        if icl_catel == 6:

            T_sk_p       = np.array([T_M_1[4, 0], T_M_1[9, 0], T_M_1[14, 0], T_M_1[19, 0], T_M_1[24, 0]]) # Skin Temperature profile
            e_M          = np.array([e_cl, e_sk, e_cl, e_cl, e_cl])
            Icl_M        = np.array([clo_1, 0.0, clo_2, clo_3, clo_cap])
            I_a_M        = np.array([I_a, I_a, I_a, I_a, I_a])
            clo_air_in_M = np.array([clo_air_in, I_a, clo_air_in, clo_air_in, clo_air_in])
            Icl_t_M      = Icl_M + I_a_M / (1 + 1.81 * Icl_M)

            hr_M     = feff * e_M * sigma * ( np.power(T_cl_out_input + 273.2, 3) + np.power(T_cl_out_input + 273.2, 2) * (tmrt + 273.2) + ( T_cl_out_input + 273.2) * np.power(tmrt + 273.2, 2) + np.power(tmrt + 273.2, 3))
            To_M     = (hc * ta + hr_M * tmrt) / (hc + hr_M)
            T_cl_out = T_sk_p - (T_sk_p - To_M) * (Icl_M / Icl_t_M)
            T_cl_in  = T_sk_p - (T_cl_out - To_M) * (clo_air_in_M / (Icl_t_M - Icl_M))

        return T_cl_in, T_cl_out, hr_M, T_sk_p, I_a_M, To_M, Icl_M, e_M, clo_air_in_M
    # end of set T_cl_in_initialization

    def set_Tcl_in(icl_catel, ta, tmrt, T_M_1, T_cl_out_input, hr_M_i, clo_air_in, hc, clo_1, clo_2, clo_3, clo_cap, e_sk, e_cl, feff, sigma):

        #global T_cl_in, T_cl_out, hr_M, T_sk_p, I_a_M, To_M, Icl_M, e_M, clo_air_in_M

        if icl_catel == 1:

            T_sk_p       = np.array([T_M_1[4, 0], T_M_1[9, 0], T_M_1[14, 0]]) # Skin Temperature profile
            e_M          = np.array([e_cl, e_sk, e_sk])
            Icl_M        = np.array([clo_1, 0.0, 0.0])
            I_a_M        = 1/ (hc + hr_M_i)
            clo_air_in_M = np.array([clo_air_in, I_a_M[1], I_a_M[2]])
            Icl_t_M      = Icl_M + I_a_M / (1 + 1.81* Icl_M)

            hr_M     = feff*e_M*sigma*(np.power(T_cl_out_input+273.2,3)+np.power(T_cl_out_input+273.2,2)*(tmrt+273.2)+(T_cl_out_input+273.2)*np.power(tmrt+273.2,2)+np.power(tmrt+273.2,3))
            To_M     = (hc*ta +hr_M * tmrt)/(hc + hr_M)
            T_cl_out = T_sk_p - (T_sk_p - To_M) * (Icl_M/Icl_t_M)
            T_cl_in  = T_sk_p - ( T_cl_out - To_M) * (clo_air_in_M/(Icl_t_M - Icl_M))

        if icl_catel == 2 or icl_catel == 3:

            T_sk_p       = np.array([T_M_1[4, 0], T_M_1[9, 0], T_M_1[14, 0], T_M_1[19, 0]]) # Skin Temperature profile
            e_M          = np.array([e_cl, e_sk, e_cl, e_sk])
            Icl_M        = np.array([clo_1, 0.0, clo_2, 0.0])
            I_a_M        = 1 / (hc + hr_M_i)
            clo_air_in_M = np.array([clo_air_in, I_a_M[1], clo_air_in, I_a_M[3]])
            Icl_t_M      = Icl_M + I_a_M / (1 + 1.81* Icl_M)

            hr_M     = feff*e_M*sigma*(np.power(T_cl_out_input+273.2,3)+np.power(T_cl_out_input+273.2,2)*(tmrt+273.2)+(T_cl_out_input+273.2)*np.power(tmrt+273.2,2)+np.power(tmrt+273.2,3))
            To_M     = (hc*ta +hr_M * tmrt)/(hc + hr_M)
            T_cl_out = T_sk_p - (T_sk_p - To_M) * (Icl_M/Icl_t_M)
            T_cl_in  = T_sk_p - ( T_cl_out - To_M) * (clo_air_in_M/(Icl_t_M - Icl_M))

        if icl_catel == 4 or icl_catel == 5:

            T_sk_p       = np.array([T_M_1[4, 0], T_M_1[9, 0], T_M_1[14, 0], T_M_1[19, 0], T_M_1[24, 0]]) # Skin Temperature profile
            e_M          = np.array([e_cl, e_sk, e_cl, e_cl, e_sk])
            Icl_M        = np.array([clo_1, 0.0, clo_2, clo_3, 0.0])
            I_a_M        = 1 / (hc + hr_M_i)
            clo_air_in_M = np.array([clo_air_in, I_a_M[1], clo_air_in, clo_air_in, I_a_M[4]])
            Icl_t_M      = Icl_M + I_a_M / (1 + 1.81 * Icl_M)

            hr_M     = feff * e_M * sigma * ( np.power(T_cl_out_input + 273.2, 3) + np.power(T_cl_out_input + 273.2, 2) * (tmrt + 273.2) + ( T_cl_out_input + 273.2) * np.power(tmrt + 273.2, 2) + np.power(tmrt + 273.2, 3))
            To_M     = (hc * ta + hr_M * tmrt) / (hc + hr_M)
            T_cl_out = T_sk_p - (T_sk_p - To_M) * (Icl_M / Icl_t_M)
            T_cl_in  = T_sk_p - (T_cl_out - To_M) * (clo_air_in_M / (Icl_t_M - Icl_M))

        if icl_catel == 6:

            T_sk_p       = np.array([T_M_1[4, 0], T_M_1[9, 0], T_M_1[14, 0], T_M_1[19, 0], T_M_1[24, 0]]) # Skin Temperature profile
            e_M          = np.array([e_cl, e_sk, e_cl, e_cl, e_cl])
            Icl_M        = np.array([clo_1, 0.0, clo_2, clo_3, clo_cap])
            I_a_M        = 1 / (hc + hr_M_i)
            clo_air_in_M = np.array([clo_air_in, I_a_M[1], clo_air_in, clo_air_in, clo_air_in])
            Icl_t_M      = Icl_M + I_a_M / (1 + 1.81 * Icl_M)

            hr_M     = feff * e_M * sigma * ( np.power(T_cl_out_input + 273.2, 3) + np.power(T_cl_out_input + 273.2, 2) * (tmrt + 273.2) + ( T_cl_out_input + 273.2) * np.power(tmrt + 273.2, 2) + np.power(tmrt + 273.2, 3))
            To_M     = (hc * ta + hr_M * tmrt) / (hc + hr_M)
            T_cl_out = T_sk_p - (T_sk_p - To_M) * (Icl_M / Icl_t_M)
            T_cl_in  = T_sk_p - (T_cl_out - To_M) * (clo_air_in_M / (Icl_t_M - Icl_M))
        return T_cl_in, T_cl_out, hr_M, T_sk_p, I_a_M, To_M, Icl_M, e_M, clo_air_in_M
    # end of set T_cl_in


    def set_boundary_T(icl_catel, T_core_i, T_M_1, T_cl_in, M_k, sk_k,  br_k, rad_brain, rad_brain_skin, rad_brain_inside, rad_body, rad_body_skin, rad_body_inside):

        #global T_boundary

        if icl_catel == 1:
            # boundary setting for body model
            T_boundary = np.array([2 * (M_k / (math.pow(rad_body_inside / 2, 2)) - M_k /(2 * (rad_body_inside / 2) * (rad_body_inside / 2))) * T_core_i,
                                   0.0,
                                   0.0,
                                   0.0,
                                   2 * (sk_k / math.pow(rad_body_skin / 2, 2) + sk_k / (2 * (rad_body_skin / 2) * (rad_body))) * T_cl_in[0],
                                   2 * (br_k / (math.pow(rad_brain_inside / 2, 2)) - br_k / (2 * (rad_brain_inside / 2) * (rad_brain_inside / 2))) * T_M_1[0, 0],
                                   0.0,
                                   0.0,
                                   0.0,
                                   2 * (sk_k / math.pow(rad_brain_skin / 2, 2) + sk_k / ( 2 * (rad_brain_skin / 2) * (rad_brain))) * T_cl_in[1],
                                   2 * (M_k / (math.pow(rad_body_inside / 2, 2)) - M_k / ( 2 * (rad_body_inside / 2) * (rad_body_inside / 2))) * T_M_1[0, 0],
                                   0.0,
                                   0.0,
                                   0.0,
                                   2*(sk_k/math.pow(rad_body_skin/2,2)+sk_k/(2*(rad_body_skin/2)*(rad_body)))*T_cl_in[2],
                                   0.0
                                   ])
            T_boundary = np.reshape(T_boundary, (16, -1))

        if icl_catel == 2 or icl_catel == 3:
            # boundary setting for body model
            T_boundary = np.array([2 * (M_k / (math.pow(rad_body_inside / 2, 2)) - M_k /(2 * (rad_body_inside / 2) * (rad_body_inside / 2))) * T_core_i,
                                   0.0,
                                   0.0,
                                   0.0,
                                   2 * (sk_k / math.pow(rad_body_skin / 2, 2) + sk_k / (2 * (rad_body_skin / 2) * (rad_body))) * T_cl_in[0],
                                   2 * (br_k / (math.pow(rad_brain_inside / 2, 2)) - br_k / (2 * (rad_brain_inside / 2) * (rad_brain_inside / 2))) * T_M_1[0, 0],
                                   0.0,
                                   0.0,
                                   0.0,
                                   2 * (sk_k / math.pow(rad_brain_skin / 2, 2) + sk_k / ( 2 * (rad_brain_skin / 2) * (rad_brain))) * T_cl_in[1],
                                   2 * (M_k / (math.pow(rad_body_inside / 2, 2)) - M_k / ( 2 * (rad_body_inside / 2) * (rad_body_inside / 2))) * T_M_1[0, 0],
                                   0.0,
                                   0.0,
                                   0.0,
                                   2*(sk_k/math.pow(rad_body_skin/2,2)+sk_k/(2*(rad_body_skin/2)*(rad_body)))*T_cl_in[2],
                                   2 * (M_k / (math.pow(rad_body_inside / 2, 2)) - M_k / ( 2 * (rad_body_inside / 2) * (rad_body_inside / 2))) * T_M_1[10, 0],
                                   0.0,
                                   0.0,
                                   0.0,
                                   2 * (sk_k / math.pow(rad_body_skin / 2, 2) + sk_k / ( 2 * (rad_body_skin / 2) * (rad_body))) * T_cl_in[3],
                                   0.0
                                   ])
            T_boundary = np.reshape(T_boundary, (21, -1))

        if icl_catel == 4 or icl_catel == 5:
            # boundary setting for body model
            T_boundary = np.array([2 * (M_k / (math.pow(rad_body_inside / 2, 2)) - M_k /(2 * (rad_body_inside / 2) * (rad_body_inside / 2))) * T_core_i,
                                   0.0,
                                   0.0,
                                   0.0,
                                   2 * (sk_k / math.pow(rad_body_skin / 2, 2) + sk_k / (2 * (rad_body_skin / 2) * (rad_body))) * T_cl_in[0],
                                   2 * (br_k / (math.pow(rad_brain_inside / 2, 2)) - br_k / (2 * (rad_brain_inside / 2) * (rad_brain_inside / 2))) * T_M_1[0, 0],
                                   0.0,
                                   0.0,
                                   0.0,
                                   2 * (sk_k / math.pow(rad_brain_skin / 2, 2) + sk_k / ( 2 * (rad_brain_skin / 2) * (rad_brain))) * T_cl_in[1],
                                   2 * (M_k / (math.pow(rad_body_inside / 2, 2)) - M_k / ( 2 * (rad_body_inside / 2) * (rad_body_inside / 2))) * T_M_1[0, 0],
                                   0.0,
                                   0.0,
                                   0.0,
                                   2*(sk_k/math.pow(rad_body_skin/2,2)+sk_k/(2*(rad_body_skin/2)*(rad_body)))*T_cl_in[2],
                                   2 * (M_k / (math.pow(rad_body_inside / 2, 2)) - M_k / ( 2 * (rad_body_inside / 2) * (rad_body_inside / 2))) * T_M_1[10, 0],
                                   0.0,
                                   0.0,
                                   0.0,
                                   2 * (sk_k / math.pow(rad_body_skin / 2, 2) + sk_k / ( 2 * (rad_body_skin / 2) * (rad_body))) * T_cl_in[3],
                                   2 * (M_k / (math.pow(rad_body_inside / 2, 2)) - M_k / ( 2 * (rad_body_inside / 2) * (rad_body_inside / 2))) * T_M_1[15, 0],
                                   0.0,
                                   0.0,
                                   0.0,
                                   2 * (sk_k / math.pow(rad_body_skin / 2, 2) + sk_k / ( 2 * (rad_body_skin / 2) * (rad_body))) * T_cl_in[4],
                                  0.0])
            T_boundary = np.reshape(T_boundary, (26, -1))

        if icl_catel == 6:
            # boundary setting for body model
            T_boundary = np.array([2 * (M_k / (math.pow(rad_body_inside / 2, 2)) - M_k /(2 * (rad_body_inside / 2) * (rad_body_inside / 2))) * T_core_i,
                                   0.0,
                                   0.0,
                                   0.0,
                                   2 * (sk_k / math.pow(rad_body_skin / 2, 2) + sk_k / (2 * (rad_body_skin / 2) * (rad_body))) * T_cl_in[0],
                                   2 * (br_k / (math.pow(rad_brain_inside / 2, 2)) - br_k / (2 * (rad_brain_inside / 2) * (rad_brain_inside / 2))) * T_M_1[0, 0],
                                   0.0,
                                   0.0,
                                   0.0,
                                   2 * (sk_k / math.pow(rad_brain_skin / 2, 2) + sk_k / ( 2 * (rad_brain_skin / 2) * (rad_brain))) * T_cl_in[1],
                                   2 * (M_k / (math.pow(rad_body_inside / 2, 2)) - M_k / ( 2 * (rad_body_inside / 2) * (rad_body_inside / 2))) * T_M_1[0, 0],
                                   0.0,
                                   0.0,
                                   0.0,
                                   2*(sk_k/math.pow(rad_body_skin/2,2)+sk_k/(2*(rad_body_skin/2)*(rad_body)))*T_cl_in[2],
                                   2 * (M_k / (math.pow(rad_body_inside / 2, 2)) - M_k / ( 2 * (rad_body_inside / 2) * (rad_body_inside / 2))) * T_M_1[10, 0],
                                   0.0,
                                   0.0,
                                   0.0,
                                   2 * (sk_k / math.pow(rad_body_skin / 2, 2) + sk_k / ( 2 * (rad_body_skin / 2) * (rad_body))) * T_cl_in[3],
                                   2 * (br_k / (math.pow(rad_brain_inside / 2, 2)) - br_k / ( 2 * (rad_brain_inside / 2) * (rad_brain_inside / 2))) * T_M_1[5, 0],
                                   0.0,
                                   0.0,
                                   0.0,
                                   2 * (sk_k / math.pow(rad_brain_skin / 2, 2) + sk_k / ( 2 * (rad_brain_skin / 2) * (rad_brain))) * T_cl_in[4],
                                   0.0
                                   ])
            T_boundary = np.reshape(T_boundary, (26, -1))

        return T_boundary
    # end of set_boundary_T

    def blood_T(icl_catel, T_M_1, body_cover_1, body_cover_2, body_cover_3, br_sk_c, br_sk_1):
        if icl_catel == 1:
            bl_T = 0.67*T_M_1[0, 0] \
                   + 0.23*(body_cover_1*T_M_1[1, 0]+br_sk_c*T_M_1[6 ,0]+(1 - body_cover_1 - br_sk_c)*T_M_1[11, 0]) \
                   + 0.1*(body_cover_1*T_M_1[4, 0]+br_sk_c*T_M_1[9, 0]+(1 - body_cover_1 - br_sk_c)*T_M_1[14, 0])

        if icl_catel == 2 or icl_catel == 3:
            bl_T = 0.67*T_M_1[0, 0] \
                   + 0.23*(body_cover_1*T_M_1[1, 0]+br_sk_c*T_M_1[6, 0]+body_cover_2*T_M_1[11, 0]+(1-body_cover_1-body_cover_2-br_sk_c)*T_M_1[16, 0]) \
                   + 0.1*(body_cover_1*T_M_1[4, 0]+br_sk_c*T_M_1[9, 0]+body_cover_2*T_M_1[14, 0]+(1-body_cover_1-body_cover_2-br_sk_c)*T_M_1[19, 0])

        if icl_catel == 4 or icl_catel == 5:
            bl_T = 0.67*T_M_1[0, 0] \
                   + 0.23*(body_cover_1*T_M_1[1, 0]+br_sk_c*T_M_1[6, 0]+body_cover_2*T_M_1[11, 0]+body_cover_3*T_M_1[16, 0]+(1-body_cover_1-body_cover_2-body_cover_3-br_sk_c)*T_M_1[21, 0])\
                   + 0.1*(body_cover_1*T_M_1[4, 0]+br_sk_c*T_M_1[9, 0]+body_cover_2*T_M_1[14, 0]+body_cover_3*T_M_1[19, 0]+(1-body_cover_1-body_cover_2-body_cover_3-br_sk_c)*T_M_1[24, 0])

        if icl_catel == 6:
            bl_T = 0.67*T_M_1[0, 0] \
                   + 0.23*(body_cover_1*T_M_1[1, 0]+(br_sk_c - br_sk_1)*T_M_1[6, 0]+body_cover_2*T_M_1[11, 0]+body_cover_3*T_M_1[16, 0] + br_sk_1*T_M_1[21, 0]) \
                   + 0.1*(body_cover_1*T_M_1[4, 0]+(br_sk_c - br_sk_1)*T_M_1[9, 0]+body_cover_2*T_M_1[14, 0]+body_cover_3*T_M_1[19, 0] + br_sk_1*T_M_1[24, 0])

        return bl_T
    # end of setting blood_T

    def set_cl_re_ISO7730(icl_catel, clo_1, clo_2, clo_3, clo_cap, evap, he, Re_factor, hr_M, clo_air_in, Icl_M):
        #global cl_re_in_M, cl_re_M, cl_re_t_M

        if icl_catel == 1:
            cl_re_in_M = np.array([Re_factor/(1.67*hc*(1/(1 +2.22*hc*(clo_air_in -(1 -1/(1+1.81*clo_air_in))/(hc +hr_M[0]))))), 1/(he*evap), 1/(he*evap)])
            cl_re_M    = np.array([Re_factor/(1.67*hc*(1/(1 +2.22*hc*(clo_1 -(1 -1/(1+1.81*clo_1))/(hc +hr_M[0]))))), 1/(he*evap), 1/(he*evap)])
            cl_re_t_M = cl_re_M + (1 / (1.67 * hc)) / (1 + 1.81 * Icl_M)
        if icl_catel == 2 or icl_catel == 3:
            cl_re_in_M = np.array([Re_factor/(1.67*hc*(1/(1 +2.22*hc*(clo_air_in -(1 -1/(1+1.81*clo_air_in))/(hc +hr_M[0]))))), 1/(he*evap), Re_factor/(1.67*hc*(1/(1 +2.22*hc*(clo_air_in -(1 -1/(1+1.81*clo_air_in))/(hc +hr_M[2]))))), 1/(he*evap)])
            cl_re_M    = np.array([Re_factor/(1.67*hc*(1/(1 +2.22*hc*(clo_1 -(1 -1/(1+1.81*clo_1))/(hc +hr_M[0]))))), 1/(he*evap), Re_factor/(1.67*hc*(1/(1 +2.22*hc*(clo_2 -(1 -1/(1+1.81*clo_2))/(hc +hr_M[2]))))), 1/(he*evap)])
            cl_re_t_M = cl_re_M + (1 / (1.67 * hc)) / (1 + 1.81 * Icl_M)
        if icl_catel == 4 or icl_catel == 5:
            cl_re_in_M = np.array([Re_factor/(1.67*hc*(1/(1 +2.22*hc*(clo_air_in -(1 -1/(1+1.81*clo_air_in))/(hc +hr_M[0]))))), 1/(he*evap), Re_factor/(1.67*hc*(1/(1 +2.22*hc*(clo_air_in -(1 -1/(1+1.81*clo_air_in))/(hc +hr_M[2]))))), Re_factor/(1.67*hc*(1/(1 +2.22*hc*(clo_air_in -(1 -1/(1+1.81*clo_air_in))/(hc +hr_M[3]))))), 1/(he*evap)])
            cl_re_M    = np.array([Re_factor/(1.67*hc*(1/(1 +2.22*hc*(clo_1 -(1 -1/(1+1.81*clo_1))/(hc +hr_M[0]))))), 1/(he*evap), Re_factor/(1.67*hc*(1/(1 +2.22*hc*(clo_2 -(1 -1/(1+1.81*clo_2))/(hc +hr_M[2]))))), Re_factor/(1.67*hc*(1/(1 +2.22*hc*(clo_3 -(1 -1/(1+1.81*clo_3))/(hc +hr_M[3]))))), 1/(he*evap)])
            cl_re_t_M = cl_re_M + (1 / (1.67 * hc)) / (1 + 1.81 * Icl_M)
        if icl_catel == 6:
            cl_re_in_M = np.array([Re_factor/(1.67*hc*(1/(1 +2.22*hc*(clo_air_in -(1 -1/(1+1.81*clo_air_in))/(hc +hr_M[0]))))), 1/(he*evap), Re_factor/(1.67*hc*(1/(1 +2.22*hc*(clo_air_in -(1 -1/(1+1.81*clo_air_in))/(hc +hr_M[2]))))), Re_factor/(1.67*hc*(1/(1 +2.22*hc*(clo_air_in -(1 -1/(1+1.81*clo_air_in))/(hc +hr_M[3]))))), Re_factor/(1.67*hc*(1/(1 +2.22*hc*(clo_air_in -(1 -1/(1+1.81*clo_air_in))/(hc +hr_M[4])))))])
            cl_re_M    = np.array([Re_factor/(1.67*hc*(1/(1 +2.22*hc*(clo_1 -(1 -1/(1+1.81*clo_1))/(hc +hr_M[0]))))), 1/(he*evap), Re_factor/(1.67*hc*(1/(1 +2.22*hc*(clo_2 -(1 -1/(1+1.81*clo_2))/(hc +hr_M[2]))))), Re_factor/(1.67*hc*(1/(1 +2.22*hc*(clo_3 -(1 -1/(1+1.81*clo_3))/(hc +hr_M[3]))))), Re_factor/(1.67*hc*(1/(1 +2.22*hc*(clo_cap -(1 -1/(1+1.81*clo_cap))/(hc +hr_M[4])))))])
            cl_re_t_M = cl_re_M + (1 / (1.67 * hc)) / (1 + 1.81 * Icl_M)

        return cl_re_in_M, cl_re_M, cl_re_t_M
    # end of set_cl_re_ISO7730
    def set_cl_re_ISO9920(icl_catel, clo_1, clo_2, clo_3, clo_cap, clo_1_T, clo_2_T, clo_3_T, clo_cap_T, evap, he, clo_air_in):

        if icl_catel == 1:
            cl_re_in_M = np.array([clo_air_in/(0.5*1.67), 1/(he*evap),  1/(he*evap)])
            cl_re_M    = np.array([clo_1/(0.38*1.67), 1/(he*evap), 1/(he*evap)])
            cl_re_t_M  = np.array([clo_1_T/(0.38*1.67), 1/(he*evap), 1/(he*evap)])
        if icl_catel == 2 or icl_catel == 3:
            cl_re_in_M = np.array([clo_air_in/(0.5*1.67), 1/(he*evap), clo_air_in/(0.5*1.67), 1/(he*evap)])
            cl_re_M    = np.array([clo_1/(0.34*1.67), 1/(he*evap), clo_2/(0.38*1.67), 1/(he*evap)])
            cl_re_t_M  = np.array([clo_1_T/(0.34*1.67), 1/(he*evap), clo_2_T/(0.38*1.67), 1/(he*evap)])
        if icl_catel == 4 or icl_catel == 5:
            cl_re_in_M = np.array([clo_air_in/(0.5*1.67), 1/(he*evap), clo_air_in/(0.5*1.67), clo_air_in/(0.5*1.67), 1/(he*evap)])
            cl_re_M    = np.array([clo_1/(0.15*1.67), 1/(he*evap),  clo_2/(0.34*1.67), clo_3/(0.38*1.67), 1/(he*evap)])
            cl_re_t_M  = np.array([clo_1_T/(0.15*1.67), 1/(he*evap),  clo_2_T/(0.34*1.67), clo_3_T/(0.38*1.67), 1/(he*evap)])
        if icl_catel == 6:
            cl_re_in_M = np.array([clo_air_in/(0.5*1.67), 1/(he*evap), clo_air_in/(0.5*1.67), clo_air_in/(0.5*1.67), clo_air_in/(0.5*1.67)])
            cl_re_M    = np.array([clo_1/(0.15*1.67), 1/(he*evap),  clo_2/(0.34*1.67), clo_3/(0.38*1.67), clo_cap/(0.34*1.67)])
            cl_re_t_M  = np.array([clo_1_T/(0.15*1.67), 1/(he*evap),  clo_2_T/(0.34*1.67), clo_3_T/(0.38*1.67), clo_cap_T/(0.34*1.67)])
        return cl_re_in_M, cl_re_M, cl_re_t_M
    # end of set_cl_re_ISO9920

    def sweating_mech_fiala(icl_catel, T_M_1, T_sk_p, body_cover_arr, adu, wetsk_s, sex):

        if icl_catel == 1:

            sw_M = body_cover_arr * adu* (0.001/300)*((T_sk_p - 34)*(0.43 * np.tanh(0.59*(T_sk_p - 34) -0.19) +0.65) + (T_M_1[0, 0]-36.7) * (3.06 * np.tanh(1.98*(T_M_1[0, 0]-36.7) -1.03) +3.44))

        if icl_catel == 2 or icl_catel == 3:

            sw_M = body_cover_arr * adu * (0.001 / 300) * (
                        (T_sk_p - 34) * (0.43 * np.tanh(0.59 * (T_sk_p - 34) - 0.19) + 0.65) + (T_M_1[0, 0] - 36.7) * (
                               3.06 * np.tanh(1.98 * (T_M_1[0, 0] - 36.7) - 1.03) + 3.44))

        if icl_catel == 4 or icl_catel == 5:


            sw_M = body_cover_arr * adu * (0.001 / 300) * (
                        (T_sk_p - 34) * (0.43 * np.tanh(0.59 * (T_sk_p - 34) - 0.19) + 0.65) + (T_M_1[0, 0] - 36.7) * (
                               3.06 * np.tanh(1.98 * (T_M_1[0, 0] - 36.7) - 1.03) + 3.44))


        if icl_catel == 6:


            sw_M = body_cover_arr * adu * (0.001 / 300) * (
                        (T_sk_p - 34) * (0.43 * np.tanh(0.59 * (T_sk_p - 34) - 0.19) + 0.65) + (T_M_1[0, 0] - 36.7) * (
                               3.06 * np.tanh(1.98 * (T_M_1[0, 0] - 36.7) - 1.03) + 3.44))

        if len(wetsk_s) != 0:
            for i in range(len(wetsk_s)):
                if wetsk_s[i - 1] >= 0.7:
                    sw_M[i - 1] = sw_M[i - 1] * (wetsk_s[i - 1] * (-0.35 / 0.3) + (0.65 + 0.35 / 0.3))
                if sw_M[i - 1] < 0:
                    sw_M[i - 1] = 0.0
                if sex ==  2:
                    sw_M[i - 1] = sw_M[i - 1]*0.7

        return sw_M


    # end of swearing_mech_fiala

    def sweating_mech_fiala_yung(icl_catel, T_M_1, body_cover_arr, adu, wetsk_s, sex):

        if icl_catel == 1:
            T_sk_p = np.array([T_M_1[3, 0], T_M_1[8, 0], T_M_1[13, 0]])

            sw_M = body_cover_arr * adu * (0.001 / 300) * (
                        (T_sk_p - 34) * (0.43 * np.tanh(0.59 * (T_sk_p - 34) - 0.19) + 0.65) + (T_M_1[0, 0] - 36.7) * (
                            3.06 * np.tanh(1.98 * (T_M_1[0, 0] - 36.7) - 1.03) + 3.44))

        if icl_catel == 2 or icl_catel == 3:

            T_sk_p = np.array([T_M_1[3, 0], T_M_1[8, 0], T_M_1[13, 0], T_M_1[18, 0]])

            sw_M = body_cover_arr * adu * (0.001 / 300) * (
                    (T_sk_p - 34) * (0.43 * np.tanh(0.59 * (T_sk_p - 34) - 0.19) + 0.65) + (T_M_1[0, 0] - 36.7) * (
                    3.06 * np.tanh(1.98 * (T_M_1[0, 0] - 36.7) - 1.03) + 3.44))

        if icl_catel == 4 or icl_catel == 5:

            T_sk_p = np.array([T_M_1[3, 0], T_M_1[8, 0], T_M_1[13, 0], T_M_1[18, 0], T_M_1[23, 0]])

            sw_M = body_cover_arr * adu * (0.001 / 300) * (
                    (T_sk_p - 34) * (0.43 * np.tanh(0.59 * (T_sk_p - 34) - 0.19) + 0.65) + (T_M_1[0, 0] - 36.7) * (
                    3.06 * np.tanh(1.98 * (T_M_1[0, 0] - 36.7) - 1.03) + 3.44))

        if icl_catel == 6:

            T_sk_p = np.array([T_M_1[3, 0], T_M_1[8, 0], T_M_1[13, 0], T_M_1[18, 0], T_M_1[23, 0]])

            sw_M = body_cover_arr * adu * (0.001 / 300) * (
                    (T_sk_p - 34) * (0.43 * np.tanh(0.59 * (T_sk_p - 34) - 0.19) + 0.65) + (T_M_1[0, 0] - 36.7) * (
                    3.06 * np.tanh(1.98 * (T_M_1[0, 0] - 36.7) - 1.03) + 3.44))

        if len(wetsk_s) != 0:
            for i in range(len(wetsk_s)):
                if wetsk_s[i] >= 0.7:
                    sw_M[i] = sw_M[i] * (wetsk_s[i] * (-0.35 / 0.3) + (0.65 + 0.35 / 0.3))
                if sw_M[i] < 0:
                    sw_M[i] = 0.0
                if sex == 2:
                    sw_M[i] = sw_M[i] * 0.7

        return sw_M

    # end of swearing_mech_fiala

    def wetsk_s_p_i(icl_catel, RH):
        if icl_catel == 1:
            wetsk_s = np.array([RH, RH, RH])

        if icl_catel == 2 or icl_catel == 3:
            wetsk_s = np.array([RH, RH, RH, RH])

        if icl_catel == 4 or icl_catel == 5:
            wetsk_s = np.array([RH, RH, RH, RH, RH])

        if icl_catel == 6:
            wetsk_s = np.array([RH, RH, RH, RH, RH])
        return wetsk_s

    def sk_wetted_p_i(icl_catel):
        a = 0.12
        b = 0.2
        if icl_catel == 1:
            sk_wetted = np.array([a, b, b])

        if icl_catel == 2 or icl_catel == 3:
            sk_wetted = np.array([a, b, a, b])

        if icl_catel == 4 or icl_catel == 5:
            sk_wetted = np.array([a, b, a, a, b])

        if icl_catel == 6:
            sk_wetted = np.array([a, b, a, a, a])
        return sk_wetted

    def vapor_mech_fiala(T_sk_p, sw_M, body_cover_arr, adu, vpa, evap, cl_re_t_M): # Fiala's equation in Fiala et al., 1999

        #global VP_sk_s, VP_sk, wetsk_s
        VP_sk_s = 6.1078*np.exp(17.1 * T_sk_p/(235.0+T_sk_p))
        VP_sk   = (evap * sw_M / (adu * body_cover_arr) + VP_sk_s * 0.3 + vpa / cl_re_t_M) / (0.3 + 1 / cl_re_t_M)
        for i in range(len(VP_sk)):
            if VP_sk[i] > VP_sk_s[i]:
                VP_sk[i] = VP_sk_s[i]
            if VP_sk[i] < (0.06 * VP_sk_s[i] - 0.94 * vpa):
                VP_sk[i] = 0.06 * VP_sk_s[i] - 0.94 * vpa

        wetsk_s = VP_sk/VP_sk_s

        sk_wetted = (VP_sk - vpa)/ (VP_sk_s - vpa)

        return VP_sk_s, VP_sk, wetsk_s, sk_wetted
    # end of vapor_pressure_mech_fiala

    def wet_energy_p(vpa, VP_sk, body_cover_arr, adu, cl_re_t_M):
        wet_energy = (vpa - VP_sk) * body_cover_arr * adu / cl_re_t_M
        return wet_energy

    # end of wet energy calculation

    def wet_To_mech(wet_energy, T_cl_in, clo_air_in_M, body_cover_arr, adu):
        T_cl_in_eff = T_cl_in + clo_air_in_M * wet_energy/(body_cover_arr*adu)
        return T_cl_in_eff

    # end of wet operative temperature mechanism

    def energy_flux_PET(icl_catel, T_sk_p, wet_energy, ere, h, VP_sk, body_cover_arr, wetsk_s, sk_wetted, T_cl_in, T_cl_out, Icl_M, e_M, To_M, adu, ta, vpa, tmrt, hc, feff, sigma):

        #global tsk, tsk_mm, vpts, tcl, fcl, enbal2

        tsk_ra = T_sk_p * body_cover_arr
        vpts_ra = VP_sk * body_cover_arr
        wetsk_s_ra = wetsk_s * body_cover_arr
        Tcl_arr = 0.7* T_cl_out+ 0.3*T_cl_in
        fcl_arr = 1 + 1.81* Icl_M
        fcl_ra = fcl_arr * body_cover_arr

        if icl_catel == 1:

            tsk = (tsk_ra[1] + tsk_ra[-1])/(body_cover_arr[1]+body_cover_arr[-1])
            wetsk = (wetsk_s_ra[1] + wetsk_s_ra[-1])/(body_cover_arr[1]+body_cover_arr[-1])
            vpts = (vpts_ra[1] + vpts_ra[-1])/(body_cover_arr[1]+body_cover_arr[-1])
            tcl = Tcl_arr[0]
            fcl = fcl_arr[0]

        if icl_catel == 2 or icl_catel == 3:

            tsk = (tsk_ra[1] + tsk_ra[-1]) / (body_cover_arr[1] + body_cover_arr[-1])
            wetsk = (wetsk_s_ra[1] + wetsk_s_ra[-1]) / (body_cover_arr[1] + body_cover_arr[-1])
            vpts = (vpts_ra[1] + vpts_ra[-1]) / (body_cover_arr[1] + body_cover_arr[-1])
            tcl = (Tcl_arr[0]*body_cover_arr[0]+Tcl_arr[2]*body_cover_arr[2])/(body_cover_arr[0] + body_cover_arr[2])
            fcl =  (fcl_ra[0]+fcl_ra[2])/(body_cover_arr[0] + body_cover_arr[2])
        if icl_catel == 4 or icl_catel == 5:

            tsk = (tsk_ra[1] + tsk_ra[-1]) / (body_cover_arr[1] + body_cover_arr[-1])
            wetsk = (wetsk_s_ra[1] + wetsk_s_ra[-1]) / (body_cover_arr[1] + body_cover_arr[-1])
            vpts = (vpts_ra[1] + vpts_ra[-1]) / (body_cover_arr[1] + body_cover_arr[-1])
            tcl = (Tcl_arr[0] * body_cover_arr[0] + Tcl_arr[2] * body_cover_arr[2]  + Tcl_arr[3] * body_cover_arr[3]) / (
                        body_cover_arr[0] + body_cover_arr[2] + body_cover_arr[3])
            fcl = (fcl_ra[0] + fcl_ra[2]+ fcl_ra[3]) / (body_cover_arr[0] + body_cover_arr[2] + body_cover_arr[3])
        if icl_catel == 6:
            tsk = T_sk_p[1]
            wetsk = wetsk_s[1]
            vpts = VP_sk[1]
            tcl = (Tcl_arr[0] * body_cover_arr[0] + Tcl_arr[2] * body_cover_arr[2]  + Tcl_arr[3] * body_cover_arr[3]  + Tcl_arr[4] * body_cover_arr[4]) / (
                        body_cover_arr[0] + body_cover_arr[2] + body_cover_arr[3] + body_cover_arr[4])
            fcl = (fcl_ra[0] + fcl_ra[2]+ fcl_ra[3] + fcl_ra[4]) / (body_cover_arr[0] + body_cover_arr[2] + body_cover_arr[3] + body_cover_arr[4])

        c_energy = hc*(ta - T_cl_out)*adu*body_cover_arr
        csum= np.sum(c_energy)

        r_energy = feff *adu * sigma* body_cover_arr * fcl_arr * e_M * (math.pow((tmrt + 273.2), 4) - np.power((T_cl_out + 273.2), 4))
        rsum = np.sum(r_energy)

        wet_sum = np.sum(wet_energy)

        tsk_mm =  np.sum(T_sk_p * body_cover_arr)

        sk_wetted_mm = np.sum(sk_wetted * body_cover_arr)

        enbal2 = h + rsum + csum + wet_sum + ere

        return tsk, tsk_mm, vpts, wetsk, sk_wetted_mm, tcl, fcl, enbal2, wet_sum, csum, rsum
    # end of energy_flux_PET

    def PETber(ta, p, tsk, tcl, wetsk, vpts, rtv, adu, fcl, emsk, emcl, sigma, feff, evap, cair, h0, enbal2):  # hie?zuvor nur PET
        tx = ta
        enbal3 = 0.0
        count2 = 0

        facl   = 0.87
        #acl	:= adu * facl + adu * (fcl - 1);
        acl	   = adu * facl + adu* facl* (fcl - 1)
        #hc0    = 0.0
        p0     = 1013.25  # (hPa)
        rsum0  = 0.0
        csum0  = 0.0
        ed0    = 0.0
        ere0   = 0.0
        while count2 < 4:
            # 150
            #hc = 2.67 + 6.5 * math.pow(0.1, 0.67)
            #hc *= math.pow((p / po), 0.55)
            hc0 = 2.67 + 6.5 * math.pow(0.1, 0.67)
            hc0 = hc0 * math.pow((p / p0), 0.55)
            he0 = 0.633 * hc0 / (p * cair * (1 + 0.94 * 0.622 * 12 / (p - 0.378 * 12)))
            #      hc := 2.67 + 6.5 * 0.1 ** 0.67
            #      hc := hc * (p /po) ** 0.55
            #       STRAHLUNGSSALDO
            aeff = adu * feff

            rbare = aeff * (1. - facl) * emsk * sigma * (math.pow((tx + 273.2), 4.0) - math.pow((tsk + 273.2), 4))
            rclo  = feff * acl * emcl * sigma * (math.pow((tx + 273.2), 4.0) - math.pow((tcl + 273.2), 4))
            rsum0 = rbare + rclo

            #       KONVEKTION
            cbare = hc0 * (tx - tsk) * adu * (1.0 - facl)
            cclo  = hc0 * (tx - tcl) * acl
            csum0 = cbare + cclo

            #       DIFFUSION

            rdsk  = 0.79 * math.pow(10.0, 7.0)
            # rdsk: = 0.79 * math.pow(10.0, 7.0) / (3 + ln(0.1)) * 3;
            rdcl  = 0.0
            # vpts: = 6.11 * math.pow(10.0, (7.45 * tsk / (235.0 + tsk)));

            # ed0: = evap / (rdsk + rdcl) * adu * (1.0 - wetsk) * (12.0 - vpts);
            #ed0 = (1 - facl) * adu * wetsk * (12.0 - vpts) * (he0 * evap)
            ed0 = (1 - facl) * adu * wetsk * (12.0 - vpts) * (he0 * evap)
            #ed0  = (1 - facl) * adu * (12.0 - vpts) * (he0 * evap)

            #       ATMUNG
            tex = 0.47 * tx + 21.
            eres = cair * (tx - tex) * rtv
            # vpex = 6.11 * 10.0** (7.45 * tex / (235.0+ tex))
            vpex = 6.11 * math.pow(10.0, (7.45 * tex / (235.0 + tex)))
            erel = 0.623 * evap / p * (12.0 - vpex) * rtv
            ere0 = eres + erel

            enbal = enbal2 - (h0 + ed0 + ere0 + csum0 + rsum0)
            #
            #       ITERATION BEZUEGLICH ta
            if (count2 == 0):
                xx = 1.0
            if (count2 == 1):
                xx = 0.1
            if (count2 == 2):
                xx = 0.01
            if (count2 == 3):
                xx = 0.001
            if (enbal > 0):
                tx = tx + xx
            if (enbal < 0):
                tx = tx - xx
            if ((enbal <= 0) and (enbal3 > 0)):
                count2 += 1
            if ((enbal >= 0) and (enbal3 < 0)):
                count2 += 1

            enbal3 = enbal

        return tx
    # end of PETber def

############# Main Program Zone ###################

    adu, h, h0, cair, rad_brain, rad_brain_skin, rad_brain_fat, rad_brain_inside, ht_brain, ht_body, rad_body, rad_body_skin, rad_body_fat, rad_body_inside, rtv, ere = insidebody(ta, vpa, work, ht, mbody, age, sex)

    # calculate he

    he0 = 0.633 * hc0 / (p * cair * (1 + 0.94 * 0.622 * 12 / (p - 0.378 * 12)))

    he = 0.633 * hc / (p * cair * (1 + 0.94 * 0.622 * vpa / (p - 0.378 * vpa)))

    icl, fcl = Auto_Icl_define(ta, clo_auto, icl)

    icl_catel, facl, body_cover_1, body_cover_2, body_cover_3, br_sk_1, clo_1, clo_2, clo_3, clo_cap, clo_1_T, clo_2_T, clo_3_T, clo_cap_T, body_cover_arr = Icl_define_i(icl, I_a, br_sk_c)

    T_M_1, Vol, D_M, beta, Q_M = \
        initial_body_T(icl_catel, T_core_i, T_sk_i, h, ere, M_w, fat_w, sk_w, br_w, sk_br_w, bl_d, bl_c, time, br_sk_c,
                   br_sk_1, rad_brain, rad_brain_skin, rad_brain_fat, rad_brain_inside, ht_brain, ht_body, rad_body,
                   rad_body_skin, rad_body_fat, rad_body_inside)

    CC_M_1, CC_M_2 = set_CC_Mat(icl_catel, beta, Vol, M_k, M_d, M_c, fat_k, fat_d, fat_c, sk_k, sk_d, sk_c, br_k, br_c, br_d, rad_brain, rad_brain_skin, rad_brain_fat, rad_brain_inside, rad_body, rad_body_skin, rad_body_fat, rad_body_inside)

    Tcl_out_i = set_Tcl_out_i(icl_catel, T_M_1, ta, clo_1, clo_2, clo_3, clo_cap, clo_1_T, clo_2_T, clo_3_T, clo_cap_T)

    T_cl_in, T_cl_out, hr_M, T_sk_p, I_a_M, To_M, Icl_M, e_M, clo_air_in_M = set_Tcl_in_i(icl_catel, ta, tmrt, T_M_1, Tcl_out_i, I_a, clo_air_in, hc, clo_1, clo_2, clo_3, clo_cap, e_sk, e_cl, feff, sigma)

    T_boundary = set_boundary_T(icl_catel, T_core_i, T_M_1, T_cl_in, M_k, sk_k,  br_k, rad_brain, rad_brain_skin, rad_brain_inside, rad_body, rad_body_skin, rad_body_inside)

    wetsk_s = np.array([])

    D_M_i   = D_M

    beta_i  = beta

    T_M_i   = T_M_1

    T_M_i = T_M_i[:-1, :]

    cl_re_in_M, cl_re_M, cl_re_t_M = set_cl_re_ISO7730(icl_catel, clo_1, clo_2, clo_3, clo_cap, evap, he, Re_factor,
                                                       hr_M, clo_air_in, Icl_M)


    VP_sk_s = 6.1078 * np.exp(17.1 *  T_sk_p / (235.0 + T_sk_p))

    VP_cl_in = (cl_re_t_M - cl_re_in_M)*(1/cl_re_t_M * VP_sk_s + (1/(cl_re_t_M - cl_re_in_M) - 1/cl_re_t_M) *vpa )

    sk_wetted = sk_wetted_p_i(icl_catel)

    wetsk_s = wetsk_s_p_i(icl_catel, RH)

    for i in range(1, 1201, 1):

        # Calculating the body temperature profile in the next time step

        T_M_2 = np.matmul(CC_M_1, T_M_1) + T_boundary + np.vstack((D_M, 0.0))

        CC_M_2 = np.linalg.inv(CC_M_2)

        T_M_3 = np.matmul(CC_M_2, T_M_2)

        T_M_1 = T_M_3[:-1,:]

        # reset D_M, beta, CC_M, boundary_T, body_T
        D_M = D_M_i + Q_M * np.power(2, ((T_M_1 - T_M_i)/10) -1 )

        beta = beta_i + 0.932 * time * Q_M * np.power(2, (((T_M_1 - T_M_i)/10) -1) )

        CC_M_1, CC_M_2 = set_CC_Mat(icl_catel, beta, Vol, M_k, M_d, M_c, fat_k, fat_d, fat_c, sk_k, sk_d, sk_c, br_k, br_c, br_d,
                   rad_brain, rad_brain_skin, rad_brain_fat, rad_brain_inside, rad_body, rad_body_skin, rad_body_fat,
                   rad_body_inside)

        # reset outer clothing insulation
        icl_catel, facl, body_cover_1, body_cover_2, body_cover_3, br_sk_1, clo_1, clo_2, clo_3, clo_cap, clo_1_T, clo_2_T, clo_3_T, clo_cap_T, body_cover_arr = Icl_define(icl, I_a_M, br_sk_c)

        # reset effective temperature outer outer skin
        T_cl_in, T_cl_out, hr_M, T_sk_p, I_a_M, To_M, Icl_M, e_M, clo_air_in_M = set_Tcl_in(icl_catel, ta, tmrt, T_M_1, T_cl_out, hr_M, clo_air_in, hc, clo_1, clo_2, clo_3, clo_cap, e_sk, e_cl, feff, sigma)

        cl_re_in_M, cl_re_M, cl_re_t_M = set_cl_re_ISO7730(icl_catel, clo_1, clo_2, clo_3, clo_cap, evap, he, Re_factor, hr_M, clo_air_in, Icl_M)


        sw_M = sweating_mech_fiala_yung(icl_catel, T_M_1, body_cover_arr, adu, wetsk_s, sex)

        # Vapor pressure calculation by fiala
        VP_sk_s, VP_sk, wetsk_s, sk_wetted = vapor_mech_fiala(T_sk_p, sw_M, body_cover_arr, adu, vpa, evap, cl_re_t_M)

        # Ordnary concept for 1st Yung-Chang's revision
        VP_cl_in = VP_sk - (VP_sk - vpa) * cl_re_in_M / cl_re_t_M

        VP_cl_out = VP_sk - (VP_sk - vpa) *  cl_re_M / cl_re_t_M

        VP_cl_in_s = 6.1078 * np.exp(17.1 * T_cl_in / (235.0 + T_cl_in))

        VP_cl_out_s = 6.1078 * np.exp(17.1 * T_cl_out / (235.0 + T_cl_out))



        #
        RH_cl_in = VP_cl_in / VP_cl_in_s

        RH_cl_out = VP_cl_out/ VP_cl_out_s


        wet_energy = wet_energy_p(vpa, VP_sk, body_cover_arr, adu, cl_re_t_M)

        T_cl_in_eff = wet_To_mech(wet_energy, T_cl_in, clo_air_in_M, body_cover_arr, adu)

        # reset boundary elements of matrices
        T_boundary = set_boundary_T(icl_catel, T_core_i, T_M_1, T_cl_in_eff, M_k, sk_k, br_k, rad_brain, rad_brain_skin, rad_brain_inside,
                       rad_body, rad_body_skin, rad_body_inside)

        # reset temperature of blood pool
        bl_T_n = blood_T(icl_catel, T_M_1, body_cover_1, body_cover_2, body_cover_3, br_sk_c, br_sk_1)

        # apend temperature of blood pool for the backward body temperature profile in next time step
        T_M_1 = np.vstack((T_M_1, bl_T_n))

    tsk, tsk_mm, vpts, wetsk, sk_wetted_mm, tcl, fcl, enbal2, wet_sum, csum, rsum = energy_flux_PET(icl_catel, T_sk_p, wet_energy, ere, h, VP_sk, body_cover_arr, wetsk_s, sk_wetted, T_cl_in, T_cl_out, Icl_M, e_M,
                        To_M, adu, ta, vpa, tmrt, hc, feff, sigma)

    mPET = PETber(ta, p, tsk, tcl, wetsk, vpts, rtv, adu, fcl, e_sk, e_cl, sigma, feff, evap, cair, h0, enbal2)

    T_core =  T_M_1[0,0]
    return {"mPET": mPET,
            "T_core": T_core,
            "tsk_mm": tsk_mm,
            "tcl": tcl,
            "vpts": vpts,
            "wetsk": wetsk,
            "icl": icl,
            "sk_wetted_mm": sk_wetted_mm,
            "metabolic_rate": h,
            "wet_sum": wet_sum,
            "convective_flux": csum,
            "radiative_flux": rsum,
            "respiratory_flux": ere,
            "energy_balance": enbal2}
##End of PET_cal()

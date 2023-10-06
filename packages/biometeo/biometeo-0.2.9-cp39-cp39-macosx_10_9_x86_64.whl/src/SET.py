# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 05:09:44 2017

@author: bearsheep

This is calculation of SET* (Gagge et al., 1982)
"""
import math


def Gagge(TA, TR, RH, VEL, ACT, CLO, IHG, IWG):
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

    Output:
        SET: Standard Effective Temperature* (SET*) (C). 

    Using example:
        SET_v = SET_func.Gagge(Ta,Tmrt,RH,v,work,icl,ht,mbody) 

    """
    #     am 18.05.2010 hinzugefuegt, waren zuvor nicht initialisiert:
    err = -1
    error = -1
    #

    WK = 0.0
    PRSW = 0.0
    # unused parameters
    #  EPSH  = 0.98
    #  EPSG  = 1.00
    SIGMA = 0.0000000567

    #     Gagge, Fobelets and Berglund
    TTSK = 33.7
    TTCR = 36.8
    ALPHA = 0.1
    TTBM = ALPHA * TTSK + (1.0 - ALPHA) * TTCR
    #    Gagge, Nishi and Nevins
    CSW = 200.0
    CSTR = 0.5
    CDIL = 150.0
    #     Gagge, Fobelets and Berglund
    TSK = TTSK
    TCR = TTCR
    TBM = ALPHA * TSK + (1.0 - ALPHA) * TCR
    SKBFN = 6.3
    SKBF = SKBFN
    EV = 0.1 * ACT
    #  RH(%) -> RH(-)
    RH = 0.01 * RH

    CHCA = 5.66 * math.pow((58.2 * 1.1 / 58.2 - 0.85), 0.39)

    CHCV = 8.6 * math.pow(VEL, 0.53)

    if CHCV <= CHCA:
        CHC = CHCA
    else:
        CHC = CHCV

    if CHC < 3.0:
        CHC = 3.0

    FACL = 1.0 + 0.15 * CLO
    CHRx = 4.7
    CTC = CHC + CHRx
    to1 = (CHRx * TR + CHC * TA) / CTC
    CLOE = CLO - (FACL - 1.0) / (0.155 * FACL * CTC)
    FCLE = 1.0 / (1.0 + 0.155 * CTC * CLOE)
    FPCL = 1.0 / (1.0 + 0.143 * CHC * CLOE)

    TIM = 0.0
    TIME = 60.0 / 60.0

    while (TIM - TIME) <= 0:
        CLOE = CLO - (FACL - 1.0) / (0.155 * FACL * CTC)
        FCLE = 1.0 / (1.0 + 0.155 * CTC * CLOE)
        TCL = to1 + FCLE * (TSK - to1)
        CHRx = 0.8 * SIGMA * (TCL + TR + 273 * 2.0) * (math.pow(TCL + 273, 2) + math.pow(TR + 273, 2))
        CTC = CHRx + CHC
        to1 = (CHRx * TR + CHC * TA) / CTC
        SVPTA = math.exp(18.6686 - 4030.183 / (TA + 235.0))
        ERES = 0.0023 * ACT * (44.0 - RH * SVPTA)
        CRES = 0.0014 * ACT * (34.0 - TA)

        DRY = FCLE * CTC * (TSK - to1)
        # ***** SENSIBLE HEAT DRY1 AND RADIATION DRY2 *************
        DRY1 = CHC * (TCL - TA)
        DRY2 = CHRx * (TCL - TR)
        # *********************************************************
        ESK = EV - ERES
        HFSK = (TCR - TSK) * (5.28 + 1.163 * SKBF) - DRY - ESK
        HFCR = ACT - (TCR - TSK) * (5.28 + 1.163 * SKBF) - CRES - ERES - WK

        TCSK = 0.97 * ALPHA * IWG * 1.0
        TCCR = 0.97 * (1.0 - ALPHA) * IWG * 1.0
        AD = 0.008883 * math.pow(IWG * 1.0, 0.443) * math.pow(IHG * 1.0, 0.663)
        DTSK = (HFSK * AD) / TCSK
        DTCR = (HFCR * AD) / TCCR
        DTIM = 1.0 / 180.0
        # unknown DTBM
        #    DTBM  = ALPHA*DTSK+(1.0-ALPHA)*DTCR
        TIM = TIM + DTIM
        TSK = TSK + DTSK * DTIM
        TCR = TCR + DTCR * DTIM

        SKSIG = TSK - TTSK
        if SKSIG <= 0:
            COLDS = -SKSIG
            WARMS = 0
        else:
            COLDS = 0
            WARMS = SKSIG
        # end if loop

        CRSIG = TCR - TTCR
        if CRSIG <= 0:
            COLDC = -CRSIG
            WARMC = 0
        else:
            WARMC = CRSIG
            COLDC = 0
        # end if loop

        STRIC = CSTR * COLDS
        DILAT = CDIL * WARMC
        SKBF = (SKBFN + DILAT) / (1.0 + STRIC)

        # Gagge, Nishi and Nevins
        ALPHA = 0.04415 + 0.351 / (SKBF - 0.014)
        TBM = ALPHA * TSK + (1.0 - ALPHA) * TCR
        BYSIG = TBM - TTBM
        if BYSIG <= 0:
            COLDB = -BYSIG
            WARMB = 0
        else:
            WARMB = BYSIG
            COLDB = 0
        # end if loop

        REGSW = CSW * WARMB * math.exp(WARMS / 10.7)
        ERSW = 0.68 * REGSW
        SVPSK = math.exp(18.6686 - 4030.183 / (TSK + 235.0))
        SVPTA = math.exp(18.6686 - 4030.183 / (TA + 235))
        EMAX = 2.2 * CHC * (SVPSK - RH * SVPTA) * FPCL
        PRSW = ERSW / EMAX
        PWET = 0.06 + 0.94 * PRSW
        EDIF = PWET * EMAX - ERSW
        EV = ERES + ERSW + EDIF

        if (EMAX - ERSW) <= 0:
            EV = ERES + EMAX
            ERSW = EMAX
            EDIF = 0
            PRSW = 1
            PWET = 1
            # end if loop

            # end while loop
        #
    STORE = ACT - WK - CRES - EV - DRY
    AHSK = ACT - ERES - CRES - WK - STORE
    # *********** ADD TO ORIGINAL PROGRAM ***********************
    # HEAT TRANSFER INDICES IN REAL ENVIRONMENT
    CTC = CHRx + CHC
    to1 = (CHRx * TR + CHC * TA) / CTC
    CLOE = CLO - (1.09 - 1.0) / (0.155 * FACL * CTC)
    FCLE = 1.0 / (1.0 + 0.155 * CTC * CLOE)
    FPCL = 1.0 / (1.0 + 0.143 * CHC * CLOE)

    # ET* ( STANDARDIZED HUMIDITY/ REAL CLO, ATA AND CHC)
    # CALCULATION OF SKIN HEAT LOSS (AHSK)
    #
    # GET A LOW --------
    TACTS = TSK - AHSK / (CTC * FCLE)
    ET = TACTS

    while err < 0:
        SVPSK = math.exp(18.6686 - 4030.183 / (TSK + 235))
        SVPET = math.exp(18.6686 - 4030.183 / (ET + 235))
        err = AHSK - CTC * FCLE * (TSK - ET) - PWET * 2.2 * CHC * FPCL * (SVPSK - SVPET / 2.0)
        ET = ET + 0.1
        # end while loop

    # C  ADD TO ORIGINAL PROGRAM 

    # SET*
    # STANDARD ENVIRONMENT

    CHRS = CHRx
    CHCS = CHCA
    CLOS = 0.6
    FACLS = 1.09
    CTCS = CHRS + CHCS
    CLOES = CLOS - (FACLS - 1.0) / (0.155 * FACLS * CTCS)
    FCLES = 1.0 / (1.0 + 0.155 * CTCS * CLOES)
    FPCLS = 1.0 / (1.0 + 0.143 * CHCS * CLOES)
    TACTS = TSK - AHSK / (CTCS * FCLES)
    set1 = TACTS

    while error < 0:
        SVPSK = math.exp(18.6686 - 4030.183 / (TSK + 235))
        SVPSE = math.exp(18.6686 - 4030.183 / (set1 + 235))
        error = AHSK - CTCS * FCLES * (TSK - set1) - PWET * 2.2 * CHCS * FPCLS * (SVPSK - 0.5 * SVPSE)
        set1 = set1 + 0.1
    # end while loop


    return set1

# proc Gagge

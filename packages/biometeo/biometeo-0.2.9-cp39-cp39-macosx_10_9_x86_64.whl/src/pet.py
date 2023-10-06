# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 18:28:26 2017
@author: Yung-Chang Chen
This is a PET calculation script file.

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
sex # 1:male 2:female
pos # 1:standing 2:sitting

Output:
PET: Pysiologically Equivalent Temperature (C).
Tcor: core temperature of subject (C).
Tsk: skin temperature of subject (C). 
Tcl: clothing temperature of subject (C).
wsum: water volume loss from subject (g)
wetsk: skin wettedness.
h: metabolic rate (W/m^2).
Ere: respiratory energy fluxes  (W/m^2).
csum: convective energy fluxes (W/m^2). 
rsum: radiative energy fluxes (W/m^2).
ed: skin diffuse energy fluxes (W/m^2).
esw: swearing evaporative energy fluxes (W/m^2)
rcl: vapor resistance of clothing only for sweating evaporation. 

"""

import numpy as np
import math

def PET_cal(ta, vpa, v, tmrt, icl, work, ht, mbody, age, sex, pos):
    """Using example:
PET, Tcor, Tsk, Tcl, wsum, wetsk, h, ere, csum, rsum, ed, esw, rcl = PET_func.PET_cal(Ta, VP, v, Tmrt, icl, work, ht, mbody, age, sex, pos)

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
        sex # 1:male 2:female
        pos # 1:standing 2:sitting

       Output:
        PET: Pysiologically Equivalent Temperature (C).
        Tcor: core temperature of subject (C).
        Tsk: skin temperature of subject (C). 
        Tcl: clothing temperature of subject (C).
        wsum: water volume loss from subject (g)
        wetsk: skin wettedness.
        h: metabolic rate (W/m^2).
        Ere: respiratory energy fluxes  (W/m^2).
        csum: convective energy fluxes (W/m^2). 
        rsum: radiative energy fluxes (W/m^2).
        ed: skin diffuse energy fluxes (W/m^2).
        esw: swearing evaporative energy fluxes (W/m^2)
        rcl: vapor resistance of clothing only for sweating evaporation. 
    """
    def INKOERP(ta, vpa, p, work, ht, mbody, age, sex, eta):
        metbf = 3.19 * np.power(mbody, (3.0 / 4)) * (1. + 0.004 * (30.0 - age) +
                                                     0.018 * ((ht * 100. / (np.power(mbody, (1. / 3)))) - 42.1))
        metbm = 3.45 * np.power(mbody, (3.0 / 4)) * (1. + 0.004 * (30.0 - age) +
                                                     0.010 * ((ht * 100.0 / (np.power(mbody, (1. / 3)))) - 43.4))
        metm = work + metbm
        metf = work + metbf
        if (sex == 2):
            met = metf
        else:
            met = metm
        h = met * (1 - eta)

        # SENSIBLE RESPIRATIONS ENERGIE
        cair = 1.01 * 1000
        tex = 0.47 * ta + 21.0
        # rtv   := 1.44 * 10. ** (-6.) * met;
        rtv = 1.44 * np.power(10.0, -6) * met
        eres = cair * (ta - tex) * rtv
        # LATENTE RESPIRATIONSENERGIE
        # vpex  := 6.11 * 10. ** (7.45 * tex / (235. +tex));
        vpex = 6.11 * np.power(10.0, (7.45 * tex / (235.0 + tex)))
        erel = 0.623 * evap / p * (vpa - vpex) * rtv
        # SUMME DER ERGEBNISSE
        ere = eres + erel
        return h, ere, rtv, cair, erel

    # end of INKOERP

    def BERECH(ta, vpa, v, tmrt, icl, h, ht, mbody, sex, pos, ere, erel, fcl, emsk, emcl, sigm, rob, cb, evap, cair, p, food):
        # wetsk = 0.0
        if (pos == 2):    #sitting
            feff = 0.696
        elif (pos == 1):
            feff = 0.725  #standing
        adu = 0.203 * np.power(mbody, 0.425) * np.power(ht, 0.725)
        hc = 2.67 + (6.5 * np.power(v, 0.67))
        hc = hc * np.power((p / po), 0.55)

        # rcl = icl / 6.45
        facl = (- 2.36 + 173.51 * icl - 100.76 * np.sqrt(icl) + 19.28 * (np.power(icl, 3))) / 100

        if (facl > 1):
            facl = 1.0

        rcl = (icl / 6.45) / facl

        if (icl >= 2):
            y = 1.0
        if ((icl > 0.6) and (icl < 2)):
            y = (ht - 0.2) / ht
        if ((icl <= 0.6) and (icl > 0.3)):
            y = 0.5
        if ((icl <= 0.3) and (icl > 0)):
            y = 0.1

        r2 = adu * (fcl - 1. + facl) / (2.0 * np.pi * ht * y)
        r1 = facl * adu / (2.0 * np.pi * ht * y)
        di = r2 - r1

        r_ratio = (adu * (fcl - 1. + facl))/(facl * adu)
        if r_ratio < 1.15:
            r_ratio = 1.15

        # HAUTTEMPERATUREN
        for j in range(1, 8):
            tsk = 34.0
            count1 = 0
            tcl = (ta + tmrt + tsk) / 3
            count3 = 1
            enbal2 = 0.0

            while count1 < 3:
                acl = adu * facl + adu * (fcl - 1)
                rclo2 = emcl * sigm * (np.power((tcl + 273.2), 4) - np.power((tmrt + 273.2), 4)) * feff

                #  ln statt alog ??
                htcl = (6.28 * ht * y * di )/ (rcl * np.log(r_ratio) * acl)
                tsk = 1.0 / htcl * (hc * (tcl - ta) + rclo2) + tcl

                #  STRAHLUNGSSALDO
                aeff = adu * feff
                rbare = aeff * (1. - facl) * emsk * sigm * (np.power((tmrt + 273.2), 4) - np.power((tsk + 273.2), 4))
                rclo = feff * acl * emcl * sigm * (np.power((tmrt + 273.2), 4) - np.power((tcl + 273.2), 4))
                rsum = rbare + rclo

                #  KONVEKTION
                cbare = hc * (ta - tsk) * adu * (1.0 - facl)
                cclo = hc * (ta - tcl) * acl
                csum = cbare + cclo

                #  KERNTEMPERATUR
                c = [h + ere, adu * rob * cb, 18. -0.5 * tsk]
                c.append(5.28 * adu * c[2])
                c.append(0.0208 * c[1])
                c.append(0.76075 * c[1])
                c.append(c[3] - c[5] - tsk * c[4])
                c.append(- c[0] * c[2] - tsk * c[3] + tsk * c[5])
                c.append(c[6] * c[6] - 4. * c[4] * c[7])
                c.append(5.28 * adu - c[5] - c[4] * tsk)
                c.append(c[9] * c[9] - 4. * c[4] * (c[5] * tsk - c[0] - 5.28 * adu * tsk))

                # c[0] := h + ere;

                # c[1] := adu * rob * cb;

                # c[2] := 18. - 0.5 * tsk;

                # c[3] := 5.28 * adu * c[2];

                # c[4] := 0.0208 * c[1];

                # c[5] := 0.76075 * c[1];

                # c[6] := c[3] - c[5] - tsk * c[4];

                # c[7] := - c[0] * c[2] - tsk * c[3] + tsk * c[5];

                # c[8] := c[6] * c[6] - 4. * c[4] * c[7];

                # c[9] := 5.28 * adu - c[5] - c[4] * tsk;

                # c[10]:= c[9] * c[9] - 4. * c[4] *(c[5] * tsk - c[0] - 5.28 * adu * tsk);

                if (tsk == 36):
                    tsk = 36.010

                tcore = [0, 1, 2, 3, 4, 5, 6, 7]
                tcore[7] = c[0] / (5.28 * adu + c[1] * 6.3 / 3600) + tsk
                tcore[3] = c[0] / (5.28 * adu + (c[1] * 6.3 / 3600) / (1.0 + 0.5 * (34.0 - tsk))) + tsk
                if c[10] >= 0:
                    tcore[6] = (- c[9] - np.sqrt(c[10])) / (2.0 * c[4])
                    tcore[1] = (- c[9] + np.sqrt(c[10])) / (2.0 * c[4])
                elif c[8] >= 0:
                    tcore[2] = (- c[6] + np.sqrt(np.fabs(c[8]))) / (2.0 * c[4])
                    tcore[5] = (- c[6] - np.sqrt(np.fabs(c[8]))) / (2.0 * c[4])
                else:
                    tcore[4] = c[0] / (5.28 * adu + c[1] / 40.0) + tsk

                # TRANSPIRATION
                tbody = 0.1 * tsk + 0.9 * tcore[j]
                swm = 304.94 * (tbody - 36.6) * adu / 3600000.0

                tsk = np.round(tsk, decimals=3)

                vpts = 6.11 * math.pow(10.0, (7.45 * tsk / (235.0 + tsk)))

                if tbody <= 36.6:
                    swm = 0.0
                swf = 0.7 * swm
                if sex == 1:
                    sw = swm
                if sex == 2:
                    sw = swf

                eswphy = - sw * evap
                he = 0.633 * hc / (p * cair)
                fec = 1.0 / (1.0 + 0.92 * hc * rcl)
                eswpot = he * (vpa - vpts) * adu * evap * fec
                wetsk = eswphy / eswpot

                if wetsk > 1:
                    wetsk = 1

                eswdif = eswphy - eswpot

                if eswdif <= 0:
                    esw = eswpot
                if eswdif > 0:
                    esw = eswphy
                if esw > 0:
                    esw = 0

                # DIFFUSION
                rdsk = 0.79 * np.power(10.0, 7.0)
                rdcl = 0.0
                ed = evap / (rdsk + rdcl) * adu * (1 - wetsk) * (vpa - vpts)

                #  MAX VB
                vb1 = 34.0 - tsk
                vb2 = tcore[j] - 36.6
                if vb2 < 0:
                    vb2 = 0.
                if vb1 < 0:
                    vb1 = 0.

                vb = (6.3 + 75.0 * (vb2)) / (1.0 + 0.5 * vb1)

                #  ENERGIEBILANZ
                enbal = h + ed + ere + esw + csum + rsum + food

                #  KLEIDUNGSTEMPERATUR
                if (count1 == 0):
                    xx = 1.0
                if (count1 == 1):
                    xx = 0.1
                if (count1 == 2):
                    xx = 0.01
                if (count1 == 3):
                    xx = 0.001
                if (enbal > 0):
                    tcl += xx
                if (enbal < 0):
                    tcl -= xx

                if ((enbal <= 0) and (enbal2 > 0)):
                    if ((count1 == 0) or (count1 == 1) or (count1 == 2)):
                        count1 = count1 + 1
                        enbal2 = 0.0
                elif ((enbal >= 0) and (enbal2 < 0)):
                    if ((count1 == 0) or (count1 == 1) or (count1 == 2)):
                        count1 = count1 + 1
                        enbal2 = 0.0
                else:
                    enbal2 = enbal;
                    count3 = count3 + 1;
                    if (count3 > 200):
                        if ((count1 == 0) or (count1 == 1) or (count1 == 2)):
                            count1 = count1 + 1
                            enbal2 = 0.0
            ## End of while loop (count1 < 3)

            #  WASSERVERLUSTE
            ws = sw * 3600.0 * 1000.0
            if (ws > 2000):
                ws = 2000.0
            wd = ed / evap * 3600.0 * (-1000)
            wr = erel / evap * 3600.0 * (-1000)
            wsum = ws + wr + wd
            j1 = j

            if count1 == 3:
                if ((j == 2) or (j == 5)):
                    if (c[8] < 0):
                        break
                    if ((tcore[j] >= 36.6) and (tsk <= 34.050)):
                        if ((not (j == 4)) and (vb >= 91)):
                            break
                        if ((j == 4) and (vb < 89)):
                            break
                        if (vb > 90):
                            vb = 90
                    break
                if ((j == 6) or (j == 1)):
                    if (c[10] < 0):
                        break
                    if ((tcore[j] >= 36.6) and (tsk > 33.850)):
                        if ((not (j == 4)) and (vb >= 91)):
                            break
                        if ((j == 4) and (vb < 89)):
                            break
                        if (vb > 90):
                            vb = 90
                    break
                if (j == 3):
                    if ((tcore[j] < 36.6) and (tsk <= 34.000)):
                        if ((not (j == 4)) and (vb >= 91)):
                            break
                        if ((j == 4) and (vb < 89)):
                            break
                        if (vb > 90):
                            vb = 90
                    break
                if (j == 7):
                    if ((tcore[j] < 36.6) and (tsk > 34.000)):
                        if ((not (j == 4)) and (vb >= 91)):
                            break
                        if ((j == 4) and (vb < 89)):
                            break
                        if (vb > 90):
                            vb = 90
                    break
                if (j == 4):
                    if ((not (j == 4)) and (vb >= 91)):
                        break
                    if ((j == 4) and (vb < 89)):
                        break
                    if (vb > 90):
                        vb = 90
            # end of while if loop




        # end of for J = 1 to 7 loop
        return tcore[j], tsk, tcl, wetsk, esw, vpts, adu, facl, acl, csum, rsum, ed, wsum, feff, rdsk, rdcl, count1, j, enbal, enbal2, rcl

    # showmessage(floattostr(esw)+' '+inttostr(j1));
    # end of def BERECH

    def PETber(ta, tsk, tcl, wetsk, esw, vpts, rtv, adu, facl, acl, emsk, emcl, sigm, feff, rdsk, rdcl, cair, h):  # hie?zuvor nur PET
        tx = ta
        enbal3 = 0.0
        count2 = 0

        while count2 < 4:
            # 150
            hc = 2.67 + 6.5 * np.power(0.1, 0.67)
            hc *= np.power((p / po), 0.55)
            #      hc := 2.67 + 6.5 * 0.1 ** 0.67
            #      hc := hc * (p /po) ** 0.55
            #       STRAHLUNGSSALDO
            aeff = adu * feff

            rbare = aeff * (1. - facl) * emsk * sigm * (np.power((tx + 273.2), 4.0) - np.power((tsk + 273.2), 4))
            rclo = feff * acl * emcl * sigm * (np.power((tx + 273.2), 4.0) - np.power((tcl + 273.2), 4))
            rsum2 = rbare + rclo

            #       KONVEKTION
            cbare = hc * (tx - tsk) * adu * (1.0 - facl)
            cclo = hc * (tx - tcl) * acl
            csum2 = cbare + cclo

            #       DIFFUSION
            ed2 = evap / (rdsk + rdcl) * adu * (1.0 - wetsk) * (12.0 - vpts)
            #       ATMUNG
            tex = 0.47 * tx + 21.
            eres = cair * (tx - tex) * rtv
            # vpex = 6.11 * 10.0** (7.45 * tex / (235.0+ tex))
            vpex = 6.11 * np.power(10.0, (7.45 * tex / (235.0 + tex)))
            erel = 0.623 * evap / p * (12.0 - vpex) * rtv
            ere2 = eres + erel

            enbal = h + ed2 + ere2 + esw + csum2 + rsum2
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
                tx = tx - xx
            if (enbal < 0):
                tx = tx + xx
            if ((enbal <= 0) and (enbal3 > 0)):
                count2 += 1
            if ((enbal >= 0) and (enbal3 < 0)):
                count2 += 1

            enbal3 = enbal
        # end of PETber def
        return tx

    # *** eigentliche Funktion ***#

    eta = 0.0
    fcl = 1.15
    #      KONSTANTEN
    po = 1013.25
    p = 1013.25
    rob = 1.06
    cb = 3640
    food = 0.0
    emsk = 0.99
    emcl = 0.95
    evap = 2.42*np.power(10.0, 6.0)
    sigm = 5.67*np.power(10.0, -8.0)

    #Input = ta, vpa, p, work, ht, mbody, age, sex, eta
    Out_body = INKOERP(ta, vpa, p, work, ht, mbody, age, sex, eta)
    #Output = h, ere, rtv, cair, erel

    #Input = ta, vpa, v, tmrt, icl, h, ht, mbody, sex, pos, ere, erel, fcl, emsk, emcl, sigm, rob, cb, evap, cair, p, food
    #BERECH(ta, vpa, v, tmrt, icl, h, ht, mbody, sex, pos, ere, erel, fcl, emsk, emcl, sigm, rob, cb, evap, cair, p, food)
    Out_Cal = BERECH(ta, vpa, v, tmrt, icl, Out_body[0], ht, mbody, sex, pos, Out_body[1], Out_body[4], fcl, emsk, emcl, sigm, rob, cb, evap, Out_body[3], p, food)
    #Output = tcore[j], tsk, tcl, wetsk, esw, vpts, adu, facl, acl, csum, rsum, ed, wsum
    #Output = tcore[j][0], tsk[1], tcl[2], wetsk[3], esw[4], vpts[5], adu[6], facl[7], acl[8], csum[9], rsump[10], ed[11], wsum[12], feff[13], rdsk[14], rdcl[15], count1[16], j[17], enbal[18], enbal2[19], r_ratio[20]

    #Input = ta, tsk, tcl, wetsk, esw, vpts, rtv, adu, facl, acl, emsk, emcl, sigm, feff, rdsk, rdcl, cair, h
    Out_PET_Cal = PETber(ta, Out_Cal[1], Out_Cal[2], Out_Cal[3], Out_Cal[4], Out_Cal[5], Out_body[2], Out_Cal[6], Out_Cal[7], Out_Cal[8], emsk, emcl, sigm, Out_Cal[13], Out_Cal[14], Out_Cal[15], Out_body[3], Out_body[0])  # hie?zuvor nur PET

    #Output = PET, Tcor, Tsk, Tcl, wsum, wetsk, h, ere, csum, rsum, ed, esw

    return Out_PET_Cal, Out_Cal[0], Out_Cal[1], Out_Cal[2], Out_Cal[12], Out_Cal[3], Out_body[0], Out_body[1], Out_Cal[9], Out_Cal[10], Out_Cal[11], Out_Cal[4], Out_Cal[20]

    #return Out_body
    #return Out_Cal
# end of function of PET;
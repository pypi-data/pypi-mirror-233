#### import necessary library
import numpy as np
from fractions import Fraction

#### self define function for calculation of Tmrt
#### Calculation of Sonnenzeit
def Sonnenzeit(szeit,zeitzone,laenge, dayofyear): ## laenge: lontitude, zeitzone: timezone
    ## Erdrotationsstoerung
    def ERS(dayofyear):
        B = 2*np.pi*(dayofyear-81)/364
        sinB = np.sin(B)
        cosB = np.cos(B)
        Result = (9.87*np.sin(2*B)-7.53*cosB-1.5*sinB)/60
        return Result
    ## main function
    zonezeit = szeit+zeitzone-laenge*12/180-ERS(dayofyear)
    if zonezeit < 0:
        zzeit = zonezeit + 24.0
    elif zonezeit >=24:
        zzeit = zonezeit - 24.0
    else:
        zzeit = zonezeit
    s = zzeit-zeitzone+laenge*12/180+ERS(dayofyear)
    if s < 0:
        Result = s + 24.0
    elif s >=24:
        Result = s - 24.0
    else:
        Result = s
    return Result
#### Calculation of Solar Zenith Angle
def Zenitwinkel(szeit,breite,dayofyear):
    '''
    def deklin(dayofyear):
        Result = np.degrees(np.arcsin(0.3978*np.sin(np.radians(0.9856*dayofyear-2.72-77.51+1.92*np.sin(np.radians(0.9856*dayofyear-2.72))))))
        return Result
    delta = deklin(dayofyear)
    '''
    delta = np.degrees(np.arcsin(0.3978*np.sin(np.radians(0.9856*dayofyear-2.72-77.51+1.92*np.sin(np.radians(0.9856*dayofyear-2.72))))))
    sinBr = np.sin(np.radians(breite))
    cosBr = np.cos(np.radians(breite))
    sinD = np.sin(np.radians(delta))
    cosD = np.cos(np.radians(delta))
    s = np.degrees(np.arcsin(-cosBr*np.cos(szeit*np.pi/12)*cosD+sinD*sinBr))
    Result = 90-s
    return Result ## output zenit angle in degrees
#### Calculation of Solar Azimut Angle
def Azimutwinkel(szeit, breite, dayofyear):
    '''
    def deklin(dayofyear):
        Result=np.degrees(np.arcsin(0.3978*np.sin(np.radians(0.9856*dayofyear-2.72-77.51+1.92*np.sin(np.radians(0.9856*dayofyear-2.72))))))
        return Result
    '''
    def Winkel(Ankathete,Gegenkathete,Gradmass): #Gradmass ist boolean
        if Gegenkathete==0:
            if Ankathete>=0:
                phi=0
            else:
                phi=np.pi
        elif Gegenkathete>0:
            phi=np.pi/2-np.arctan(Ankathete/Gegenkathete)
        else:
            phi=3*np.pi/2-np.arctan(Ankathete/Gegenkathete)
        if Gradmass:
            phi=np.degrees(phi)
        return phi
    #delta = deklin(dayofyear)
    delta = np.degrees(np.arcsin(0.3978*np.sin(np.radians(0.9856*dayofyear-2.72-77.51+1.92*np.sin(np.radians(0.9856*dayofyear-2.72))))))
    ## get sin(breite), cos(breite), sin(delta), cos(delta), sin(szeit*pi/12), cos(szeit*pi/12)
    sinBr = np.sin(np.radians(breite))
    cosBr = np.cos(np.radians(breite))
    sinD = np.sin(np.radians(delta))
    cosD = np.cos(np.radians(delta))
    sinSz = np.sin(szeit*np.pi/12)
    cosSz = np.cos(szeit*np.pi/12)
    sy = -sinSz*cosD
    sz = sinBr*cosSz*cosD+sinD*cosBr
    Result = Winkel(sz,-sy,True)
    return Result ## output azimut angle in degrees
#### Turbidity Forcing
def LinkeTruebung(dayofyear, breite, RH): #breite ist latitude auf Englisch
    if RH < 85:
    ## KondratYew (1977):
        if breite>=0 :
            Tl = 2.9-1.4*np.cos(2*np.pi*(dayofyear-15)/365)
        else:
            Tl = 2.9+1.4*np.cos(2*np.pi*(dayofyear-15)/365)
        ## end of if loop
    else: ##foggy
        if RH < 100 :
            Vm = np.maximum(1, 15*(1-np.exp(-(np.power(100-RH,4))/(np.power(100-90,4)))))
        else:
            Vm = 1
        ## end of if loop
        Tl = 0.84+39/Vm  ## VDI
    ##end of if loop
    return Tl
#### Calculation of relative optical air mass
def RelOptLuftmasse(zenitwinkel): ## input zenit angle in degrees
    ##const
    a = 0.50572
    b = 6.07995
    c = 1.6364
    Tabm = np.array([37.92, 39.22, 40.34, 41.48, 42.63, 43.72, 44.81, 45.90, 47.00, 48.08, 49.15, 50.12])
    i = int(np.trunc(zenitwinkel*10-900))
    if (0<=zenitwinkel) and (zenitwinkel<=91):
        if zenitwinkel<90:
            if zenitwinkel<80:
                m = 1/np.cos(np.radians(zenitwinkel))
            else:
                m = 1/(np.cos(np.radians(zenitwinkel))+a*np.power(90-zenitwinkel+b,-c))
        else:
            m = Tabm[i]+Fraction(zenitwinkel*10)*(Tabm[i+1]-Tabm[i])
    else:
        m = 999 ## 999?? or NaN?
    return m
#### Calculation of the max direct radiation
def MaxDirekteStrahlung(dayofyear, mHoehe, zenitwinkel, LinkeTr, RelOptLuftM): ## input zenit angel in degrees
    def ExtraterrStrahlung(dayofyear):
        S0 = 1367 ## (W/m^2)  Solarkonstante
        Result = S0*(1+0.03344*np.cos(np.pi/180*(0.9856*dayofyear-2.72)))
        return Result
    def OptDicke(zenitwinkel, RelOptLuftM):
        if (0<=zenitwinkel) & (zenitwinkel<91):
            if zenitwinkel<85:
                rho=1/(9.4+0.9*RelOptLuftM)
            else:
                rho=0.0408+0.0028*(90-zenitwinkel) ## KondratYev
        else:
             rho=999 ## 999?? or NaN?
        return rho
    def Druckkorrektur(Hoehe):
        Result=np.exp(-Hoehe/8434.5)
        return Result
    ## Main function
    if zenitwinkel<90:
        Isenkr = ExtraterrStrahlung(dayofyear)*np.exp(-LinkeTr*OptDicke(zenitwinkel, RelOptLuftM)*RelOptLuftM*Druckkorrektur(mHoehe))
    else:
        Isenkr = 0
    return Isenkr
#### Calculation of the max global radiation
def MaxGlobalstrahlung(dayofyear, mHoehe, zenitwinkel, LinkeTr): ## input zenit angel in degrees
    def ExtraterrStrahlung(dayofyear):
        S0 = 1367 ## (W/m^2)  Solarkonstante
        Result = S0*(1+0.03344*np.cos(np.pi/180*(0.9856*dayofyear-2.72)))
        return Result
    def Druckkorrektur(Hoehe):
        Result=np.exp(-Hoehe/8434.5)
        return Result
    ##Main function
    if zenitwinkel<90:
        Gmax = 0.84*ExtraterrStrahlung(dayofyear)*np.cos(np.radians(zenitwinkel))*np.exp(-0.027*Druckkorrektur(mHoehe)*LinkeTr/np.cos(np.radians(zenitwinkel)))
    else:
        Gmax = 0
    return Gmax
#### Calculation of direct radiation with clouds
def DirStrMBew(Imax, N):
    Result = Imax*(1-(N/8))
    return Result
#### Calculation of current diffusion radiation with clouds
def TatDiffStrMBew(Isenkr, Dmax, Gmax, N, OmegaF, verdeckt):# verdeckt or nicht: boolean, N: the amount of partial of could, OmegaF: sky view factor
    S0 = 1367 ## (W/m^2)  Solarkonstante
    isotrop = Dmax*(1-(Isenkr/S0))*OmegaF
    if verdeckt:
        anisotrop = 0.2*Gmax # =0 bis 17.01.00
    else:
        anisotrop = Dmax*Isenkr/S0
    Dbeschr0 = isotrop+anisotrop
    Dfrei8 = Gmax*(1-0.72)
    Result = Dbeschr0*(1-(N/8))+(N/8)*Dfrei8*OmegaF
    return Result
#### Calculation of reflective shortwave radiation
def AtmosGegenstr(LuftTemp, Dampfdruck , N):
    epseff = 9.9E-6
    sigma = 5.67E-8  ## W/(m^2*K^4)  Stefan-Boltzmann-Konstante
    T = LuftTemp+273.15
    ## Kasten:
    '''
    A0 =epseff*sigma*np.power(T,6);
    aL = 2.30-0.00737*T
    aM = 2.48-0.00823*T
    aH = 2.89-0.01*T
    nx = np.power(N/8,2.5)
    Result = A0*(1+aL*nx+(1-N/8)*aM*nx+(1-N/8)*(1-N/8)*aH*nx)
    '''
    ## Angstrˆm bisher (VDI):
    A0 =sigma*np.power(T,4)*(0.82-0.25*np.power(10,-0.0945*Dampfdruck))
    nx =np.power(N/8,2.5)
    Result =A0*(1+0.21*nx)
    ## Angstrˆm neu (VP in Torr):
    '''
    A0 =sigma*np.power(T,4)*(0.79-0.174*np.power(10,-0.055*Dampfdruck*133.3))
    nx = np.power(N/8,2.5)
    Result =A0*(1+0.21*nx)
    '''
    ## Sridhar & Elliott (2002):
    '''
    A0 = 1.31*sigma*np.power(T,4)*np.power(10*Dampfdruck/T, 1/7) ## VP in kPa => 10*VP in hPa
    nx = np.power(N/8,2.5)
    Result = A0*(1+0.21*nx)
    '''
    return Result
#### Calculastion of relfective longwave radiation
def Waermestr(LwOben, OberflTemp, eps):
    sigma = 5.67E-8  ## W/(m^2*K^4)  Stefan-Boltzmann-Konstante
    Ea = (1-eps)*LwOben
    Ek = eps*sigma*np.power(273.15+OberflTemp,4)
    Result = Ea+Ek
    return Result
#### Calculation of surface temperature
def OberflTemp(Strahlungsbilanz, LuftTemp, WindGeschw, Bowen):
    Q = Strahlungsbilanz
    ## Bodenwaerme
    if Q > 0:
        B = -0.19*Q
    else:
        B = -0.32*Q
    ##
    alphaL = 6.2+4.26*WindGeschw
    if Bowen <-0.9:
        Bowen = -0.9
    if Bowen == 0:
        Result = LuftTemp
    else:
        Result =LuftTemp+(Q+B)/(alphaL*(1+1/Bowen))
    return Result
#### Basic calculation of mean radiant temperature
def MittlStrTemp(zenitwinkel,EStrOben,EStrUnten,AGegenstr,DiffStr,MaxDirStr,ReflStr,albedo, albedo_env):
    ## alphaIR=0.7;  ## 1-Albedo des Menschen
    sigma = 5.67E-8  ## W/(m^2*K^4)  Stefan-Boltzmann-Konstante
    epsP = 0.97  ## Emissionskoeff. des Menschen
    alphaIR = 1-albedo ## 1-Albedo des Menschen
    gamma = 90-zenitwinkel
    ## fP could be problem to calculate a steady Tmrt
    fP = 0.308*np.cos(np.radians(gamma*(0.998-np.sqrt(gamma)/50000)))
    #fP_zeta = 0.308*np.cos(np.radians(zenitwinkel*(0.998-np.sqrt(zenitwinkel)/50000)))

    ## fP from Parl and Tuller 20111
    #fP = 3.01E-7*np.power(gamma,3)-6.46E-5*np.power(gamma,2)+8.34E-4*gamma+0.298
    #print(gamma)
    #print(fP)
    ## Another formula is shown in RayMan
    #Result = np.power( np.power(OberflTemp+273.15,4)*(1-OmegaF/2)+AGegenstr*(OmegaF/2)/sigma+alphaIR/(sigma*epsP)*(DiffStr*OmegaF/2+MaxDirStr*fP+ReflStr*(1-OmegaF/2)) ,0.25) -273.15
    #Result = np.power((EStrOben+EStrUnten+AGegenstr)/sigma+alphaIR/(sigma*epsP)*(DiffStr+MaxDirStr*fP+ReflStr),0.25) - 273.15
    Result = np.power(((EStrOben+EStrUnten+AGegenstr)+(alphaIR/epsP)*(DiffStr+MaxDirStr*fP))/sigma,0.25) - 273.15
    ### Daunter sind all falsche Testen 2022.05.02
    #Result = np.power((EStrOben+EStrUnten+AGegenstr)/sigma+alphaIR/(sigma*epsP)*(DiffStr+MaxDirStr*fP+albedo_env*DiffStr),0.25) - 273.15
    #Result = np.power((EStrOben+EStrUnten+AGegenstr)/sigma+alphaIR/(sigma*epsP)*(DiffStr+MaxDirStr*fP+ReflStr*((np.cos(np.radians(gamma))+np.sin(np.radians(gamma)))-1)*0.15),0.25) - 273.15
    #Result = np.power((EStrOben+EStrUnten+AGegenstr)/sigma+alphaIR/(sigma*epsP)*(DiffStr+MaxDirStr*fP+ReflStr*(np.sqrt(np.cos(np.radians(gamma))*np.sin(np.radians(gamma))))),0.25) - 273.15
    #Result = np.power((EStrOben+EStrUnten+AGegenstr)/sigma+alphaIR/(sigma*epsP)*(DiffStr+MaxDirStr*fP+ReflStr*fP),0.25) - 273.15
    ## question: the ReflStr has been removed in RayMan 2022.04.27
    return Result
#### Calculation of mean radiant temperature with global radiation, partial of cloud cover, or sky view factor von RayMan
def Geodat_Strahlung(uhrzeit, zeitzone, laenge, br, mHoehe, tg, Ta, Vp, RH, Vwind, N, G, DGratio, Tob, Tm, ltf, OmegaF, alb, albhum, RedGChk, foglimit, bowen):
    """Using function Geodat_Strahlung. Input variables are following.
        Uhrzeit: 0.0 to 23.xx hours of day                                                                                                                                                                                   
        zeitzone: time zone
        aenge: lontitude
        br: latitude
        mHoehe: sea level heigt in m, 
        tg: day of the year                                                                                                      
        Ta: air temperature in degree C
        Vp: vapor pressure in hPa
        RH: relative humidity in %
        Vwind: wind speed in m/s                                                                                                   
        N: cloud cover in 0 to 8 (oct)
        G: global radiation in (w/m^2)
        DGratio: ratio of diffuse and global (default is NaN, normal value is 0.15 or 0.2 to 0.x)
        Tob: surface temperature in degree C
        Tm: mean radiant temperature in degree C
        ltf: "Linke turbidity" (default is NaN) 
        OmegaF: sky view factor in 0.0 to 1.0 (clear sky is 1.0)
        alb: "Albedo of the surrounding" (default is 0.3)
        albhum:"Albedo of the human being" (default is 0.3)
        RedGChk: "Reduction of G presetting by obstacles" in boolean, 
        foglimit: "Lower limit of rel. humidity (%) for full diffuse radiation" (default is 90) 
        bowen: Bowen ratio (default is 1.0)
        Output variables are following.
        Imax: maximum of directional solar radiation in W/m^2
        Gmax: maximum of global radiation in W/m^2
        Dmax: maximum of diffuse solar radiation in W/m^2
        Itat: current directional solar radiation in W/m^2
        Gtat: current global radiation in W/m^2
        Dtat: current diffuse solar radiation in W/m^2
        A: atmospheric long wave radiation in W/m^2 
        Eu: upward long wave radiation in W/m^2
        Es: downward long wave radiation in W/m^2

        Using example:
        Imax, Gmax, Dmax, Itat, Gtat, Dtat, A, Eu, Es, Tob, Tmrt  = Geodat_Strahlung(uhrzeit, zeitzone, laenge, br, mHoehe, tg, Ta, Vp, RH, Vwind, N, G, DGratio, Tob, Tm, ltf, OmegaF, alb, albhum, RedGChk, foglimit, bowen)

    """
    ## Calculation of solar time
    woz = Sonnenzeit(uhrzeit,zeitzone,laenge,tg)
    ## Calculation of zenit and azimut angle at
    zeta = Zenitwinkel(woz, br, tg)
    alpha = Azimutwinkel(woz, br, tg)
    ## Ingore the following code, because there is no obstacle to be considered
    ## Only check if the zeta is over 90 degree such as in polar region during the winter
    ''' 
    if (zeta<90) and (ObjBmp.Canvas.Pixels[Radius+Round(Radius*(zeta/90*sin(DegToRad(alpha)))),Radius-Round(Radius*(zeta/90*cos(DegToRad(alpha))))]=clWhite)
        then verd:=False  ##becomes false if direct radiation, true if sun is covered by obstacle
    else verd:=True;
    '''
    if zeta<90:
        verd = False
    else:
        verd = True

    ## Linke Turbidity Forcing
    if np.isnan(ltf):
        ltf = LinkeTruebung(tg,br, RH)
    ## calculation of max direct radiation & global radiation
    RelOptLuftM = RelOptLuftmasse(zeta)
    Isenkr = MaxDirekteStrahlung(tg, mHoehe, zeta, ltf, RelOptLuftM) ## zenith angle = 90 degree
    Gmax = MaxGlobalstrahlung(tg, mHoehe, zeta, ltf)
    Imax = Isenkr*np.cos(np.radians(zeta)) ## with local and current zenith angel
    Dmax = Gmax - Imax ## calculate the max diffuse radiation

    ## check the dataset of all short wave radiation
    if not np.isnan(G): ## falls G vorgegeben
        if np.isnan(DGratio): ## DGratio autom. bestimmen
            if (Gmax > 0 ) and (G/Gmax<0.8):
                DGratio = 1-G/Gmax
            else:
                DGratio = 0.2
        ## end of check the D/G ratio
        if (RedGChk and verd): ## falls Vorgabe von G reduziert wird
            Dtat = DGratio*OmegaF*G       ## ... nicht verdeckt
            Gtat = Dtat
            Itat = 0.0
        else:
            if verd: ## falls Vorgabe von G nicht reduziert wird
                Gtat = G
                Dtat = Gtat
                Itat = 0.0
            else:
                Gtat = G
                Dtat = DGratio*OmegaF*Gtat
                Itat = Gtat-Dtat
        ##G:=nopreset  ## Check if G is not needed otherwise!
        G = np.nan
    else: ## falls G nicht vorgegeben
        ## give direct radiation
        if (verd) or (RH > foglimit):
            Itat = 0
        else:
            Itat = DirStrMBew(Imax,N)
        ## give diffuse radiation
        if (RH > foglimit): ## bei Nebel
            Dtat=0.5*TatDiffStrMBew(Isenkr,Dmax,Gmax,N,OmegaF,verd)
        else:
            Dtat=TatDiffStrMBew(Isenkr,Dmax,Gmax,N,OmegaF,verd)
        Gtat = Itat + Dtat
        ## vvv ## auf Verlangen von Andreas am 08.03.2006 eingef¸gt:
    ## end of check all short wave radiations

    ## check all long wave radiations
    A = AtmosGegenstr(Ta,Vp,N)
    Es = Waermestr(A,Ta,0.95)   ## Einstrahlung von der Seite

    if np.isnan(Tob):
        Toberfl = Ta
        for i in range(1,12,1):             ## Iteration
            Eu = Waermestr(A*OmegaF+Es*(1-OmegaF),Toberfl,0.95)  ## Einstrahlung von unten
            ##     1-albedo=0.2 bis 28.06.2007,
            ##     aber zuerst nur alb*G als 1. Term, ab 04.08.2007 dann richtig (1-alb)*G+...:
            ##     Toberfl:=OberflTemp(0.8*Gtat+A*OmegaF+Es*(1-OmegaF)-Eu,Ta,Vwind,FormVorgaben.bowen);
            Toberfl = OberflTemp((1-alb)*Gtat+A*OmegaF+Es*(1-OmegaF)-Eu,Ta, Vwind, bowen)
        Tob = Toberfl
    else:
        Eu = Waermestr(A*OmegaF+Es*(1-OmegaF),Tob,0.95)      ## Emissionskoeff.!!!
    ## end of check Eu and Tob
    ## Calculation of Tmrt
    if np.isnan(Tm): ## if the Tmrt is not given then calculate it
        ##  albedo=0.2 bis 04.07.2007:
        ##  then Tmrt:=MittlStrTemp(zeta,Es*(1-OmegaF)/2,Eu/2,A*OmegaF/2,Dtat,Itat,0.2*Gtat,FormVorgaben.albedo)
        if zeta > 90:
            zeta = 90  ## set a limitation of zenith angle for calculation
        Tmrt =MittlStrTemp(zeta,Es*(1-OmegaF)/2,Eu/2,A*OmegaF/2,Dtat,Itat,alb*Gtat,albhum, alb)
    else:
        Tmrt = Tm
        ##Tm = np.nan
    return Imax, Gmax, Dmax, Itat, Gtat, Dtat, A, Eu, Es, Tob, Tmrt
    #### vars: Kurzwellige Einstrahlung (max), Globalstrahlung (max), Diffuse Strahlung (max), alle tats‰chlich,
    ####       Atmosph‰rische Gegenstrahlung, Einstrahlung von der Seite und von unten, Oberfl‰chentemperatur, Tmrt
    #### Tob und Tmrt sind result
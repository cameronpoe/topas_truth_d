import numpy as np
import scipy as scp
from scipy import integrate
import matplotlib.pyplot as plt



def jablonskyMap(CBT,CBP, time):

    # units: 1/ps
    # Constants:
    radiusTol = 3.18/20000000000. #meter
    radiusBP = 8.04/20000000000.
    radiusBT = 10.72/20000000000.

    molarMassTol = 92.14 # g/mol
    molarMassBT = 468.5 # g/mol
    molarMassBP = 182.22 # g/mol

    densityToluene = 0.8621 # g/cm3
    viscosityToluene =  0.56 /1000 # pa.s

    Na = 6.02214086 * 10**23
    Kb = 1.380649 * 10**(-23)
    T = 25 + 273.15

    # Knobs:
    volume = .000001 # m3
    concentrationBT = 10.**(CBT) #M
    concentrationBP = 10.**(CBP) #M

    tolueneC = densityToluene*Na*1000000/molarMassTol # molecules/m3
    btC = concentrationBT*Na*1000 # molecules/m3
    bpC = concentrationBP*Na*1000 # molecules/m3

    muTolBT = molarMassTol*molarMassBT/(molarMassBT + molarMassTol)/(Na*1000) #kg
    muTolBP = molarMassTol*molarMassBP/(molarMassBP + molarMassTol)/(Na*1000) #kg
    muBPBT = molarMassBP*molarMassBT/(molarMassBT + molarMassBP)/(Na*1000) #kg

    sigmaTolBT = radiusTol+radiusBT
    sigmaTolBP = radiusTol+radiusBP
    sigmaBPBT = radiusBP+radiusBT

    k_col_tol_bt = sigmaTolBT**2 * np.sqrt(8*np.pi*Kb*T/muTolBT)*tolueneC*btC*volume # collisions per second
    k_col_tol_bp = sigmaTolBP**2 * np.sqrt(8*np.pi*Kb*T/muTolBP)*tolueneC*bpC*volume
    k_col_bp_bt = sigmaBPBT**2 * np.sqrt(8*np.pi*Kb*T/muBPBT)*bpC*btC*volume


    #print(sigmaTolBT**2, np.sqrt(8*np.pi*Kb*T/muTolBT),tolueneC,btC,volume,1000000000000)

    #print("print(k_col_tol_bt, k_col_tol_bp, k_col_bp_bt)")
    #print(k_col_tol_bt, k_col_tol_bp, k_col_bp_bt)

    # Toluene
    k_f_tol =  4.7*1000000 # 10.1063/1.443140
    #2.6*(10**7)  # https://omlc.org/spectra/PhotochemCAD/html/090.html * #Baxendale 1973
    k_dc_tol = 0
    k_isc_tol = 8.5*1000000 # 10.1063/1.443140

    k_ss_tol_bt =  5.4*(10**10)*concentrationBT #Baxendale 1973  # ASSUMPTION NAPHTALENE MAY WANT TO TRY 0
    k_st_tol_bt =  0 #Baxendale 1973
    k_st_tol_bp =  0
    k_ss_tol_bp =  5.4*(10**10)*concentrationBP #Baxendale 1973 # ASSUMPTION NAPHTALENE

    k_ph_tol = 3.45*100000
    k_dph_tol = 0

    k_ts_tol_bt =  0
    k_tt_tol_bt = 0
    k_ts_tol_bp = 0
    k_tt_tol_bp = 1.1*(10**10)*concentrationBP #Baxendale 1973

    # BP
    k_f_bp = 0 # https://pubs.rsc.org/en/content/articlelanding/2018/cp/c8cp01023d#cit54
    #1.7*(10**6) # https://pubs.acs.org/doi/pdf/10.1021/ja00184a047
    k_dc_bp = 0
    k_isc_bp = 3.3*(10**10) #Handbook of photophysical chemistry pg 16

    k_ss_bp_bt =  0
    k_st_bp_bt =  0

    k_ph_bp = 2*10000 #Baxendale 1973
    #1.6*100 #https://pubs.acs.org/doi/pdf/10.1021/ja00184a047
    k_dph_bp = 0

    k_ts_bp_bt =  0
    k_tt_bp_bt =  2.7*(10**6)*concentrationBT/(10**(-3)) # From Murata 2015, Xanthone to BT, not BTFO

    maxK = np.amax([k_f_tol ,k_dc_tol,k_isc_tol ,k_ss_tol_bt ,k_st_tol_bt,k_st_tol_bp ,k_ss_tol_bp,k_ph_tol ,
                  k_dph_tol ,k_ts_tol_bt,k_tt_tol_bt ,k_ts_tol_bp ,k_tt_tol_bp ,k_f_bp ,k_dc_bp ,k_isc_bp ,
                  k_ss_bp_bt ,k_st_bp_bt ,k_ph_bp ,k_dph_bp ,k_ts_bp_bt ,k_tt_bp_bt])

    def solver(t,vec):
        S1_tol = vec[0]
        T1_tol = vec[1]
        S0_tol = vec[2]
        S1_bp = vec[3]
        T1_bp = vec[4]
        S0_bp = vec[5]
        S1_bt = vec[6]
        T1_bt = vec[7]

        dS1_tol = S1_tol*(-(k_f_tol + k_dc_tol +k_isc_tol +k_ss_tol_bt +k_ss_tol_bp +k_st_tol_bt +k_st_tol_bp))
        dT1_tol = S1_tol*k_isc_tol + T1_tol*(-(k_ph_tol+k_dph_tol +k_ts_tol_bt+k_ts_tol_bp +k_tt_tol_bt +k_tt_tol_bp ))
        dS0_tol = S1_tol*(k_f_tol + k_dc_tol) + T1_tol*(k_ph_tol+k_dph_tol)
        dS1_bp = S1_tol*(k_ss_tol_bp) + T1_tol*(k_ts_tol_bp) - S1_bp*(k_f_bp + k_dc_bp+ k_isc_bp + k_ss_bp_bt + k_st_bp_bt )
        dT1_bp = S1_tol*(k_st_tol_bp)+ T1_tol*(k_tt_tol_bp)+ S1_bp*(k_isc_bp) - T1_bp*(k_ph_bp +k_dph_bp +k_ts_bp_bt +k_tt_bp_bt )
        dS0_bp = T1_bp*(k_ph_bp +k_dph_bp) +  S1_bp*(k_f_bp + k_dc_bp)
        dS1_bt = S1_tol*(k_ss_tol_bt) + T1_tol*(k_ts_tol_bt)+S1_bp*(k_ss_bp_bt) + T1_bp*(k_ts_bp_bt)
        dT1_bt = S1_tol*(k_st_tol_bt) + T1_tol*(k_tt_tol_bt)+S1_bp*(k_st_bp_bt) + T1_bp*(k_tt_bp_bt)

        return (dS1_tol,dT1_tol ,dS0_tol ,dS1_bp ,dT1_bp ,dS0_bp,dS1_bt,dT1_bt   )

    picosecond = 10**(-12)
    xi = 0
    xf = picosecond*time

    initialConditions = [2250,4000,0,0,0,0,0,0]

    times = np.arange(xi, xf, xf/1000) # domain
    solution = integrate.solve_ivp(solver, [xi,xf], initialConditions  ,t_eval = times, method = 'LSODA') # 'RK23'  'LSODA'
    x = solution.t
    y = solution.y
    S1_tol = y[0]
    T1_tol = y[1]
    S0_tol = y[2]
    S1_bp = y[3]
    T1_bp = y[4]
    S0_bp = y[5]
    S1_bt = y[6]
    T1_bt = y[7]
    print((S1_bt+T1_bt)[-1])

    '''print("here")
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_axes([0.1,0.1,0.7,0.9])
    ax.plot(x, S1_tol, label = "S1_tol")
    ax.plot(x, T1_tol, label = "T1_tol")
    ax.plot(x, S0_tol, label = "S0_tol")
    ax.plot(x, S1_bp, label = "S1_bp")
    ax.plot(x, T1_bp, label = "T1_bp")
    ax.plot(x, S0_bp, label = "S0_bp")
    ax.plot(x, S1_bt, label = "S1_bt")
    ax.plot(x, T1_bt, label = "T1_bt")
    ax.legend()
    print("here")
    plt.show()
    #plt.savefig("output2.png")'''
    return S1_bt[-1], T1_bt[-1]


time = 10.**(6) # Time in picoseconds
CBT = np.arange(-7, 0, 0.5)
CBP = np.arange(-7,0,0.5)
map = np.zeros(shape = (len(CBT),len(CBP)))
mapS = np.zeros(shape = (len(CBT),len(CBP)))
mapT = np.zeros(shape = (len(CBT),len(CBP)))
for i in range(len(CBT)):
    for j in range(len(CBP)):
        result = jablonskyMap(CBT[i],CBP[j], time)
        map[i,j] = result[0] + result[1]
        mapS[i,j] = result[0]
        mapT[i, j] =  result[1]
fig, (ax1,ax2,ax3) = plt.subplots(1,3,figsize=(18,6))
c = ax1.pcolor(CBP, CBT,map, cmap = "YlGn")
ax1.set_xlabel("p[BP]")
ax1.set_ylabel("p[BTFO]")
ax1.set_title("All")
fig.colorbar(c, ax=ax1)

d = ax2.pcolor(CBP, CBT,mapS, cmap = "YlGn")
ax2.set_xlabel("p[BP]")
ax2.set_ylabel("p[BTFO]")
ax2.set_title("Singlets")
fig.colorbar(d, ax=ax2)

e=  ax3.pcolor(CBP, CBT,mapT, cmap = "YlGn")
ax3.set_xlabel("p[BP]")
ax3.set_ylabel("p[BTFO]")
ax3.set_title("Triplets")
fig.colorbar(e, ax=ax3)

plt.show()
# Import standard Python packages
import numpy as np
import matplotlib.pyplot as plt
#import NuPy modules
import omega_plus as omega_plus
from NuPyCEE import chem_evol
from NuPyCEE import omega
from NuPyCEE import sygma
from NuPyCEE import stellab
from solar_Mg_Fe_abundances import *

#Kroupa imf

imf_type = 'kroupa'
imf_bdys = [0.1, 100]
alphaimf = 1.35
imf_yields_range = [0,40]


table = 'yield_tables/agb_and_massive_stars_K10_K06_0.5HNe.txt'
exp_infall = [[100/2.2, 0.0, 0.8e9], [13.0/2.2, 1.0e9, 7.0e9]] #from 'best' model

sn1a_table = 'yield_tables/sn1a_i99_W7.txt'

#ivo_sn1a_table = 'yield_tables/sn1a_ivo13_stable_z.txt'

#standard model afterwards
kwargs = {"special_timesteps":150, "t_star":1.0, "table":table, "mgal":1.0,
          "m_DM_0":1.0e12, "sfe":2.3e-10, "mass_loading":0.52, "imf_type": imf_type, "imf_bdys": imf_bdys, "alphaimf": alphaimf,
          "imf_yields_range":imf_yields_range, "sn1a_table":sn1a_table, "sn1a_rate": 'power_law'}

o_res = omega_plus.omega_plus(exp_infall = exp_infall, beta_pow = -1.3, **kwargs)
#o_res2 = omega_plus.omega_plus(exp_infall = exp_infall, beta_pow = -1.3, nb_1a_per_m = 1.0e-4, **kwargs)
#o_res3 = omega_plus.omega_plus(exp_infall = exp_infall, beta_pow = -1.3, nb_1a_per_m = 1.0e-2, **kwargs)

def SFR_time(sim):
    t = np.array(sim.inner.history.age)/1.0e9
    plt.plot(t[:-1], sim.inner.history.sfr_abs[:-1], label = "SFR")
    plt.xlabel("Galactic age[Gyr]", fontsize=15)
    plt.ylabel('SFR [M$_\odot$ yr$^{-1}$]', fontsize = 15)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend()
    plt.show()
    return(True)


def age_metallicity(t, Fe_H):
    plt.plot(np.array(t)/1e9, Fe_H, '-b', linewidth = 1.5, label = "Metallicity vs age")
    plt.plot([(13-4.6), (13-4.6)], [-10, 10], ':', color = 'cornflowerblue', alpha = 0.7)
    plt.plot([-1e10, 1e10], [0,0], ':', color = 'cornflowerblue', alpha = 0.7)
    plt.xlim(-0.3, 13.5)
    plt.ylim(-2.0, 0.7)
    plt.ylabel('[Fe/H]', fontsize = 15)
    plt.xlabel('Galactic age[Gyr]', fontsize = 15)
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.legend()
    plt.show()
    return(True)



def Mg_Fe_H(sim):
    xaxis = '[Fe/H]'
    yaxis = '[Mg/Fe]'

    xy = sim.inner.plot_spectro(fig=1, xaxis = xaxis, yaxis = yaxis, return_x_y = True)
    stellar_data.plot_spectro(fig=1,galaxy='milky_way',xaxis=xaxis,yaxis=yaxis,obs=obs_all)
    plt.plot(xy[0], xy[1], color = 'w', linewidth = 3.0)
    plt.plot(xy[0], xy[1], color = 'b', linewidth = 1.5, label = 'beta_power = -1.3')
    plt.xlim(-2,0.5)
    plt.ylim(-0.5,1)
    plt.xlabel('[Fe/H]', fontsize = 15)
    plt.ylabel('[Mg/Fe]', fontsize = 15)
    plt.show()

    return(True)
'''
def Mg_Fe_nb1a(sim1, sim2,sim3):
    x = '[Fe/H]'
    y = '[Mg/Fe]'

    xy1 = sim1.inner.plot_spectro(fig=2, xaxis = x, yaxis = y, return_x_y = True)
    xy2 = sim2.inner.plot_spectro(fig=2, xaxis = x, yaxis = y, return_x_y = True)
    xy3 = sim3.inner.plot_spectro(fig=2, xaxis = x, yaxis = y, return_x_y = True)

    plt.plot(xy1[0], xy1[1], color='b', linewidth = 1.5, label = 'nb_1a_per_m = 1e-3')
    plt.plot(xy2[0], xy2[1], color='r', linewidth = 1.5, label = 'nb_1a_per_m = 1e-4')
    plt.plot(xy3[0], xy3[1], color='g', linewidth = 1.5, label = 'nb_1a_per_m = 1e-2')

    plt.xlim(-2, 0.5)
    plt.ylim(-0.5, 1)
    plt.legend()
    plt.xlabel('[Fe/H]', fontsize = 15)
    plt.ylabel('[Mg/Fe]', fontsize = 15)
    plt.show()

    return(True)
'''

def Mg_Fe_t(t, sim, obs_data):
    time = np.array(t)/1e9
    age = 13-time
    xx = 'age'
    yy = '[Mg/Fe]'
    xy_Mg = sim.inner.plot_spectro(fig = 3, xaxis = xx, yaxis = yy, return_x_y = True)

    Mg_Fe = []
    for i in range(len(xy_Mg[1])):
        if i<120:
            Mg_Fe.append(xy_Mg[1][i])
    plt.plot(age, np.array(Mg_Fe), color = 'r', linewidth = 1.5, label = 'Age vs [Mg/Fe]')
    plt.errorbar(obs_age, obs_data, 0.011, error_plot, fmt='o', color = 'c', label = 'Nissen et al 2020')
    plt.ylim(-0.199, 0.199)
    plt.xlabel('Age[Gyr]')
    plt.ylabel('[Mg/Fe]')
    plt.legend()
    plt.show()
    
    return(True)

def sn_plot(sim):
    sn_type2 = sim.inner.history.sn2_numbers[-1]
    sn_type1a = sim.inner.history.sn1a_numbers[-1]

    sn_ratio = sn_type2/sn_type1a

    sim.inner.plot_sn_distr()
    plt.semilogx()
    plt.show()
    
    return(sn_ratio)

def mass_of_yields(sim):
    specie = 'Fe'
    sim.inner.plot_mass(specie = specie, color = 'b', label = 'Massive stars', source = 'massive', shape = '-')
    sim.inner.plot_mass(specie = specie, color = 'k', label = 'AGB stars', source = 'agb', shape = '--')
    plt.show()

    return(True)


def ISM_mass(sim):
    sim.inner.plot_totmasses(color='b', label = 'open box')
    plt.show()

    return(True)


#main program
# Load STELLAB data
stellar_data=stellab.stellab()

#test1.plot_spectro?
obs_all = ['stellab_data/milky_way_data/Frebel_2010_Milky_Way_stellab',
'stellab_data/milky_way_data/Venn_et_al_2004_stellab',
'stellab_data/milky_way_data/Akerman_et_al_2004_stellab',
'stellab_data/milky_way_data/Andrievsky_et_al_2007_stellab',
'stellab_data/milky_way_data/Andrievsky_et_al_2008_stellab',
'stellab_data/milky_way_data/Andrievsky_et_al_2010_stellab',
'stellab_data/milky_way_data/Bensby_et_al_2005_stellab',
'stellab_data/milky_way_data/Bihain_et_al_2004_stellab',
'stellab_data/milky_way_data/Bonifacio_et_al_2009_stellab',
'stellab_data/milky_way_data/Caffau_et_al_2005_stellab',
'stellab_data/milky_way_data/Cayrel_et_al_2004_stellab',
'stellab_data/milky_way_data/Cohen_et_al_2013_stellab',       
'stellab_data/milky_way_data/Fabbian_et_al_2009_stellab',
'stellab_data/milky_way_data/Gratton_et_al_2003_stellab',
'stellab_data/milky_way_data/Israelian_et_al_2004_stellab',
'stellab_data/milky_way_data/Lai_et_al_2008_stellab',
'stellab_data/milky_way_data/Nissen_et_al_2007_stellab',
'stellab_data/milky_way_data/Reddy_et_al_2006_stellab',
'stellab_data/milky_way_data/Reddy_et_al_2003_stellab',
'stellab_data/milky_way_data/Spite_et_al_2005_stellab',
'stellab_data/milky_way_data/Battistini_Bensby_2016_stellab',
'stellab_data/milky_way_data/Nissen_et_al_2014_stellab',
'stellab_data/milky_way_data/Bensby_et_al_2014_stellab',
]
t, Fe_H = o_res.inner.plot_spectro(solar_norm = 'Asplund_et_al_2009', return_x_y = True)

SFR_time(o_res)
age_metallicity(t, Fe_H)
Mg_Fe_H(o_res)
#Mg_Fe_nb1a(o_res, o_res2, o_res3)

Mg_Fe_t(t, o_res, MgFe_plot_data)

#ratio_supernovae = sn_plot(o_res)




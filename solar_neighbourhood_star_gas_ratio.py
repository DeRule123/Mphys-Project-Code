import numpy as np
import matplotlib.pyplot as plt

import omega_plus as omega_plus
from NuPyCEE import chem_evol
from NuPyCEE import omega
from NuPyCEE import sygma
from NuPyCEE import stellab

#Kroupa imf

imf_type = 'kroupa'
imf_bdys = [0.1, 100]
alphaimf = 1.35
imf_yields_range = [0,40]


table = 'yield_tables/agb_and_massive_stars_K10_K06_0.5HNe.txt'
exp_infall = [[100/2.2, 0.0, 0.8e9], [13.0/2.2, 1.0e9, 7.0e9]] #from 'best' model

sn1a_table = 'yield_tables/sn1a_i99_CDD1.txt'

#ivo_sn1a_table = 'yield_tables/sn1a_ivo13_stable_z.txt'

#standard model afterwards
kwargs = {"special_timesteps":150, "t_star":1.0, "table":table, "mgal":1.0,
          "m_DM_0":1.0e12, "sfe":2.3e-10, "mass_loading":0.52, "imf_type": imf_type, "imf_bdys": imf_bdys, "alphaimf": alphaimf,
          "imf_yields_range":imf_yields_range, "sn1a_table":sn1a_table, "sn1a_rate": 'power_law'}

o_res = omega_plus.omega_plus(exp_infall = exp_infall, beta_pow = -1.3, **kwargs)


m_gas_exp = np.zeros(o_res.inner.nb_timesteps+1)

for i_t in range(o_res.inner.nb_timesteps+1):
    m_gas_exp[i_t] = sum(o_res.inner.ymgal[i_t])

m_star_lost = 0.0

for i_t in range(o_res.inner.nb_timesteps):
    m_star_lost +=np.sum(o_res.inner.mdot[i_t])


stellar_final = np.sum(o_res.inner.history.m_locked)-m_star_lost
gas_final = m_gas_exp[-1]

gas_to_star = gas_final/stellar_final

print(gas_to_star)

true_val = 3/7
if true_val>gas_to_star:
    uncertainty_absolute = (true_val-gas_to_star)/true_val

else:
    uncertainty_absolute = (gas_to_star-true_val)/true_val

print("\n")
print("percentage uncertainty: ", (uncertainty_absolute*100), "%")
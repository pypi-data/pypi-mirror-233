from .quantity import *

G = 6.67430e-11*(N*m2/kg**2) # gravitational constant
c = 299792458*m/s # speed of light
h = 6.62607015e-34*J*s # planck constant
k = 1.380649e-23*J/K # boltzmann constant
R_ideal = k*mol
e = 1.602176634e-19*C # elementary charge
sigma_sb = (2*pi**5*k**4)/(15*c**2*h**3)

g_earth = 9.80665*m/s/s # avg surface gravity on earth

mu_0 = 1.25663706212e-6*N/A/A # vacuum magnetic permeability
e_0 = One/(mu_0*c**2) # vacuum electric permittivity
k_e = 8.9875517923e9*N*m2/C**2

m_e = 9.1093837015e-31*kg # electron mass
m_p = 1.67262192369e-27*kg # proton mass
m_n = 1.67492749804e-27*kg # neutron mass

# planck units
l_planck = 1.616255e-35*m
m_planck = 2.176434e-8*kg
t_planck = 5.391247e-44*s
T_planck = 1.416784e+32*K
E_planck = m_planck*c**2

def qpy_constants_help():
    print("constant:   variable name: value")
    print("--------------------------------")
    print("speed of light:         c:", c)
    print("Planck constant:        h:", h)
    print("Boltzmann constant:     k:", k)
    print("ideal gas constant: R_ideal:", R_ideal)
    print("elementary charge:      e:", e)
    print("gravitational constant: G:", G)
    print("Stefan-Boltzmann constant: sigma_sb:", sigma_sb)
    print()
    print("vacuum permeability: mu_0:", mu_0)
    print("vacuum permittivity:  e_0:", e_0)
    print("Coulomb constant:     k_e:", k_e)
    print()
    print("electron mass:        m_e:", m_e)
    print("proton mass:          m_p:", m_p)
    print("neutron mass:         m_n:", m_n)
    print()
    print("earth acc. due to gravity:  g_earth:", g)
    print()
    print("Planck length:   l_planck:", l_planck)
    print("Planck masss:    m_planck:", m_planck)
    print("Planck time:     t_planck:", t_planck)
    print("Planck temp.:    T_planck:", T_planck)
    print("Planck energy:   E_planck:", E_planck)
    print("---------------------------------")
    print("example:")
    print()
    print(">>> import qpy.constants as qc")
    print(">>> E_electron = qc.m_e * qc.c**2")
    print(">>> print(E_electron.termsOf(MeV))")
    print("0.5109989499961642 MeV")

if __name__ == '__main__':
    help()

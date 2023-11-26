#!/usr/bin/pythoon
from __future__ import print_function
import os,sys,math

unit=sys.argv[1]     # unit of energy kcal or kJ
unit2=sys.argv[2]    # unit of window space (length, angle, ect)
d=float(sys.argv[3]) # window spacing 
                     # in length - (use A for kcal & nm for kJ)
T=float(sys.argv[4]) # Temparatuer (in K)

eps = 1.0e-14

# MATH constants
#
PI = math.acos(-1.0) # PI
sPI = math.sqrt(PI)  # PI^(1/2)

#
# PHYSICAL CONSTANTS
#
# REF:COTATA 2017 adjustment
#	To cite this article: D B Newell et al 2018 Metrologia 55 L13
#
conv=1.e-3       # J to kJ conversion factor
conv2=1.0/4.184  # J to cal conversion factor (1 cal = 4.184 J , thermochemical definition exact)
kB=1.380649e-23  # in J/K
Na=6.02214076e23 # Avogadro's Number (1 mol of particles)

if (unit == "kcal"): 
  conv*=Na # (J/K -> kJ/mol/K)
  conv*=conv2
  # kB = 0.0019872041 # Boltzmann constant (in kcal/mol/K)
  # output from code : kB = 0.0019872 ( in kcal/mol/K)
elif (unit == "kJ"): 
  conv*=Na # (J/K -> kJ/mol/K )
  # kB = 0.0083144621 # Boltzmann constant (in kJ/mol/K)
  # output from code : kB = 0.00831446 ( in kJ/mol/K) 
else:
  print("energy units should be either kcal or kJ") ; sys.exit(0);

kB*=conv # units in kJ/mol/K or kcal/mol/K

print("kB = %g (%s/mol/K)" % (kB,unit))

kBT  = kB*T         # Thermal energy (in kcal/mol)
# print(kBT)

# Equation that provides force constant based on overlap of two Gaussians separated by d
# whose average acceptance probability ~ 0.4
#
# N1~exp(-k/2kBT*(x-x0)^2) & N2~exp(-k/2kBT*(x-x0-d)^2)
#
# z=d/sqrt(k/2kBT) ~ 0.8643 for Pa ~ 0.3875
#
# k=2*kBT*(z/d)^2
zopt=0.8643
kbias=2.0*kBT*((zopt/d)**2)

print("bias force constant for umbrella potential = %g (%s/mol/%s^2)" % (kbias,unit,unit2))
print("0.5*kbias= %g" % (0.5*kbias))

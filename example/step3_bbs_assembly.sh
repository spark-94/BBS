#!/bin/bash

# CHARMM executable: change as needed
#
charmm=/v/apps/bin/c47b1

# Make Output directories
#
mkdir -p charmm
mkdir -p openmm
mkdir -p openmm/restraints

# Run job
# 1. Assembly of a BBS from two bilayers
# 2. Prepare psf/crd/pdb                 (consistent w/ OpenMM box convention)
#            lipid_pos.txt/prot_pos.txt  (lists of restrained atoms)
#
${charmm} -i step3_bbs_assembly.inp >& step3_bbs_assembly.out

# Write sysinfo.dat for OpenMM
#
finp=charmm/step3_bbs_assembly.str
A=`cat ${finp} | grep 'SET A ' | awk '{print $4}'`
B=`cat ${finp} | grep 'SET B ' | awk '{print $4}'`
C=`cat ${finp} | grep 'SET C ' | awk '{print $4}'`

fout=openmm/sysinfo.dat
echo "{\"dimensions\": [ ${A} , ${B} , ${C} , 90.0 , 90.0 , 90.0 ]}" > ${fout}

# Prepare OpenMM input scripts
# Copy scripts to ./openmm
cp ./openmm_script/toppar.str ./openmm/
cp ./openmm_script/*.py       ./openmm/
cp ./openmm_script/run*.slurm ./openmm/


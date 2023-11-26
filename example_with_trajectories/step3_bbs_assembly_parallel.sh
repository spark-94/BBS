#!/bin/bash
#SBATCH --partition=sky
#SBATCH --nodes=1 --exclusive
#SBATCH --ntasks=8
#SBATCN --ncpus-per-task=3
#SBATCH --qos=medium
#SBATCH --output=error.o
#SBATCH --error=error.e
#

# Set ncpu for different partitions
partition=${SLURM_JOB_PARTITION} # partition name
if [[ ${partition} == "sky" ]] ; then
  ncpu=24
elif [[ ${partition} == "ivy" ]] ; then
  ncpu=12
else
  ncpu=16
fi
 

module load intel/17.0.1 impi/5.1
module list

# # ALIAS TO THE FULL PATHNAME TO HINT FOR LIBS
# alias mpirun `which mpirun`
mpirun=`which mpirun`

# SPECIFIC FOR INTEL MPI ONLY
unset I_MPI_PMI_LIBRARY
# CHIPSET AUTODETECT; ASSUME AVX, CHECK FOR AVX2
chip=avx
na=`grep avx2 /proc/cpuinfo | wc -l`
if [[ $na > 0 ]]; then chip=avx2;fi
# CIRCUMVENT SLURM AND OPENMP ISSUES
export SLURM_CPU_BIND=none
export OMP_NUM_THREADS=1
# ASSIGN PROGRAM NAME AND RUN
charmm=/v/apps/charmm/c47b1/chm.intel.$chip.impi
# mpirun -np $SLURM_NTASKS $charmm -i file.inp >& file.out


mkdir -p charmm
mkdir -p openmm
mkdir -p openmm/restraints

# Use fewer tasks for job
# ncpu=$(( ${ncpu} / 2 ))
ncpu=8
${mpirun} -np ${ncpu} ${charmm} -i step3_bbs_assembly_mini_snapshots.inp >& step3_bbs_assembly.out

finp=charmm/step3_bbs_assembly.str
A=`cat ${finp} | grep 'SET A ' | awk '{print $4}'`
B=`cat ${finp} | grep 'SET B ' | awk '{print $4}'`
C=`cat ${finp} | grep 'SET C ' | awk '{print $4}'`

# Write sysinfo.dat for OpenMM
fout=openmm/sysinfo.dat
echo "{\"dimensions\": [ ${A} , ${B} , ${C} , 90.0 , 90.0 , 90.0 ]}" > ${fout}

# Prepare OpenMM input scripts
# Copy scripts to ./openmm
cp ./openmm_script/toppar.str ./openmm/
cp ./openmm_script/*.py       ./openmm/
cp ./openmm_script/run*.slurm ./openmm/


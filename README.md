# BBS 

Membrane proteins (MPs) often show preference for one phase over the other, which is characterized by the partition coefficient, Kp. The physical mechanisms underlying Kp from experiments have been only inferred indirectly due to the unavailability of detailed structures and compositions of ordered phases. Molecular dynamics (MD) simulations can complement these details and thus, in principle, can provide further insights to the partitioning of MPs between two phases. However, the application of MD has remained difficult due to long required time scales for equilibration and large system size for the phase stability, which have not been fully resolved even in free energy simulations. 

The binary bilayer system (BBS) is designed to preserve the lateral packing of both phases in a significantly smaller size compared to the that required for macroscopic phase separation. These characteristics are advantageous in partitioning simulations, where the length scale for diffusion across the system can be significantly smaller than that in larger bilayers. Hence the BBS can be efficiently employed in both conventional MD and free energy simulations. 

A BBS is composed of two laterally attached patches of bilayers, B1 and B2, which can be conveniently prepared from two pre-equilibrated individual bilayers. To maintain interface bewteen two bilayers, the binary bilayer restraing potential, V(X), is applied to specified lipids in each bilayer. The embedded MP can be restrained as well with an applied umbrella potential, U(X). 

# Example
Here, we provide example scripts for the generation of a BBS from two pre-equilibrated individual Lo- and Ld-phase bilayers with an embedded model transmembrane peptide.

All required scripts are given in example folder.
There is another folder, example_with_trajectories, which contains the outputs from the scripts. 

Contents in directories 
----------------------
    bilayers     : PSF,CRD, and PDB of inidividual bilayers B1 and B2 with system info. (STR)
    toppar       : CHARMM force field files
    openmm_script: OpenMM simulations (based on CHARMM-GUI Membrane-Builder) and SLURM job scripts

Assembly of a BBS
--------------------
After modifiyng the path for CHARMM excecutable run

    bash step3_bbs_assembly.sh

This is a wrapper script for a CHARMM script,

    step3_bbs_assembly.inp

which reads or runs the following files

    toppar.str (for reading CHARMM force field parameters)
    crystal_image.str (for setting up PBC & Crystal system)
    checkfft.py (for calc. numbers of grids for PME)
    setup_dihe_rest.str (for dihedral restraint)
        - modified from membrane_restraint2.str form Membrane-Builder

Generated outputs (PSF, CRD, PDB, and system information) are saved in

	./charmm: CHARMM outputs 
	./openmm: Inputs for OpenMM simulations

After the assembly, OpenMM and SLURM job scripts are copied to ./openmm for the simulation of the BBS.

If BBS configurations after each minimization step is necessary, edit 

    step3_bbs_assembly.sh

in which, replace 

    step3_bbs_assembly.inp

with 

    step3_bbs_assembly_mini_snapshots.inp

OpenMM equilibration and production runs 
--------------------
In ./example/openmm_script, scripts for OpenMM simulations are provided.
These scripts are based on those provided by CHARMM-GUI Membrane Builder.

**Modified or added Python scripts**

    omm_restraint.py        : Modified to support V(X) and U(X) 
    omm_readinputs.py       : Modified to read paramters for V(X) and U(X)
    omm_comreporter.py      : COMReporter. Added to generate box size & COM of embedded MPs
    openmm_run.py           : Modified to support V(X), U(X), and COMReporter

Header section in all Python scripts is updated for OpenMM 7.0 or later versions.

V(X) and U(X) are the binary bilayer restraining and umbrella potentials, respectively.

COMReporter allows on the fly generation of time series of
        box size and COM along the X, Y, and Z dimensions

While the Python and SLURM scripts are copied to ./example/openmm in the assembly step, the input parameter scripts (*.inp) are not copied. Instead these scripts are updated appropriately for the target position of the MP and saved to ./example/openmm.

Input scripts for simulation
---------------------------
toppar.str                 : list of paths for CHARMM force field
step6.x_equilibration.inp  : Input scripts for equilibration
step7_production.inp       : Input script for production

# NOTE
#       Simulations input scripts (*.inp) is copied to simulation directory (../openmm)
#       with updated target X-position (XCOM) for the embedded MP
#
#       In this example XCOM is set to the X-box center.
#       (see *.slurm for details).

Example SLURM job script
-------------------------
run_equi.slurm          : SLURM script for equilibration (step6.1 - 6.6)
run_prod.slurm          : SLUMR script for production 

# NOTE
#       Provided slurm job scripts will not work without appropriate edits.
#       Edits over lines 1-22 (header part) should be sufficient.
#       In the end, users are responsible for editing SLURM job scripts for their use.

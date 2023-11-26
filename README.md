# BBS 

Binary bilayer system (BBS) is composted of two laterally attached patches of bilayers.\n
BBS can be easily prepared from two pre-equilibrated individual bilayers.

Here, we provide example scripts for the generation of a BBS from two pre-equilibrated individual Lo- and Ld-phase bilayers with an embedded model transmembrane peptide.

All required scripts are given in example folder.
There is another folder, example_with_trajectories, which contains the outputs from the scripts. 


Soohyung Park, November 25, 2023.


Contents

DIRECTORIES
-------------------
bilayers     : where inidividual bilayers B1 and B2 are given
toppar       : where CHARMM force field are saved
openmm_script: where template OpenMM scripts are saved

CHARMM input scripts
--------------------
step3_bbs_assembly.inp: CHARMM script to generate a BBS

	use step3_bbs_assembly_mini_snapshots.inp (for PDBs after each minimization)

	outputs will be save to
		./charmm: CHARMM outputs 
		./openmm: Inputs for OpenMM simulations

	The following scripts are read
		toppar.str (for reading CHARMM force field parameters)
		crystal_image.str (for setting up PBC & Crystal system)
		checkfft.py (for calc. numbers of grids for PME)
		setup_dihe_rest.str (for dihedral restraint)
			- modified from membrane_restraint2.str form Membrane-Builder

Bash script to run CHARMM (for BBS assembly)
--------------------
step3_bbs_assembly.sh: a bash script to run CHARMM to generate a BBS &
		     : prepare inputs for OpenMM simulations in ./openmm


NOTE: For OpenMM simulation,
      read README_box_size & README_openmm in openmm_script.


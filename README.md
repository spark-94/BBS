# BBS 

Membrane proteins (MPs) often show preference for one phase over the other, which is characterized by the partition coefficient, Kp. The physical mechanisms underlying Kp from experiments have been only inferred indirectly due to the unavailability of detailed structures and compositions of ordered phases. Molecular dynamics (MD) simulations can complement these details and thus, in principle, can provide further insights to the partitioning of MPs between two phases. However, the application of MD has remained difficult due to long required time scales for equilibration and large system size for the phase stability, which have not been fully resolved even in free energy simulations. 

The binary bilayer system (BBS) is designed to preserve the lateral packing of both phases in a significantly smaller size compared to the that required for macroscopic phase separation. These characteristics are advantageous in partitioning simulations, where the length scale for diffusion across the system can be significantly smaller than that in larger bilayers. Hence the BBS can be efficiently employed in both conventional MD and free energy simulations. 

A BBS is composed of two laterally attached patches of bilayers, B1 and B2, which can be conveniently prepared from two pre-equilibrated individual bilayers. To maintain interface bewteen two bilayers, the binary bilayer restraing potential, V(X), is applied to specified lipids in each bilayer. The embedded MP can be restrained as well with an applied umbrella potential, U(X). 

# Example
Here, we provide example scripts for the generation of a BBS from two pre-equilibrated individual Lo- and Ld-phase bilayers with an embedded model transmembrane peptide.

All required scripts are given in example folder.
There is another folder, example_with_trajectories, which contains the outputs from the scripts. 



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


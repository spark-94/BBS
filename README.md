# BBS 

Membrane proteins (MPs) often show preference for one phase over the other, which is characterized by the partition coefficient, Kp. The physical mechanisms underlying Kp from experiments have been only inferred indirectly due to the unavailability of detailed structures and compositions of ordered phases. Molecular dynamics (MD) simulations can complement these details and thus, in principle, can provide further insights to the partitioning of MPs between two phases. However, the application of MD has remained difficult due to long required time scales for equilibration and large system size for the phase stability, which have not been fully resolved even in free energy simulations. 

The **binary bilayer system (BBS)** is designed to preserve the lateral packing of both phases in a significantly smaller size compared to the that required for macroscopic phase separation. These characteristics are advantageous in partitioning simulations, where the length scale for diffusion across the system can be significantly smaller than that in larger bilayers. Hence the BBS can be efficiently employed in both conventional MD and free energy simulations. 

A BBS is composed of two laterally attached patches of bilayers, B1 and B2, which can be conveniently prepared from two pre-equilibrated individual bilayers. To maintain interface bewteen two bilayers, the binary bilayer restraing potential, V(X), is applied to specified lipids in each bilayer. The embedded MP can be restrained as well with an applied umbrella potential, U(X). 

<figure>
  <img
  src="./BBS.tiff"
  alt="Schematic of BBS">
  <figcaption>Schematic of a binary bilayer system (BBS), where two membrane patches are laterally attached (enclosed by a black rectangle). Their interfaces are maintained by soft restraining potentials (blue and red arrows) applied to specific lipids when they cross the pre-defined X-positions (red and blue dotted vertical lines) in the center and edges of the periodic cell. The unrestrained components can freely diffuse across interfaces (green and yellow). Adapted with permission from Ref. 1. Copyright 2018 American Chemical Society.</figcaption>
</figure>

# Example
Here, we provide example input files for the generation of a BBS from two pre-equilibrated individual Lo- and Ld-phase bilayers with an embedded model transmembrane peptide.

Contents in directories 
----------------------
    bilayers     : PSF,CRD, and PDB of inidividual bilayers with their system info. (STR); The box center is at the origin (the CHARMM box convention)
    toppar       : CHARMM force field files
    openmm_script: OpenMM simulation (based on CHARMM-GUI Membrane-Builder) and SLURM job scripts

Assembly of a BBS
--------------------
After modifiyng the path for CHARMM excecutable, assemble a BBS by running

    bash step3_bbs_assembly.sh

This is a wrapper script for a CHARMM script,

    step3_bbs_assembly.inp

which reads or runs the following files

    toppar.str (for reading CHARMM force field parameters)
    crystal_image.str (for setting up PBC & Crystal system)
    checkfft.py (for calc. numbers of grids for PME)
    setup_dihe_rest.str (for dihedral restraint)
        - modified from membrane_restraint2.str form Membrane-Builder

Generated outputs (PSF, CRD, PDB, and system information) will be saved in

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

V(X) and U(X) are the binary bilayer restraining and umbrella potentials, respectively.

COMReporter allows on the fly generation of time series of
        box size and COM along the X, Y, and Z dimensions.
The header section in all Python scripts is updated for OpenMM 7.6 or later versions.

**SLURM job scripts**

    run_equi.slurm          : SLURM script for equilibration (step6.1 - 6.6)
    run_prod.slurm          : SLUMR script for production 

Provided slurm job scripts will not work without appropriate edits in the header section (lines 1-22). After edit, submit a SLURM job for equilibration

    sbatch -J bbs run_equi.slurm

If allowed, production run will be recursively submitted after equilibration.
If not, one can submit for production runs after equilibration is done,

    sbatch -J bbs run_prod.slurm

**Input parameter scripts**

While the Python and SLURM scripts are copied to ./example/openmm in the assembly step, the input parameter scripts (*.inp) are not copied. Instead these scripts are updated appropriately for the target position of the MP and written in ./example/openmm. (See run_equi.slurm and/or run_prod.slurm for details.)

Example with trajectories
--------------------------
The ouputs from CHARMM assembly and OpenMM simulations are given in ./example_with_trajectories with input files.

References
-----------
[1] Park, S., & Im, W. (2018). Quantitative Characterization of Cholesterol Partitioning between Binary Bilayers. Journal of Chemical Theory and Computation, 14(6), 2829–2833. https://doi.org/10.1021/acs.jctc.8b00140

[2] Park, S., Levental, I., Pastor, R. W., & Im, W. (2023). Unsaturated Lipids Facilitate Partitioning of Transmembrane Peptides into the Liquid Ordered Phase. Journal of Chemical Theory and Computation, 19(15), 5303–5314. https://doi.org/10.1021/acs.jctc.3c00398

[3] Park, S., Yeom, M. S., Andersen, O. S., Pastor, R. W., & Im, W. (2019). Quantitative Characterization of Protein-Lipid Interactions by Free Energy Simulation between Binary Bilayers. Journal of Chemical Theory and Computation, 15(11), 6491–6503. https://doi.org/10.1021/acs.jctc.9b00815

[4] Park, S., Pastor, R. W., & Im, W., (2023).  Binary Bilayer Simulations for Partitioning Within Membranes, (in preparation).

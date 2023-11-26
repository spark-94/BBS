"""
comreporter.py

This reports the COM defined by CustomCentroidBondForce method along with Box sizes.
Template is dcdreporter.py & forcereporter in OpenMM website
Authors: Soohyung Park (2020/05/07)

# dcdreporter.py: Outputs simulation trajectories in DCD format

This is part of the OpenMM molecular simulation toolkit originating from
Simbios, the NIH National Center for Physics-Based Simulation of
Biological Structures at Stanford, funded under the NIH Roadmap for
Medical Research, grant U54 GM072970. See https://simtk.org.

Portions copyright (c) 2012 Stanford University and the Authors.
Authors: Peter Eastman
Contributors:

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS, CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# report COM time series in text format 
# Soohyung Park, 2020/05/01

from __future__ import absolute_import
__author__ = "Soohyung Park" # "Peter Eastman"
__version__ = "1.0"

from openmm import *
from openmm.app import *
from openmm.unit import *

class COMReporter(object):
    """COMReporter outputs a series of COM values from a Simulation to a text file.

    To use it, create a COMReporter, then add it to the Simulation's list of reporters.
    """

    def __init__(self, file, reportInterval, append=False, enforcePeriodicBox=True):
        """Create a COMReporter.

        Parameters
        ----------
        file : string
            The file to write to
        reportInterval : int
            The interval (in time steps) at which to write frames
        append : bool=False
            If True, open an existing text file to append to.  If False, create a new file.
        enforcePeriodicBox: bool
            Specifies whether particle positions should be translated so the center of every molecule
            lies in the same periodic box.  If None (the default), it will automatically decide whether
            to translate molecules based on whether the system being simulated uses periodic boundary
            conditions.
        """
        self._reportInterval = reportInterval
        self._append = append
        self._enforcePeriodicBox = enforcePeriodicBox 
        # self._enforcePeriodicBox = None
        if append:
            mode = 'r+'
        else:
            mode = 'w'
        self._out = open(file, mode)
        # self._com = None

    def describeNextReport(self, simulation):
        """Get information about the next report this object will generate.

        Parameters
        ----------
        simulation : Simulation
            The Simulation to generate a report for

        Returns
        -------
        tuple
            A six element tuple. The first element is the number of steps
            until the next report. The next four elements specify whether
            that report will require positions, velocities, forces, and
            energies respectively.  The final element specifies whether
            positions should be wrapped to lie in a single periodic box.
        """
        steps = self._reportInterval - simulation.currentStep%self._reportInterval
        return (steps, True, False, False, False, self._enforcePeriodicBox)

    def report(self, simulation, state):
        """Generate a report.

        Parameters
        ----------
        simulation : Simulation
            The Simulation to generate a report for
        state : State
            The current state of the simulation
        """

        ## dtypes=state.getDataTypes()
        ## print("DataTypes in State is",dtypes);

        for force in simulation.system.getForces(): # try this one !!
            if isinstance(force,CustomCentroidBondForce):
                # print("force type CustomCentroidBondForce was found");
                comres = force
                break

        #  FOR BBS, box size is necessaary for post processing PMF
        box   = state.getPeriodicBoxVectors()
        boxlx = box[0][0].value_in_unit(nanometers)
        boxly = box[1][1].value_in_unit(nanometers)
        boxlz = box[2][2].value_in_unit(nanometers)

        comgroups = []
        ngroup = comres.getNumGroups()
        for i in range(ngroup):
            # 'PARTICLES' MAY CONTAIN ATOM INDICES AND 'WEIGHTS' MAY CONTAIN MASS WEIGHT
            particles, weights = comres.getGroupParameters(i)
            comgroups.append([particles, weights])
            ## print(comgroups[i]); # Mass array was empty ... so particle masses should be read


        # CALCULATE COM
        sout="%.6f %.6f %.6f" % (boxlx,boxly,boxlz) # write box sizes
        positions = state.getPositions().value_in_unit(nanometers)
        for igrp, comgroup in enumerate(comgroups):
            particles = comgroup[0] # pick indices only
            ## print("particles",particles)
            xcm = ycm = zcm = 0.0
            tmass = 0.0
            for i, iatom in enumerate(particles):
                x, y, z = positions[iatom]
                tm = simulation.system.getParticleMass(iatom).value_in_unit(amus)
                # print(x,y,z,tm)
                xcm += x * tm
                ycm += y * tm
                zcm += z * tm
                tmass += tm
            xcm = xcm / tmass
            ycm = ycm / tmass
            zcm = zcm / tmass
            sout+=" %.6f %.6f %.6f" % (xcm,ycm,zcm) # write COM of each group
        sout+="\n"
        self._out.write(sout) 

    def __del__(self):
        self._out.close()

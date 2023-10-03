# -*- coding: utf-8 -*-
"""
    Execute the Premod solver
"""

import os
import numpy as np
import subprocess
import warnings
from pathlib import Path

from premod.io import PremodInputs, Results 
from premod.plot import PlotResults
#from pario.chemistry import Chemistry


class Progress(object):
    
    """ Simple object to track the status of a simulation """
    
    def __init__(self):
        self.status = ''
        self.message = ''
        
    def failed(self, message):
        self.status = 'failed'
        self.message = message
        
    def success(self, message=''):
        self.status = 'success'
        self.message = message
    
    def __call__(self, percent, message):
        pass


class PremodSolver(object):
    
    """
        
        Class to prepare the inputs, read the outputs and run a premod 
        simulation.
        
        Open a template, change parameters, save input in a different location,
        run the simulation, plot the results:
        
        >>> premod = PremodSolver(filename='template.txt', exe='premod.exe')
        >>> premod.set_weight_fraction('Mg', 0.82)
        >>> premod.run('test.txt')
        >>> premod.plot(figtyp='particle_evolution')
            
    """
    
    name = 'premod'
    
    def __init__(self, inp=None, filename=None, exe=''):
        self.exe = exe
        self.inp = PremodInputs()
        self.chemistry = None
        self.result = Results()
        self.fig = PlotResults(self.result)
        if inp is not None and filename is not None:
            raise ValueError("initialization of PremodSolver with both filename and inp")
        if inp is not None:
            self.inp = inp
        if filename is not None:
            self.read(filename)
        
    def _update_alloy(self):
        """ Update the alloy input file from the chemistry object """
        unit = self.inp.alloy['UNIT']
        el = self.chemistry.symbols
        if unit.find('w') == 0:
            frac = self.chemistry.weight_fractions
        elif unit.find('a') == 0:
            frac = self.chemistry.atom_fractions
        if unit.find('%') > 0:
            frac *= 100.0
        self.inp.alloy.set_table(cols=[el, frac])
            
    def _create_chemistry(self, elements, fractions, unit):
        """ Create a chemistry object for the alloy composition """
        if 'Al' in elements:
            elements.remove('Al')
        elements.insert(0, 'Al')
        frac = np.array(fractions)
        if unit.find('%') > 0:
            frac *= 0.01
        if unit.find('w') == 0:
            self.chemistry = Chemistry(elements, weight_fractions=frac)
        elif unit.find('a') == 0:
            self.chemistry = Chemistry(elements, atom_fractions=frac)
            
    def set_alloy(self, name, elements, fractions, unit='wt%'):
        """ Set the composition of the alloy """
        if len(elements) != len(fractions):
            raise ValueError("arrays of different length in set_alloy")
        self.inp.alloy['ALLOYNAME'] = name
        self.inp.alloy['UNIT'] = unit
        self._create_chemistry(elements, fractions, unit)
        self._update_alloy()
    
    def set_weight_fraction(self, element, fraction):
        """ Set the weight fraction of the given element """
        self.chemistry.set_weight_fraction(element, fraction)
        self._update_alloy()
    
    def set_atom_fraction(self, element, fraction):
        """ Set the atom fraction of the given element """
        self.chemistry.set_atom_fraction(element, fraction)
        self._update_alloy()
        
    def set_fraction(self, element, fraction, unit):
        """ Set the element fraction with the specified unit """
        if unit.find('%') > 0:
            fraction *= 0.01
        if unit.find('w') == 0:
            self.chemistry.set_weight_fraction(element, fraction)
        elif unit.find('a') == 0:
            self.chemistry.set_atom_fraction(element, fraction)
        self._update_alloy()
        
    def fractions(self, unit):
        """ Return the fractions in wt, wt% or at_frac """
        if unit.find('w') == 0:
            f = self.chemistry.weight_fractions
        elif unit.find('a') == 0:
            f = self.chemistry.atom_fractions
        if unit.find('%') > 0:
            f *= 100.0
        return f
    
    def balance(self, unit):
        """ Return the balance (Al) in wt, wt% or at_frac """
        fractions = self.fractions(unit)
        return fractions[0]
    
    def composition(self, unit):
        """ Return a dict with key: symbol, value: fraction """
        return dict(zip(self.chemistry.symbols, self.fractions(unit)))
        
    def set_process(self, time, temperature):
        """ Set the temperature history / thermal treatment """
        self.inp.process.set_table(cols=[time, temperature])
        
    def set_output(self, times=None, period=None):
        if isinstance(times, (list, tuple, np.ndarray)):
            self.inp['OUTPUT_TIMES'] = [str(x) for x in times]
        if period is not None:
            try:
                p = float(period)
            except:
                p = None
            if p is not None:
                self.inp['OUTPUT_PERIOD'] = p

    def set_instance_IO_version(self,instance_IO_version=1):
        """ set the value for the instance_IO_version parameter"""
        self.inp['INSTANCE_IO_VERSION'] = instance_IO_version
    
    def set_phase(self, name, ppt):
        """ Set the table for the PPTSIM input file
        
            name: str
                Name of one phase model defined in the PHASES file
                
            ppt: str
                Name of one precipitate model defined in the PPTLIB file
        
        """
        col = ['', '']
        if isinstance(name, int):
            col[0] = self.inp.phases.entry[name]['NAME']
        elif isinstance(name, str):            
            for entry in self.inp.phases.entry:
                if entry['NAME'] == name:
                    col[0] = name
                    break

        if isinstance(ppt, int):
            col[1] = self.inp.pptlib.entry[name]['NAME']
        elif isinstance(name, str):            
            for entry in self.inp.pptlib.entry:
                if entry['NAME'] == ppt:
                    col[1] = ppt
                    break
        
        if all([len(x) for x in col]): 
            self.inp.pptsim.set_table(cols=[col])
        else:
            if not col[0]:
                raise RuntimeError('Phase not found: ' + name)
            if not col[1]:
                raise RuntimeError('Precipitate not found: ' + ppt)

    def read(self, filename,result=True):
        """ Read the input files """
        self.inp.read(filename)
        elements = self.inp.alloy.column(0)
        fractions = self.inp.alloy.column(1, 'float')
        self._create_chemistry(elements, fractions, self.inp.alloy['UNIT'])
        if result:
            self.result.read(filename, self.inp)

    def write(self, filename):
        """ Write the input files """
        # check if the sequence is not empty
        if len(self.inp.sequence) == 0:
            warnings.warn("The input sequence is empty and so nothing will be written.")
        self.inp.write(filename)
        
    def run(self, filename, progress=None):
        """ Write the input files, run the premod solver and read the outputs
            
            filename: str
                Input path and filename
                
            progress: Progress object
                Track the simulation status and show progress
        """
        return self._run(filename, add_input=True, progress=progress)
        
    def check_log(self, line, progress):
        """ Check the output line of the solver and change the status of the
            progress object
        """
        if line.find('fatal') == 0:
            error = line.replace('The program will stop', '')
            error = error.replace('fatal', '').strip()
            progress.failed(error)
            
        elif line.find('error') == 0:
            error = line.replace('The program will stop', '')
            error = error.replace('error', '').strip()
            progress.failed(error)
            
        elif line.find('Written: Output') >= 0:
            parts = line.split('=')
            tim = float(parts[1])
            if tim not in progress.times:
                progress.times.add(tim)                        
                done = 100.0 * len(progress.times) / len(progress.out_times)
                progress(done, line.replace('info', '').strip())
                    
        elif line.find('Program ended normally') >= 0:
            progress.success()
    
    def _run(self, filename, add_input=True, progress=None):
        self.inp.write(filename)
        self.result.clear()
        # run process    
        basename = os.path.basename(filename)
        casedir = os.path.dirname(filename)
        if casedir == '':
            casedir = './'
        args = [self.exe, basename] if add_input else [self.exe]
        
        if progress is None:
            progress = Progress()
              
        with subprocess.Popen(args, cwd=casedir,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              universal_newlines=True) as proc:

            progress.message = ''
            progress.status = ''
            progress.times = set()
            progress.out_times = [float(x) for x in self.inp['OUTPUT_TIMES']]
            while True:
                self.check_log(proc.stdout.readline(), progress)
                if progress.status == 'failed':
                    break
                if proc.poll() is not None:
                    break            
            proc.terminate()
    
        #if progress.status == 'success':
        #    self.result.read(filename, self.inp)
        
        return progress.status, progress.message
        
    def plot(self, figtyp='', fig_kw=dict()):
        """ Plot a result
            
            figtyp: str
                Type of the figure

            fig_kw: str
                Figure parameters, see matplotlib.pyplot.figure
        """
        self.fig.plot(figtyp, fig_kw)

    
    def set_default(self):
        """
        read default input file to perform a standard initialization of the simulation
        the files are located in the default folder next to this file.
        """
        folder = Path(__file__).parent.resolve()
        file_default = folder / "default" / "test_default.txt"
        self.read(filename=file_default,result=False)


class Chemistry(object):

    def __init__(self,elements,
                weight_fractions=None,
                atom_fractions=None):
        self.elements = elements
        self.symbols = elements
        self.weight_fractions = weight_fractions
        self.atom_fractions = atom_fractions
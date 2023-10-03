# -*- coding: utf-8 -*-
"""
    Handling of input files and output files of Premod
"""

import os, sys
from glob import glob
from collections import OrderedDict
from inspect import isfunction, ismethod

import numpy as np

dirname = os.path.dirname(__file__)
sys.path.append(os.path.join(dirname, '..', '..','..','calm'))
from calm.chemistry import ChemistrySizeDistribution
from premod.parser_generic import parse_complete
from premod.strength import define_chem_premod


class InputFile(OrderedDict):

    def __init__(self, name):
        OrderedDict.__init__(self)
        self.name = name
        self.comment = '!'

    def read(self, filename):
        """ Read a input file """
        with open(filename) as fil:
            self.read_string(fil.read())

    def read_string(self, value):
        """ Read a input string """
        pass

    def to_string(self):
        """ Convert a InputFile to a string """
        return ''

    def write(self, filename):
        """ Write a input file """
        with open(filename, 'w') as fil:
            fil.write(self.to_string())


class ConfigFile(InputFile):

    def __init__(self, name, key='', keep_comment=False):
        InputFile.__init__(self, name)
        self.keep_comment = keep_comment        
        self.key = key
        self.comments = []
        self.sequence = []

    def read_string(self, value):
        self.clear()
        self.comments.clear()
        self.sequence.clear()
        lines = value.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.find(self.comment) == 0:
                self.sequence.append(len(self.comments))
                self.comments.append(line)
            else:
                delimiter = '='
                kv = [x.strip() for x in line.split('=')]
                if len(kv) < 2:
                    kv = [x.strip() for x in line.split()]
                    delimiter = ' '
                if len(kv) == 2:
                    key, val = kv
                    if key == self.key:
                        i += 1
                        val = [x for x in lines[i].split()]
                    self[key] = val
                    self.sequence.append([key, delimiter])
            i += 1

    def to_string(self):
        """ Format the ConfigFile to a string """
        lines = []
        for key in self.sequence:
            if isinstance(key, int):
                if self.keep_comment:
                    lines.append(self.comments[key])
            else:
                k = key[0]
                delimiter = key[1]
                v = self[k]
                if k == self.key:
                    lines.append('{}{}{}'.format(k, delimiter, len(v)))
                    lines.append(' '.join([str(x) for x in v]))
                else:
                    lines.append('{}{}{}'.format(k, delimiter, v))
        lines.append('')
        return '\n'.join(lines)


class TableFile(InputFile):

    def __init__(self, name, nrow=None):
        InputFile.__init__(self, name)
        self.table = []
        self._nrow = nrow

    @property
    def nrow(self):
        """ Return the number of rows in the table """
        if isfunction(self._nrow) | ismethod(self._nrow):
            return self._nrow(self.table)
        elif isinstance(self._nrow, int):
            return self._nrow
        else:
            return len(self.table)

    def read_string(self, value):
        self.clear()
        self.table.clear()
        lines = value.split('\n')
        for line in lines:
            if line.find(self.comment) == 0:
                pass
            elif line.find('=') > 0:
                kv = [x.strip() for x in line.split('=')]
                if len(kv) == 2:
                    self[kv[0]] = kv[1]
            else:
                try:
                    num = int(line)
                except:
                    num = None
                if num is None:
                    row = [x.strip() for x in line.split()]
                    if row:
                        self.table.append(row)

    def set_table(self, rows=None, cols=None):
        self.table.clear()
        if rows:
            self.table = rows
        elif cols:
            nrow = max([len(c) for c in cols])
            for r in range(nrow):
                row = [col[r] if r < len(col) else None for col in cols]
                self.table.append(row)

    def column(self, index, dtype='str'):
        col = [row[index] for row in self.table]
        if dtype.find('s') == 0:
            return col
        elif dtype.find('f') == 0:
            return [float(x) for x in col]
        elif dtype.find('i') == 0:
            return [int(x) for x in col]

    def to_string(self):
        lines = ['{}={}'.format(k, v) for k, v in self.items()]
        lines.append('{}'.format(self.nrow))
        for row in self.table:
            lines.append(' '.join(['{}'.format(x) for x in row]))
        lines.append('')
        return '\n'.join(lines)


class LibraryFile(InputFile):

    def __init__(self, name, key=''):
        InputFile.__init__(self, name)
        self.key = key
        self.entry = []

    def read_string(self, value):
        self.clear()
        self.entry.clear()
        lines = value.split('\n')
        entry = None
        for line in lines:
            if line.find(self.comment) == 0:
                pass
            elif line.find('=') > 0:
                kv = [x.strip() for x in line.split('=')]
                if len(kv) == 2:
                    key, val = kv
                    if key == self.key:
                        entry = OrderedDict()
                        self.entry.append(entry)
                    if entry is None:
                        self[key] = val
                    else:
                        entry[key] = val

    def to_string(self):
        lines = ['{}={}'.format(k, v) for k, v in self.items()]
        for entry in self.entry:
            lines.append(self.comment + '-----------')
            lines += ['{}={}'.format(k, v) for k, v in entry.items()]
        lines.append('')
        return '\n'.join(lines)

    def add(self, **kwargs):
        """ Add an entry in the library """
        entry = OrderedDict()
        for k, v in kwargs.items():
            entry[k.upper()] = v
        self.entry.append(entry)
        return entry


class MainFile(ConfigFile):

    def __init__(self, files, comment='!', filename='', keep_comment=False):
        ConfigFile.__init__(self, 'main', 'OUTPUT_TIMES', keep_comment)
        self.comment = comment
        for name, params in files.items():
            inp = self._input_file(name, params)
            if inp is not None:
                inp.comment = comment
                self.__dict__[name] = inp
        self.filename = filename
        if filename:
            self.read(filename)

    def _input_file(self, name, params):
        typ = ''
        arg = ''
        if isinstance(params, str):
            typ = params.lower()
        elif isinstance(params, tuple):
            typ = params[0].lower()
            arg = params[1]
        fil = None
        if typ == 'config':
            fil = ConfigFile(name, arg, self.keep_comment)
        elif typ == 'table':
            fil = TableFile(name, arg)
        elif typ == 'library':
            fil = LibraryFile(name, arg)
        return fil

    def read(self, filename):
        self.filename = filename
        ConfigFile.read(self, filename)

    def read_string(self, value):
        ConfigFile.read_string(self, value)
        dirname = os.path.dirname(self.filename)
        for key, val in self.items():
            if key.find('FILE_') == 0:
                name = key[5:].lower()
                fil = getattr(self, name, None)
                if fil is not None:
                    fil.read(os.path.join(dirname, val))

    def before_write(self):
        """ Update some inputs before writing """
        pass

    def write(self, filename):
        """ Write a input file """
        self.before_write()
        ConfigFile.write(self, filename)
        dirname = os.path.dirname(filename)
        for key, val in self.items():
            if key.find('FILE_') == 0:
                name = key[5:].lower()
                fil = getattr(self, name, None)
                if fil is not None:
                    fil.write(os.path.join(dirname, val))


class PremodInputs(MainFile):

    def __init__(self, filename=''):
        nrow = lambda table: len(table) // 2
        MainFile.__init__(self,
                          files={'solver': 'config',
                                 'alloy': 'table',
                                 'process': 'table',
                                 'phases': ('library', 'NAME'),
                                 'pptlib': ('library', 'CATEGORY'),
                                 'pptsim': ('table', nrow)},
                          filename=filename)

    def before_write(self):
        """ Update some inputs before writing """
        elements = self.alloy.column(0)
        #self.phases['NELEMENTS'] = len(elements)
        #self.phases['NPHASES'] = len(self.phases.entry)
        #self.phases['ELEMENTS'] = ', '.join([f'"{el}"' for el in elements])
        self.pptlib['NMODELS'] = len(self.pptlib.entry)

    def modify_outputtimes(self, list_times:list):
        """ modify the list of times at which microstructure state is written"""
        # sort the list
        list_times.sort()
        # convert list to string
        list_strings = [str(value) for value in list_times]

        if 'OUTPUT_TIMES' in self.keys():
            # affect the new list
            self['OUTPUT_TIMES'] = list_strings
        else:
            raise ValueError('OUTPUT_TIMES not in the keys')

    
    def modify_temperature_history(self, times_temp:list, hist_filename):
        """ modify the temperature history and possibly the name of the file"""
        # TODO need to check if the list is sorted
        # l.sort(key=lambda x: x[0]) to sort the list with the first value
        # convert list to string
        list_strings = [[str(time),str(temp)] for [time,temp] in times_temp]

        # affect the new list
        self.process.table = list_strings

        self['FILE_PROCESS'] = hist_filename


class HistoryFile(OrderedDict):

    def __init__(self, filename=''):
        self.names = []
        self.units = []
        
        if filename:
            self.read(filename)

    def get_IO_version(self,filename):
        """ get the IO_version from the header of the file"""
        self.IO_version = None
        with open(filename) as fil:
            for line in fil.readlines():
                # temporary change to handle the case
                if "_fv (-)" in line:       #"IO_version:" in line:
                    self.IO_version = 2     #int(line.strip().split(":")[1])
                    break
        if self.IO_version is None:
            self.IO_version = 1
            print("Warning: " +"IO_version not found in "+filename+ " version 1 is used")

    def clear(self):
        super().clear()
        self.names.clear()
        self.units.clear()

    def read(self, filename):
        self.get_IO_version(filename)
        if os.path.exists(filename):
            nskip = 1
            with open(filename) as fil:
                for line in fil.readlines():
                    if line[0] == "#":
                        nskip+=1
                    else:
                        names = line.split(';')
                        break
            #try:
            #print("Error in loading the file: ",filename,"\nnskip: ",nskip)
            data = np.loadtxt(filename, delimiter=';', skiprows=nskip)
            #except:
            #    print("Error in loading the file: ",filename,"\nnskip: ",nskip)
            self.clear()
            if len(data) > 0:
                for i, name in enumerate(names):
                    p1 = name.find('(')
                    p2 = name.find(')')
                    unit = ''
                    if (p1 > 0) & (p2 > p1):
                        unit = name[p1 + 1: p2].strip()
                    key = name[0:p1].strip() if p1 > 0 else name.strip()
                    self.names.append(key)
                    self.units.append(unit)
                    self[key] = data[:,i]


class Results(object):

    def __init__(self, filename='',IO_version=None):
        self.history = HistoryFile()
        self.particles = []
        self.IO_version = IO_version
        if filename:
            self.read(filename)

    def clear(self):
        self.history.clear()
        self.particles.clear()

    def _create_chem(self, ndomains, elements, phases):
        """ Create a new ChemistrySizeDistribution """
        X0 = np.zeros((len(elements), ), dtype=float)
        chem = ChemistrySizeDistribution(elements=elements,
                                         X0=X0,
                                         phases=phases)
        nelements = len(chem.elements)
        chem.Xd = np.zeros((ndomains, nelements))
        chem.Xi = np.zeros((ndomains, nelements))
        chem.rd = np.zeros((ndomains, ))
        chem.shape = np.ones((ndomains, ))
        chem.Nd = np.zeros((ndomains, ))
        width = max([len(p) for p in chem.phases])
        chem.phasenames = np.zeros((ndomains, ), dtype='U{}'.format(width))
        chem.atvol = np.ones((ndomains, ))
        chem.atvol0 = 1.0

        return chem

    def get_IO_version(self,filename):
        """ get the IO_version from the header of the file"""
        with open(filename) as fil:
            for line in fil.readlines():
                if "IO_version:" in line:
                    self.IO_version = int(line.strip().split(":")[1])
                    break
        if self.IO_version is None:
            self.IO_version = 1
            raise Warning("IO_version not found in "+filename+ " version 1 is used")

    def read_particles_v1(self, filename):
        """ Read particles file """
        with open(filename) as fil:
            lines = fil.read().split('\n')
        values = {}
        domains = []
        keys = 'ndomains,nelements,nphases,Init,Solid,Phase composition,DomainID'.split(',')
        index = {}
        for i, line in enumerate(lines):
            for key in keys:
                if line.find(key) == 0:
                    index[key] = i
            if 'DomainID' in index:
                break

        for key in ['ndomains', 'nelements', 'nphases']:
            if key in index:
                kv = lines[index[key]].split(':')
                values[key] = int(kv[1])

        i = index['nphases'] + 1
        for key in ['elements', 'phases']:
            values[key] = []
            for j in range(values['n' + key]):
                values[key].append(lines[i].strip())
                i += 1

        for key in ['Init', 'Solid', 'Phase composition']:
            values[key] = []
            i = index[key] + 1
            if key == 'Phase composition': i = index[key] + 2
            for j in range(values['nelements']):
                values[key].append(float(lines[i]))
                i += 1

        i = index['DomainID'] + 1
        for j in range(values['ndomains']):
            items = [item.strip() for item in lines[i].split()]
            domains.append([float(x) for x in items])
            i += 1
        domains = np.array(domains)

        values['phases'].insert(0, 'matrix')
        chem = self._create_chem(values['ndomains'],
                                 values['elements'],
                                 values['phases'])
        chem.X0 = np.array(values['Init'])
        for j in range(values['ndomains']):
            chem.Xd[j,:] = np.array(values['Phase composition'])
        chem.rd = domains[:,1]
        chem.shape = domains[:,2]
        chem.Nd = domains[:,3]
        phases = values['phases']
        phaseid = np.array(domains[:,4], 'i')
        for d in range(values['ndomains']):
            chem.phasenames[d] = phases[phaseid[d]]

        # deactivated as it will not reflect the content of premod state
        #chem.atvol = chem.estimated_atvol()
        #chem.atvol0 = chem.estimated_atvol('nominal')

        return chem

    def check_dataFrame(self, metadata, df):
        bool_alpha = False
        for key,value in metadata.items():
            if key == 'Xd_AlphaPhase':
                bool_alpha = True
        if bool_alpha:
            ndomains = int(metadata['ndomains'])
            start_ID = np.argwhere(df['phaseID[-]']==2).flatten()[0]
            end_ID = ndomains-1
            nAlpha = end_ID-start_ID+1
            ndomains = ndomains-nAlpha
            metadata['ndomains'] = '{}'.format(ndomains)
            metadata['nphases'] = '{}'.format(int(metadata['nphases'])-1)
            metadata['phases'] = metadata['phases'][:-1]
            metadata.pop('Xd_AlphaPhase')
            df = df.drop([start_ID+i for i in range(nAlpha)])
        if int(metadata['nphases']) > 1:
            raise Exception('PyPremod can not handle multiphase for now.')
        return metadata, df
        
    def read_particles_v2(self, filename):
        """ parsing should be based on the new format"""
        metadata, df = parse_complete(filename)
        #print("*** read_particles_v2 ***\n",metadata,"\n\n",df,"\n\n")
        # post-treatment of the metadata
        # convert to float

        # Clean metadata and dataframe for alpha-phase
        metadata, df = self.check_dataFrame(metadata,df)

        for key,value in metadata.items():
            if key == "X0" or "Xd_" in key or key == "XSS":
                metadata[key] = [float(val) for val in value]
            elif key in ['IO_version','ndomains','nelements','nphases']:
                metadata[key] = int(value)
        #print("*** read_particles_v2 ***\n",metadata,"\n\n",df,"\n\n")
        chem = define_chem_premod(metadata,df)

        return chem

    def read_particles(self,filename):
        """ read the particles data depending on the IO_version"""
        self.get_IO_version(filename)

        #print("*********** filename=",filename)
        #print("IO_version=",self.IO_version)
        if self.IO_version == 1:
            return self.read_particles_v1(filename)
        elif self.IO_version == 2 or self.IO_version == 3:
            return self.read_particles_v2(filename)
        else:
            raise ValueError("In read_particles, IO_version number not valid: "
                            ,self.IO_version)


    def read_particle_evolution(self, pattern, times, temperatures):
        """ Read particles outputs """
        self.particles.clear()
        for filename in glob(pattern):
            basename = os.path.splitext(os.path.basename(filename))[0]
            parts = basename.split('Micro_')
            #raise Exception(basename, pattern, parts)
            if len(parts) == 2:
                chem = self.read_particles(filename)
                if chem:
                    tim = float(parts[1])
                    item = {'time': tim,
                            'temperature': np.interp(tim, times, temperatures),
                            'chem': chem}
                    self.particles.append(item)
        self.particles.sort(key=lambda item: item['time'])

    def read(self, filename, inp=None):
        dirname = os.path.dirname(filename)
        base = os.path.splitext(os.path.basename(filename))[0]
        ppt = os.path.join(dirname, base, base + '_PPT.txt')
        self.history.read(ppt)
        micro = os.path.join(dirname, base, base + '_Micro_*.txt')
        if inp is None:
            inp = PremodInputs(filename)
        times = np.array(inp.process.column(0, 'float'))
        temperatures = np.array(inp.process.column(1, 'float'))
        self.read_particle_evolution(micro, times, temperatures)

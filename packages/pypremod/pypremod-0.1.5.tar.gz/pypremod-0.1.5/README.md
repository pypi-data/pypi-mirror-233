Python package for Premod solver
================================

This folder contains the premod python package.
It's helping to work with the Premod solver: pre- and post-processing.

Setting-up the work environment
--------------------------------

To use the python package for Premod, python needs to be install on the machine.
Python can be downloaded from https://www.python.org/downloads/.
Please check that python is included in the PATH variable. You can test if the
following command work and returns the python version you have installed:

```
python --version
```

After installation of python, it is recommended to work on a virtual environment.
The virtual environment is a working space where only specific modules are installed.
It enables a better control of the packages and often prevents conflicts.

### Virtualenv installation

Virtualenv is a package that enables the management of virtual environment. Other solutions exist. 

PIP is a package manager for Python packages that will facilitate the installation
and version control of the required packages. It is normally installed during python installation.

To install virtualenv package: 

```pip install virtualenv```

*Remark*: depending on the system, it is sometimes necessary to use python3 or pip3

For Windows system, we install in addition another package(https://pypi.org/project/virtualenvwrapper-win/):

```pip install virtualenvwrapper-win```

For that additional package we need to define the location where all our virtual environments will be stored: WORKON_HOME to be defined in the environment variables of the system. 
On windows, you can access them through the search bar with "edit the system environment variables".

Prior to the installation of any package, we need to create a virtual environment:

```
mkvirtualenv environment_name
```

Every time we want to work on that environment we need to type:

```
workon environment_name
```

To leave the virtual environment:

```
deactivate
```


### Premod installation from pip

The package latest available version is available as pypremod (https://pypi.org/project/pypremod/).
Therefore to install it you only need:

```
pip install pypremod
```



Install from the source
---------------------------

```
cd premod/python
pip install --editable . --user
pytest
```

Using Premod
-------------------------

The python Premod package is just a way to facilitate the use of Premod.
The calculation will require the installation of an executable.

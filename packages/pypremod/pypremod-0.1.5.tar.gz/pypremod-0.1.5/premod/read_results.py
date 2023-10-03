import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import json
import dlite
from pathlib import Path

# standard plot
def standardplotVf():
    """
    """
    for element in fracs:
        plt.plot(times, df[element], label = element)
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Volume fraction')
    plt.show()
    return

# pie chart

def piechartVf():
    """
    """
    fig, ax = plt.subplots(ncols=len(times), figsize = (12,3))
    for i, row in df.iterrows():
        ax[i].pie(np.array([row['X_Mg (at_frac)'], row['X_Si (at_frac)'], row['X_Mn (at_frac)'], row['X_Fe (at_frac)']]), 
                labels = ['Mg', 'Si', 'Mn', 'Fe'],
                startangle = 90)
        ax[i].set_title(f"t = {int(row['Time (s)'])}")
    plt.show()
    return

def rv_Nd():
    """
    """
    plt.plot(df['rv_avg (m)'], df['Nv (m-3)'])
    plt.xlabel('rv')
    plt.ylabel('Nv')
    plt.show()
    return

def formatting_hist(): #a modifier
    """
    """
    # creer entite
    local_dir = Path(__file__).parent.resolve()
    os.chdir(local_dir)
    entity_path = "./entities/"   \
                  "entity_particlesizedistribution-0.1.json"
    #print(entity_path)
    dlite.storage_path.append(f'{entity_path}')
    alloyEntity = Instance.from_url(entity_path)

    # charger donnees read_csv
    df = pd.read_csv('fichier', sep=';', comment='#')

    # ouvrir le ficher txt pour avoir la list des lignes qui commence pqr diese pour recuperer les compo de la phase
    # convertir en dict 
    df.to_dict()

    # extract data
    # Time (s);Temp (K);fv (-);rv_avg (m);Nv (m-3);X_Al (at_frac);X_Mg (at_frac);X_Si (at_frac);X_Mn (at_frac);X_Fe (at_frac);X_Cu (at_frac)
    # list element;
    # nom des phases a ajouter dans la partie fortran, compo fixee
                                                                                                                                                                          
    results = {}
    results["dimensions"] = []
    results["dimensions"].append({"nelements" : nelements})
    results["nphases"].append({"nphases" : nphases})
    results["ntimestep"].append({"ntimestep" : ntimestep})

    results["properties"] = []
    results["properties"].append({"elements" : elements})
    results["properties"].append({"phases" : phases})
    results["properties"].append({"X0" : X0})
    results["properties"].append({"Xp" : Xp})
    results["properties"].append({"volfrac" : volfrac})
    results["properties"].append({"rmean" : rmean})
    results["properties"].append({"atvol" : atvol})
    
    with open(example + 'results', "w") as fp:
        json.dump(results, fp, indent=4) 
    return results


def formatting_chem():
    """
    """
    results = {}
    results["dimensions"] = []
    results["dimensions"].append({"nelements" : nelements})
    results["nphases"].append({"nphases" : nphases})

    results["properties"] = []
    results["properties"].append({"elements" : elements})
    results["properties"].append({"phases" : phases})
    results["properties"].append({"X0" : X0})
    results["properties"].append({"Xp" : Xp})
    results["properties"].append({"volfrac" : volfrac})
    results["properties"].append({"rmean" : rmean})
    results["properties"].append({"atvol" : atvol})
    
    with open(example + 'results', "w") as fp:
        json.dump(results, fp, indent=4) 
    return results


def test_read_results():
    dirname = os.path.dirname(__file__)
    example = 'TestMyhr2001'

    df = pd.read_table(dirname+'\\'+example+'\\'+example+'_summary.txt', sep=';', encoding='utf8')
    #print(df.head())
    #print(df.keys())
    times = list(df['Time (s)'])
    fracs = ['X_Mg (at_frac)', 'X_Si (at_frac)', 'X_Mn (at_frac)', 'X_Fe (at_frac)']



#-------------------------------------------------------------------------------
if __name__ == "__main__":
    
    standardplotVf()
    rv_Nd()
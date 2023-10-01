"""
THIS FILE USED TO GENERATE ANY POLYMER 3D STRUCTURE AND TOPOLOGY FILES FOR MD SIMULATION.
@author: Abd. Kakhar Umar abdulkaharumar@gmail.com
"""

import os.path
import json
import math
import pickle
import random
import argparse
import subprocess
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.MolStandardize import rdMolStandardize
from polyflin.BOSSReader import BOSSReader, CheckForHs
from polyflin.BOSS2OPENMM import mainBOSS2OPM
from polyflin.BOSS2CHARMM import mainBOSS2CHARMM
from polyflin.BOSS2GMX import mainBOSS2GMX
from polyflin.BOSS2XPLOR import mainBOSS2XPLOR
from polyflin.BOSS2Q import mainBOSS2Q
from polyflin.BOSS2LAMMPS import mainBOSS2LAMMPS
from polyflin.BOSS2DESMOND import mainBOSS2DESMOND 
from polyflin.BOSS2TINKER import mainBOSS2TINKER 
from polyflin.createZmat import genMolRep


def get_mol(input_file):
    mol = None
    if ".smi" in input_file:
        smi = open(input_file, "r").readline().strip().split()[0]
        mol = Chem.RemoveHs(Chem.MolFromSmiles(smi))
        
    elif ".mol" in input_file:
        mol = Chem.MolFromMolFile(input_file)  
    
    elif ".pdb" in input_file:
        mol = Chem.MolFromPDBFile(input_file)  
        AllChem.Compute2DCoords(mol)
        
    elif ".xyz" in input_file:
        mol = Chem.MolFromXYZFile(input_file)  
        AllChem.Compute2DCoords(mol)
        
    elif ".mol2" in input_file:
        mol = Chem.MolFromMol2File(input_file)
        AllChem.Compute2DCoords(mol)
        
    else:
        print("The input file type is not recognized")
        exit()
        
    return mol


def mol_with_atom_index( mol ):
    atoms = mol.GetNumAtoms()
    for idx in range( atoms ):
        mol.GetAtomWithIdx( idx ).SetProp( 'molAtomMapNumber', str( mol.GetAtomWithIdx( idx ).GetIdx() ) )
    return mol


def combMols(sequence, monomers):
    combo_mol = Chem.Mol()
    prev_mnr = ""
    atom_nums = 0
    
    for mnr_type in sequence:
        mol_now_data = next(filter(lambda x: x["code"] == mnr_type, monomers), None)
        mol_now = mol_now_data.get("mol", None)
        
        if(len(combo_mol.GetAtoms()) > 0):
            mol_prev_data = next(filter(lambda x: x["code"] == prev_mnr, monomers), None)
            mol_prev_atoms = len(mol_prev_data.get("atoms", None)) 
            connection = next(filter(lambda x: x["to"] == mnr_type, mol_prev_data.get("connections", None)), None)
            
            my_atom = atom_nums + int(connection.get("my_atom", 0))
            to_atom = len(combo_mol.GetAtoms()) + int(connection.get("to_atom", 0))
            bond_type = connection.get("bond_type", "SINGLE")
              
            combo_mol = Chem.CombineMols(combo_mol, mol_now)
            edcombo = Chem.EditableMol(combo_mol)
            
            edcombo.AddBond(my_atom, to_atom, order=get_bond_type(bond_type))
            combo_mol = edcombo.GetMol()
            
            atom_nums += mol_prev_atoms       

        else:
            combo_mol = Chem.CombineMols(combo_mol, mol_now)
                    
        prev_mnr = mnr_type
    
    return combo_mol


def get_bond_type(bond_type):
    if(bond_type == "SINGLE"):
        bond_type = Chem.rdchem.BondType.SINGLE
    elif(bond_type == "DOUBLE"):
        bond_type = Chem.rdchem.BondType.DOUBLE
    else:
        bond_type = Chem.rdchem.BondType.AROMATIC
    
    return bond_type


def round_down_to_non_zero(number):
    rounded_down = math.floor(number)
    if rounded_down == 0:
        return math.ceil(number)
    return rounded_down


def optimize_mol(forcefield, mol):
    optimized_mol = Chem.Mol()
    optimized_mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(optimized_mol, useRandomCoords=True)
    if forcefield is not None:
        if forcefield == "MMFF":
            AllChem.MMFFOptimizeMolecule(optimized_mol)
        else:
            AllChem.UFFOptimizeMolecule(optimized_mol)
            
    return optimized_mol


def writing_output(format, mol, output, forcefield, hydrogen, ob_func):
    new_smi = Chem.MolToSmiles(mol)
    std_smi = rdMolStandardize.StandardizeSmiles(new_smi)
    new_mol = Chem.MolFromSmiles(std_smi)
    AllChem.Compute2DCoords(new_mol)
    AllChem.ComputeGasteigerCharges(new_mol)
    current_path = os.getcwd()
    
    cmd = ""
    if ob_func is not None:
        cmd = " " + ob_func
    
    if hydrogen != "FALSE":
        new_mol = Chem.AddHs(new_mol)
    
    if forcefield is not None:
        new_mol = optimize_mol(forcefield, new_mol)
    
    if not os.path.exists(str(output)+".pdb"):
        writer = Chem.PDBWriter(str(output) + ".pdb")
        writer.write(new_mol)
        writer.close()
    
    if format == "TOP":
        if not os.path.exists(str(output)+".mol"):
            process = subprocess.Popen('obabel %s.pdb -O %s.mol --gen3D%s' % (output, output, cmd), shell=True)
            process.wait()  
        
        charge = 0
        optim = 0
        lbcc = False
        resname = "POL"
        clu = False
        if charge == 0:
            lbcc = True
            print('LBCC converter is activated')
        else:
            lbcc = False
            print('1.14*CM1A-LBCC is only available for neutral molecules\nAssigning unscaled CM1A charges')
        
        
        # Remove temporary XML file if it exists
        if os.path.exists(f'{current_path}/tmp/{resname}.xml'):
            subprocess.run(['rm', f'{current_path}/tmp/{resname}.*'])
        
        process = subprocess.Popen(f'mkdir {current_path}/tmp/', shell=True)
        process.wait()
        
        subprocess.run(['cp', f'{output}.mol', f'{current_path}/tmp/{output}.mol'])
        
        os.chdir(f'{current_path}/tmp/')
        genMolRep(f'{output}.mol', resname, charge)
        mol = BOSSReader(f'{resname}.z', optim, charge, lbcc)
        
        # Perform assertions based on molecular properties
        assert mol.MolData['TotalQ']['Reference-Solute'] == charge, "PROPOSED CHARGE IS NOT POSSIBLE: SOLUTE MAY BE AN OPEN SHELL"
        assert CheckForHs(mol.MolData['ATOMS']), "Hydrogens are not added. Please add Hydrogens"
    
        pickle.dump(mol, open(resname + ".p", "wb"))
        
        try:
            mainBOSS2OPM(resname, clu)
            print('Input files for OPENMM have been exported!')
        except ValueError as e:
            pass
        
        try:
            mainBOSS2GMX(resname, clu)
            print('Input files for GROMACS have been exported!')
        except ValueError as e:
            pass
        
        try:
            mainBOSS2LAMMPS(resname, clu)
            print('Input files for LAMMPS have been exported!')
        except ValueError as e:
            pass
        
        try:
            mainBOSS2DESMOND(resname, clu)
            print('Input files for DESMOND have been exported!')
        except ValueError as e:
            pass
        
        try:
            mainBOSS2TINKER(resname, clu)
            print('Input files for TINKER have been exported!')
        except ValueError as e:
            pass
        
        try:
            mainBOSS2Q(resname, clu)
            print('Input files for Q have been exported!')
        except ValueError as e:
            pass
        
        try:
            mainBOSS2CHARMM(resname, clu)
            print('Input files for CHARMM/NAMD have been exported!')
        except ValueError as e:
            pass
        
        try:  
            mainBOSS2XPLOR(resname, clu)
            print('Input files for XPLOR have been exported!')
        except ValueError as e:
            pass
        
        os.remove(resname + ".p")
        mol.cleanup()
    else:
        process = subprocess.Popen('obabel %s.pdb -O %s.%s%s' % (output, output, format, cmd), shell=True)
        process.wait()
        
        print(f'The {output}.{format} file has been exported!')


def make_cyclic(temp_chain, sequence, cyclic):
    bond_type = cyclic.get("bond_type", "SINGLE")
    head_mol = cyclic.get("head_mol", None)
    head_atom = cyclic.get("head_atom", None)
    tail_mol = cyclic.get("tail_mol", None)
    tail_atom = cyclic.get("tail_atom", None)
    
    total_atoms_before_head = 0
    for index, monomer in enumerate(sequence):
        if index == head_mol:
            break
        else:
            mol = next(filter(lambda x: x["code"] == monomer, monomers), None).get("atoms", 0)
            total_atoms_before_head += len(mol)
    
    head_atom_new_index = total_atoms_before_head + head_atom
    
    total_atoms_before_tail = 0
    for index, monomer in enumerate(sequence):
        if index == tail_mol:
            break
        else:
            mol = next(filter(lambda x: x["code"] == monomer, monomers), None).get("atoms", 0)
            total_atoms_before_tail += len(mol)
    
    tail_atom_new_index = total_atoms_before_tail + tail_atom
    
    temp_edit = Chem.EditableMol(temp_chain)
    temp_edit.AddBond(head_atom_new_index, tail_atom_new_index, order=get_bond_type(bond_type))
    temp_chain = temp_edit.GetMol()
    
    return temp_chain


def clean_valence(mol, atom_id):
    atom_N = mol.GetAtomWithIdx(atom_id)
    num_bonds_N = atom_N.GetTotalNumHs() + atom_N.GetDegree()

    if num_bonds_N == 3:
        
        idx_hydrogen = None
        for neighbor in atom_N.GetNeighbors():
            print(neighbor.GetSymbol())
            if neighbor.GetSymbol() == "H":
                idx_hydrogen = neighbor.GetIdx()
                break

        if idx_hydrogen is not None:
            bond_idx = mol.GetBondBetweenAtoms(atom_id, idx_hydrogen).GetIdx()
            mol.RemoveBond(bond_idx)

            # Hapus atom hidrogen dari molekul
            mol.RemoveAtom(idx_hydrogen)
    
    return mol


#USAGE: monomers, chains, output, atoms_map = getData('config.json')
def getData(config_file):
    config = json.loads(open(config_file, "r").read())
    monomers = config.get("monomers", None)
    chains = config.get("chains", None)
    output = config.get("output", None)
    atoms_map = []

    #MAPPING MONOMERS
    if monomers is not None:
        for monomer in monomers:
            mol = get_mol(monomer["file"])
            monomer["mol"] = mol
            monomer["atoms"] = mol.GetAtoms()

    #MAPPING ATOMS
    if chains is not None:
        cur_index = 0
        
        for chain in chains:
            code = chain.get("code", None)
            sequence = chain.get("sequence", None)
            chain_nums = chain.get("nums", None)
            
            for _ in range(chain_nums):
            
                for monomer in sequence:
                    mol = next(filter(lambda x: x["code"] == monomer, monomers), None).get("mol", 0)
                    mol_atoms = mol.GetAtoms()
                    for atom in mol_atoms:
                        item = {
                            "chain":code,
                            "monomer":monomer,
                            "original_id":atom.GetIdx(),
                            "symbol":atom.GetSymbol(),
                            "new_id":cur_index,
                            "injected":"FALSE"
                        }
                        
                        atoms_map.append(item)
                        cur_index += 1

    return monomers, chains, output, atoms_map


#USAGE: polymer = createChains(chains, monomers, atoms_map); Chem.Mol() object
def createChains(chains, monomers, atoms_map):
    final_mol = Chem.Mol()
    if chains is not None:
        
        for chain in chains:
            
            #GET CHAIN PROPERTIES
            sequence = chain.get("sequence", None)
            cyclic = chain.get("cyclic", None)
            chain_nums = chain.get("nums", 1)
            connections = chain.get("connections", None)        
            
            for _ in range(chain_nums):
                total_atoms = len(final_mol.GetAtoms())
                temp_chain = combMols(sequence, monomers)
                
                #MAKE CYCLIC
                if cyclic is not None:
                    temp_chain = make_cyclic(temp_chain, sequence, cyclic)        
                    
                    
                final_mol = Chem.CombineMols(final_mol, temp_chain)
                
                
                
                #MAKE BRANCH
                if connections is not None:
                    
                    for connection in connections:
                        #GET TO_CHAIN ATOM REAL INDEX
                        bond_type = connection.get("bond_type", None)
                        to_chain = connection.get("to_chain", None)
                        to_mol = connection.get("to_mol", None)
                        to_atom = connection.get("to_atom", None)
                        randomness = connection.get("random", "FALSE")
                        
                        
                        if not isinstance(to_atom, list):
                            to_atom = [to_atom]
                        
                        
                        new_to_mol = to_mol
                        seq = None
                        if isinstance(to_mol, int):
                            seq = next(filter(lambda x: x["code"] == to_chain, chains)).get("sequence", None)
                            new_to_mol = seq[to_mol]
                            
                        atom_array = filter(lambda x: x["chain"] == to_chain and x["monomer"] == new_to_mol and (x["original_id"] in to_atom or x["symbol"] in to_atom) and x["injected"] == "FALSE", atoms_map)
                            
                        
                        to_cur_atom = None
                        if randomness == "TRUE":
                            to_cur_atom = random.choice(list(atom_array))
                        elif isinstance(to_mol, int):
                            atom_array = filter(lambda x: x["chain"] == to_chain and x["monomer"] == new_to_mol and (x["original_id"] in to_atom or x["symbol"] in to_atom), atoms_map)
                            num_of_the_same_monomer_before_to_mol = ''.join([c for c in seq[:to_mol] if c == new_to_mol]) 
                            to_cur_atom = list(atom_array)[len(num_of_the_same_monomer_before_to_mol)]
                        else:
                            to_cur_atom = next(atom_array) 
                        
                                            
                        to_new_index = to_cur_atom.get("new_id", None)
                        atoms_map = [{**item, "injected": "TRUE"} if item["new_id"] == to_new_index else item for item in atoms_map]
                                            
                        
                        #GENERATE BRANCH NEW INDEX
                        my_mol = connection.get("my_mol", None)
                        my_atom = connection.get("my_atom", None)
                        my_new_index = my_atom
                        for index, monomer in enumerate(sequence):
                            if index == my_mol:
                                break
                            else:
                                mol = next(filter(lambda x: x["code"] == monomer, monomers), None).get("atoms", 0)
                                my_new_index += len(mol)
                                
                        my_new_index += total_atoms
                                            
                        final_edit = Chem.EditableMol(final_mol)
                        final_edit.AddBond(to_new_index, my_new_index, order=get_bond_type(bond_type))
                        final_mol = final_edit.GetMol()
                        final_mol.UpdatePropertyCache(strict=False)
                        Chem.SanitizeMol(final_mol, Chem.SanitizeFlags.SANITIZE_ADJUSTHS|Chem.SanitizeFlags.SANITIZE_FINDRADICALS|Chem.SanitizeFlags.SANITIZE_KEKULIZE|Chem.SanitizeFlags.SANITIZE_SETAROMATICITY|Chem.SanitizeFlags.SANITIZE_SETCONJUGATION|Chem.SanitizeFlags.SANITIZE_SETHYBRIDIZATION|Chem.SanitizeFlags.SANITIZE_SYMMRINGS,catchErrors=True)
                        Chem.Kekulize(final_mol, clearAromaticFlags=True)
    
        return final_mol                    
    else:
        print("Chain parameter is not defined")
        exit()


#USAGE: exportFiles(output, polymer)
def exportFiles(output, polymer):
    print("Finish making the polymer! Preparing the output!")
    for format in output["format"]:
        writing_output(format, polymer, output.get("name", None), output.get("forcefield", None), output.get("add_hydrogen", "FALSE"), output.get("obabel_func", None))


if __name__=="__main__":

    #GET CONFIG
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config-file", required=True,  help="Configuration file in json format")

    args = parser.parse_args()
    config_file = args.config_file



    #DETERMINE THE PARAMETERS
    config = json.loads(open(config_file, "r").read())
    monomers = config.get("monomers", None)
    chains = config.get("chains", None)
    output = config.get("output", None)
    atoms_map = []

    if monomers is not None:
        for monomer in monomers:
            mol = get_mol(monomer["file"])
            monomer["mol"] = mol
            monomer["atoms"] = mol.GetAtoms()



    #MAPPING ATOMS
    if chains is not None:
        cur_index = 0
        
        for chain in chains:
            code = chain.get("code", None)
            sequence = chain.get("sequence", None)
            chain_nums = chain.get("nums", None)
            
            for _ in range(chain_nums):
            
                for monomer in sequence:
                    mol = next(filter(lambda x: x["code"] == monomer, monomers), None).get("mol", 0)
                    mol_atoms = mol.GetAtoms()
                    for atom in mol_atoms:
                        item = {
                            "chain":code,
                            "monomer":monomer,
                            "original_id":atom.GetIdx(),
                            "symbol":atom.GetSymbol(),
                            "new_id":cur_index,
                            "injected":"FALSE"
                        }
                        
                        atoms_map.append(item)
                        cur_index += 1



    #MAKING THE POLYMER
    print("Making the polymer!")
    final_mol = Chem.Mol()
    if chains is not None:
        
        for chain in chains:
            
            #GET CHAIN PROPERTIES
            sequence = chain.get("sequence", None)
            cyclic = chain.get("cyclic", None)
            chain_nums = chain.get("nums", 1)
            connections = chain.get("connections", None)        
            
            for _ in range(chain_nums):
                total_atoms = len(final_mol.GetAtoms())
                temp_chain = combMols(sequence, monomers)
                
                #MAKE CYCLIC
                if cyclic is not None:
                    temp_chain = make_cyclic(temp_chain, sequence, cyclic)        
                    
                    
                final_mol = Chem.CombineMols(final_mol, temp_chain)
                
                
                
                #MAKE BRANCH
                if connections is not None:
                    
                    for connection in connections:
                        #GET TO_CHAIN ATOM REAL INDEX
                        bond_type = connection.get("bond_type", None)
                        to_chain = connection.get("to_chain", None)
                        to_mol = connection.get("to_mol", None)
                        to_atom = connection.get("to_atom", None)
                        randomness = connection.get("random", "FALSE")
                        
                        
                        if not isinstance(to_atom, list):
                            to_atom = [to_atom]
                        
                        
                        new_to_mol = to_mol
                        seq = None
                        if isinstance(to_mol, int):
                            seq = next(filter(lambda x: x["code"] == to_chain, chains)).get("sequence", None)
                            new_to_mol = seq[to_mol]
                            
                        atom_array = filter(lambda x: x["chain"] == to_chain and x["monomer"] == new_to_mol and (x["original_id"] in to_atom or x["symbol"] in to_atom) and x["injected"] == "FALSE", atoms_map)
                            
                        
                        to_cur_atom = None
                        if randomness == "TRUE":
                            to_cur_atom = random.choice(list(atom_array))
                        elif isinstance(to_mol, int):
                            atom_array = filter(lambda x: x["chain"] == to_chain and x["monomer"] == new_to_mol and (x["original_id"] in to_atom or x["symbol"] in to_atom), atoms_map)
                            num_of_the_same_monomer_before_to_mol = ''.join([c for c in seq[:to_mol] if c == new_to_mol]) 
                            to_cur_atom = list(atom_array)[len(num_of_the_same_monomer_before_to_mol)]
                        else:
                            to_cur_atom = next(atom_array) 
                        
                                            
                        to_new_index = to_cur_atom.get("new_id", None)
                        atoms_map = [{**item, "injected": "TRUE"} if item["new_id"] == to_new_index else item for item in atoms_map]
                                            
                        
                        #GENERATE BRANCH NEW INDEX
                        my_mol = connection.get("my_mol", None)
                        my_atom = connection.get("my_atom", None)
                        my_new_index = my_atom
                        for index, monomer in enumerate(sequence):
                            if index == my_mol:
                                break
                            else:
                                mol = next(filter(lambda x: x["code"] == monomer, monomers), None).get("atoms", 0)
                                my_new_index += len(mol)
                                
                        my_new_index += total_atoms
                                            
                        final_edit = Chem.EditableMol(final_mol)
                        final_edit.AddBond(to_new_index, my_new_index, order=get_bond_type(bond_type))
                        final_mol = final_edit.GetMol()
                        final_mol.UpdatePropertyCache(strict=False)
                        Chem.SanitizeMol(final_mol, Chem.SanitizeFlags.SANITIZE_ADJUSTHS|Chem.SanitizeFlags.SANITIZE_FINDRADICALS|Chem.SanitizeFlags.SANITIZE_KEKULIZE|Chem.SanitizeFlags.SANITIZE_SETAROMATICITY|Chem.SanitizeFlags.SANITIZE_SETCONJUGATION|Chem.SanitizeFlags.SANITIZE_SETHYBRIDIZATION|Chem.SanitizeFlags.SANITIZE_SYMMRINGS,catchErrors=True)
                        Chem.Kekulize(final_mol, clearAromaticFlags=True)
                        
    else:
        print("Chain parameter is not defined")
        exit()



    #STRUCTURE FINALIZATION
    print("Finish making the polymer! Preparing the output!")
    for format in config["output"]["format"]:
        writing_output(format, final_mol, output.get("name", None), output.get("forcefield", None), output.get("add_hydrogen", "FALSE"), output.get("obabel_func", None))



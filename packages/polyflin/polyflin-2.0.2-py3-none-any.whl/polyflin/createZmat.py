import os
import subprocess
import numpy as np
import collections
import networkx as nx
from polyflin.Vector_algebra import pairing_func, angle, dihedral, tor_id, ang_id, bossElement2Num, Distance


def mol_to_z_matrix(ifile, resid):    
    mollines = open(ifile, 'r').readlines()
        
    COOS, ATYPES, MolBonds = read_mol_lines(mollines)
    G_mol, mol_icords = make_graphs(ATYPES, COOS, MolBonds)
    save_z_matrix(ATYPES, G_mol, mol_icords, COOS, '%s.z' % resid, resid)
    
    return None


def canonalize_z_matrix(ifile, resid):
    process = subprocess.Popen('obabel %s -O %s --canonical' % (ifile, ifile), shell=True)
    process.wait() 
     
    mollines = open(ifile, 'r').readlines()
    
    COOS, ATYPES, MolBonds = read_mol_lines(mollines)
    G_mol, mol_icords = make_graphs(ATYPES, COOS, MolBonds)
    save_z_matrix(ATYPES, G_mol, mol_icords, COOS, '%s.z' % resid, resid)
    
    return None


def genMolRep(ifile, resid, charge):
    current_path = os.getcwd()
        
    try:
        mol_to_z_matrix(ifile, resid)
        
    except (ZeroDivisionError, IndexError):
        print('Warning!!\n 1.Cannonicalising Input MOL file\n 2.Atom ordering may change \n 3.But the Coordinates remain the same')
        canonalize_z_matrix(ifile, resid)
        
    getOpt(f'{resid}.z', charge)
    
    if os.path.exists(f'{current_path}/clu.pdb'):
        os.remove(f'{current_path}/clu.pdb')
            
    return True


def getOpt(zmat, charge):
    current_path = os.getcwd()
    assert os.path.isfile(zmat), f'File named {zmat} does not exist'
    
    boss_dir = os.environ.get('BOSSdir')
    assert boss_dir and os.path.isfile(os.path.join(boss_dir, 'scripts/xZCM1A')), \
            'Please make sure $BOSSdir is defined and xZCM1A and related files are in the scripts directory of BOSS'
    
    execs = {
        2: f'{boss_dir}/scripts/xZCM1A+2 > {current_path}/olog',
        1: f'{boss_dir}/scripts/xZCM1A+  > {current_path}/olog',
        0: f'{boss_dir}/scripts/xZCM1A > {current_path}/olog',
        -1: f'{boss_dir}/scripts/xZCM1A-  > {current_path}/olog',
        -2: f'{boss_dir}/scripts/xZCM1A-2 > {current_path}/olog',
        'OPT': f'{boss_dir}/scripts/xOPT > {current_path}/olog'
    }
    
    print(f'MOLECULE HAS A CHARGE of {charge}')
    execfile = execs[charge]
    coma = f'{execfile} {zmat[:-2]}'
    subprocess.run(coma, shell=True)
    subprocess.run(f'cp sum {zmat}', shell=True)
    
    execfile_spm = f'{boss_dir}/scripts/xSPM > {current_path}/olog'
    coma_spm = f'{execfile_spm} {zmat[:-2]}'
    subprocess.run(coma_spm, shell=True)
    subprocess.run(f'/bin/cp sum {zmat}', shell=True)
    
    return None


def read_mol_lines(mollines):
    nats, nbonds = int(mollines[3][0:3]), int(mollines[3][3:6])
    cooslines = mollines[4:4 + nats]
    coos = {}
    atypes = {}
    
    for i, line in enumerate(cooslines):
        els = line.split()
        coos[i + 1] = [float(e) for e in els[0:3]]
        atypes[i + 1] = els[3]
    
    bondlines = mollines[4 + nats:4 + nats + nbonds]
    bonds = {'BI': [], 'BJ': [], 'RIJ': [], 'UID': []}
    
    for line in bondlines:
        bi, bj = int(line[0:3]), int(line[3:6])
        bonds['BI'].append(bi)
        bonds['BJ'].append(bj)
        bonds['RIJ'].append(Distance(coos[bi], coos[bj]))
        bonds['UID'].append(pairing_func(bi, bj))
    
    return coos, atypes, bonds


def make_graphs(atoms, coos, bonds):
    G = nx.DiGraph()
    # ADD NODES USING ATOM TYPES AND COORDINATES
    for i in coos.keys():
        G.add_node(i, XYZ=coos[i], elem=atoms[i],
                   atno=bossElement2Num(atoms[i]))
    for (i, j, rij) in zip(bonds['BI'], bonds['BJ'], bonds['RIJ']):
        G.add_edge(i, j, distance=rij)
        G.add_edge(j, i, distance=rij)
    
    all_ps = dict(nx.algorithms.all_pairs_shortest_path_length(G))
    all_paths = []
    
    for s in all_ps.keys():
        for e in all_ps[s].keys():
            if   all_ps[s][e] == 1: all_paths+=list(nx.algorithms.all_simple_paths(G,s,e,cutoff=1))
            elif all_ps[s][e] == 2: all_paths+=list(nx.algorithms.all_simple_paths(G,s,e,cutoff=2))
            elif all_ps[s][e] == 3: all_paths+=list(nx.algorithms.all_simple_paths(G,s,e,cutoff=3))

    all_bonds = [p for p in all_paths if len(set(p))==2]
    new_angs =  [p for p in all_paths if len(set(p))==3]
    new_tors =  [p for p in all_paths if len(set(p))==4]
    dict_new_tors = {tor_id(t): t for t in new_tors}
    dict_new_angs = {ang_id(t): t for t in new_angs}
    imp_keys = [n for n in G.nodes() if G.degree(n) / 2 == 3]
    all_imps = {}
    for i in imp_keys:
        nei = list(G.neighbors(i))
        if G.nodes[i]['atno'] == 6:
            all_imps[i] = [nei[0], i, nei[1], nei[2]]
            
    MOL_ICOORDS = {'BONDS': all_bonds,
                   'ANGLES': dict_new_angs, 
                   'TORSIONS': dict_new_tors, 'IMPROPERS': all_imps}
    
    return(G, MOL_ICOORDS)


def get_additional_int(mol_icords, z_bonds, z_angles, z_torsions):
    all_bonds_mol, all_angles_mol, all_torsions_mol = mol_icords['BONDS'], mol_icords['ANGLES'], mol_icords['TORSIONS']
    
    Z_B = {pairing_func(i[0] - 2, i[1] - 2): [i[0] - 2, i[1] - 2] for i in z_bonds.values()}
    Z_A = {ang_id([i[0] - 2, i[1] - 2, i[2] - 2]): [i[0] - 2, i[1] - 2, i[2] - 2] for i in z_angles.values()}
    Z_T = {tor_id([i[0] - 2, i[1] - 2, i[2] - 2, i[3] - 2]): [i[0] - 2, i[1] - 2, i[2] - 2, i[3] - 2] for i in z_torsions.values()}
    
    Z_Ad_B, Z_Ad_A, Z_Ad_T = collections.OrderedDict(), collections.OrderedDict(), collections.OrderedDict()
    
    for b_ij in all_bonds_mol:
        uid_b_ij = pairing_func(b_ij[0], b_ij[1])
        if uid_b_ij not in Z_B:
            Z_Ad_B[uid_b_ij] = [b_ij[0] + 2, b_ij[1] + 2]
    
    for a_ij, angles in all_angles_mol.items():
        if a_ij not in Z_A:
            Z_Ad_A[a_ij] = [i + 2 for i in angles]
    
    for t_ij, torsions in all_torsions_mol.items():
        if t_ij not in Z_T:
            Z_Ad_T[t_ij] = [i + 2 for i in torsions]
    
    for c in mol_icords['IMPROPERS'].values():
        Z_Ad_T["-".join(map(str, c))] = [i + 2 for i in c]
    
    return Z_Ad_B, Z_Ad_A, Z_Ad_T


def save_z_matrix(atoms, G_mol, mol_icords, coos, zmat_name, resid):
    if not zmat_name:
        zmat_name = resid
        
    Z_ATOMS = {1: 'X', 2: 'X'}
    Z_NO = {1: -1, 2: -1}
    Z_BONDS = {1: (1, 0, 0.000), 2: (2, 1, 1.00), 3: (3, 2, 1.00)}
    Z_ANGLES = {1: (1, 0, 0, 0.000), 2: (2, 1, 0, 0.000),
                3: (3, 2, 1, 90.00), 4: (4, 3, 2, 90.0)}
    Z_TORSIONS = {1: (1, 0, 0, 0, 0.00), 2: (2, 1, 0, 0, 0.00), 3: (
        3, 2, 1, 0, 0.00), 4: (4, 3, 2, 1, 0.00), 5: (5, 4, 3, 2, 90.0)}
    
    for i in range(1, len(atoms) + 1):
        Z_ATOMS[i + 2] = atoms[i]
    for i in range(1, len(atoms) + 1):
        Z_NO[i + 2] = G_mol.nodes[i]['atno']
        
    n_ats = 0
    B_LINK = {}
    
    for i in G_mol.nodes():
        if n_ats > 0:
            neigs = np.sort(list(G_mol.neighbors(i)))
            B_LINK[i] = neigs[0]
            Z_BONDS[i + 2] = (i + 2, neigs[0] + 2, G_mol[i]
                              [neigs[0]]['distance'])
        n_ats += 1
        
    n_ats = 0
    A_LINK = {}
    
    for i in G_mol.nodes():
        if n_ats > 1:
            neigs = np.sort(list(G_mol.neighbors(B_LINK[i])))
            A_LINK[i] = neigs[0]
            ang = angle(coos[i], coos[B_LINK[i]], coos[neigs[0]])
            Z_ANGLES[i + 2] = (i + 2, B_LINK[i] + 2, neigs[0] + 2, ang)
        n_ats += 1
        
    n_ats = 0
    
    for i in G_mol.nodes():
        if n_ats > 2:
            neigs =list(G_mol.neighbors(A_LINK[i]))
            neigs = np.array([j for j in neigs if j not in [i, B_LINK[i], A_LINK[i]]])
            neigs = np.sort(neigs)
            neigs = neigs[neigs<i]
            if len(neigs)<1:
               neigs = [j for j in list(G_mol.neighbors(B_LINK[i])) if j not in [i,A_LINK[i]]]
               if (B_LINK[i] in list(mol_icords['IMPROPERS'].keys())): del mol_icords['IMPROPERS'][B_LINK[i]]
            [ti, tj, tk, tl] = [i, B_LINK[i], A_LINK[i], neigs[0]]
            dihed = dihedral(coos[ti], coos[tj], coos[tk], coos[tl])
            Z_TORSIONS[i + 2] = (ti + 2, tj + 2, tk + 2, tl + 2, dihed)
        n_ats += 1
        
    Z_Ad_B, Z_Ad_A, Z_Ad_T = get_additional_int(
        mol_icords, Z_BONDS, Z_ANGLES, Z_TORSIONS)
    
    
    # PRINTING ACTUAL Z-MATRIX
    ofile = open(zmat_name, 'w+')
    ofile.write('BOSS Z-Matrix with LSDautozmat (written by Abd. Kakhar Umar)\n')
    for i in range(1, len(atoms) + 3):
        ofile.write('%4d %-3s%5d%5d%5d%12.6f%4d%12.6f%4d%12.6f%4s%5d\n'
                    % (i, Z_ATOMS[i], Z_NO[i], Z_NO[i], Z_BONDS[i][1], Z_BONDS[i][-1], Z_ANGLES[i][-2], Z_ANGLES[i][-1], Z_TORSIONS[i][-2], Z_TORSIONS[i][-1], resid[0:3], 1)
                    )
    ofile.write(
        '''                    Geometry Variations follow    (2I4,F12.6)
                    Variable Bonds follow         (I4)\n'''
                )
    for i in range(4, len(atoms) + 3):
        ofile.write('%4d\n' % i)
    ofile.write('                    Additional Bonds follow       (2I4)\n')
    if len(Z_Ad_B) > 0:
        for i in Z_Ad_B.values():
            ofile.write('%4d%4d\n' % (i[0], i[1]))
            
            
    # CREATE A FUNCTION TO DEFINE ADDITIONAL BONDS IN CASE OF RINGS
    ofile.write('''                    Harmonic Constraints follow   (2I4,4F10.4)
                    Variable Bond Angles follow   (I4)\n''')
    for i in range(5, len(atoms) + 3):
        ofile.write('%4d\n' % i)
    ofile.write('                    Additional Bond Angles follow (3I4)\n')
    if len(Z_Ad_A) > 0:
        for i in Z_Ad_A.values():
            ofile.write('%4d%4d%4d\n' % (i[0], i[1], i[2]))
            
            
    # CREATE A FUNCTION TO DEFINE ADDITIONAL BONDS IN CASE OF RINGS
    ofile.write(
        '                    Variable Dihedrals follow     (3I4,F12.6)\n')
    for i in range(6, len(atoms) + 3):
        ofile.write('%4d%4d%4d%12.6f\n' % (i, -1, -1, 0.000))
    ofile.write('                    Additional Dihedrals follow   (6I4)\n')
    if len(Z_Ad_T) > 0:
        for k in Z_Ad_T.keys():
            torsion = Z_Ad_T[k]
            ofile.write('%4d%4d%4d%4d%4d%4d\n' %
                        (torsion[0], torsion[1], torsion[2], torsion[3], -1, -1))
    ofile.write(
        '''                    Domain Definitions follow     (4I4)
                    Conformational Search (2I4,2F12.6)
                    Local Heating Residues follow (I4 or I4-I4)
                    Final blank line
''')
    ofile.close()
    return None

import os
import subprocess
import numpy as np
import pandas as pd
from collections import OrderedDict

from polyflin.fepzmat import BCC_file2zmat
from polyflin.mol_boss import new_mol_info


def mod_add_diheds(line):
    adihed = [int(l) for l in line.split()[0:4]]+[-1,-1]
    return(adihed)


def fix_add_dihed(zmat_name):
    input_file_path = f'{zmat_name}.z'
    output_file_path = f'{zmat_name}_fixed.z'

    # Read input file and extract necessary lines
    with open(input_file_path, 'r') as f:
        flines = f.readlines()
    
    imp_lines = [i for i, line in enumerate(flines) if 'Additional Dihedrals follow' in line or 'Domain Definitions follow' in line]

    # Modify and write to the output file
    with open(output_file_path, 'w+') as ofile:
        for line in flines[:imp_lines[0]]:
            ofile.write(f'{line.rstrip()}\n')
        
        for line in flines[imp_lines[0]:imp_lines[1]]:
            m_ad = mod_add_diheds(line)
            ofile.write(f'{m_ad[0]:4d}{m_ad[1]:4d}{m_ad[2]:4d}{m_ad[3]:4d}{m_ad[4]:4d}{m_ad[5]:4d}\n')
        
        for line in flines[imp_lines[1]:]:
            ofile.write(f'{line.rstrip()}\n')

    return None


def CheckForHs(atoms):
    atype = [line.split()[1][0] for line in atoms]
    ans = False
    if ('H' in atype): ans = True 
    return ans 


def bcc_db():
    '''
    19 LBCCs from 1.14*CM1A-LBCC paper
    '''
    lbcc = {'C#-C=': 0.0,
  'C-N': 0.0,
  'C-O': 0.05,
  'C-OE': 0.0,
  'C-OH': 0.0,
  'C-OS': 0.0,
  'CA-Br': 0.19,
  'CA-C': 0.0,
  'CA-C!': -0.0,
  'CA-C=': 0.0,
  'CA-CB': -0.0,
  'CA-CE': 0.0,
  'CA-CF': 0.0,
  'CA-CK': -0.0,
  'CA-CT': 0.0,
  'CA-CZ': 0.0,
  'CA-CZA': 0.0,
  'CA-Cl': 0.0,
  'CA-F': 0.13,
  'CA-I': 0.0,
  'CA-N3': 0.0,
  'CA-NC': 0.07,
  'CA-NO': -0.08,
  'CA-NP': 0.06,
  'CA-NS': 0.0,
  'CA-OH': 0.22,
  'CA-OS': -0.0,
  'CA-S': -0.0,
  'CA-SH': -0.0,
  'CAM-CA': 0.0,
  'CAM-CT': 0.0,
  'CAM-N': 0.0,
  'CAM-O': 0.0,
  'CB-C=': -0.0,
  'CB-NC': -0.0,
  'CE-O': -0.0,
  'CE-OE': 0.0,
  'CE-OS': 0.0,
  'CF-F': -0.0,
  'CF-OS': -0.0,
  'CK-O': -0.0,
  'CM-C': 0.0,
  'CM-C=': -0.0,
  'CM-CT': -0.0,
  'CM-Cl': -0.0,
  'CP-CS': 0.0,
  'CP-SA': -0.0,
  'CT-Br': 0.08,
  'CT-C': -0.0,
  'CT-C=': 0.0,
  'CT-CE': -0.0,
  'CT-CF': 0.0,
  'CT-CK': -0.0,
  'CT-CP': 0.0,
  'CT-CZ': -0.0,
  'CT-CZT': -0.0,
  'CT-Cl': 0.1,
  'CT-F': -0.0,
  'CT-I': -0.0,
  'CT-N': -0.0,
  'CT-N3': -0.0,
  'CT-NO': 0.0,
  'CT-NP': 0.04,
  'CT-NS': -0.0,
  'CT-NT': -0.0,
  'CT-OE': -0.0,
  'CT-OH': 0.1,
  'CT-OS': -0.0,
  'CT-S': 0.08,
  'CT-SH': 0.175,
  'CT-SZ': 0.0,
  'CY-C': 0.0,
  'CY-CE': 0.0,
  'CZ-NZ': -0.0,
  'CZA-NZ': 0.09,
  'CZT-NZ': 0.03,
  'H-N': -0.0,
  'H-N3': -0.0,
  'H-NP': -0.05,
  'H-NS': -0.0,
  'H-NT': -0.0,
  'HA-CA': -0.01,
  'HA-CM': 0.0,
  'HA-CP': -0.0,
  'HA-CS': -0.0,
  'HC-C': 0.0,
  'HC-C#': -0.0,
  'HC-C=': -0.0,
  'HC-CAM': 0.0,
  'HC-CE': 0.0,
  'HC-CF': -0.0,
  'HC-CM': -0.0,
  'HC-CT': 0.0,
  'HC-CY': 0.0,
  'HC-CZ': -0.0,
  'HO-OH': 0.0,
  'HS-SH': 0.0,
  'NO-ON': -0.18,
  'O-P': 0.0,
  'OS-P': 0.0,
  'OY-SZ': 0.06,
  'U-U': 0.0,
  'X-X': 0.0}
    db = OrderedDict(lbcc)
    return db


def refine_pdb_lines(fname):
    filen = fname if os.path.exists(fname) else fname.replace("/tmp", "")

    pdb_lines = []
    with open(filen, 'r+') as file:
        for line in file:
            if 'ATOM' in line or 'HETATM' in line:
                line = line.strip()
                if 'DUM' not in line:
                    pdb_lines.append(line)

    return pdb_lines


def get_coos_from_pdb(pdb_dat):
    atoms = []
    coos = []
    for line in pdb_dat:
        atom = line.split()[2]
        x, y, z = line[28:56].split()
        atoms.append(atom)
        coos.append([float(x), float(y), float(z)])
    return (atoms, coos)


def pairing_func(a, b):
    ans = (a + b) * (a + b + 1) * 0.5
    if a > b:
        ans = ans + a
        pans = '%6d%6d' % (b, a)
    else:
        ans = ans + b
        pans = '%6d%6d' % (a, b)
    return (int(ans), pans)


def ucomb(vec, blist):
    res = 0
    for a in vec:
        vec.remove(a)
        for b in vec:
            ans = (a + b) * (a + b + 1) * 0.5
            if (ans + a in blist) or (ans + b in blist):
                res = res + 1
    return res


def tor_cent(vec, blist):
    db = {}
    for a in vec:
        na = 0
        for b in vec:
            ans = (a + b) * (a + b + 1) * 0.5
            if (ans + a in blist) or (ans + b in blist):
                na += 1
        db[a] = na
    new_vec = list(sorted(db, key=db.__getitem__, reverse=True))
    return (new_vec)


def bossPdbAtom2Element(attype):
    elem = ''.join([i for i in attype[:-1] if not i.isdigit()])
    return elem


def bossElement2Mass(elem):
    symb2mass = {
        'H': 1.008,
        'F': 18.998403163,
        'Cl': 35.45,
        'Br': 79.904,
        'I': 126.90447,
        'O': 15.999,
        'S': 32.06,
        'N': 14.007,
        'P': 30.973761998,
        'C': 12.011,
        'Si': 28.085,
        'Na': 22.98976928,
        'SOD': 22.98976928,
        'K': 39.0983,
        'Mg': 24.305,
        'Ca': 40.078,
        'Mn': 54.938044,
        'Fe': 55.845,
        'Co': 58.933194,
        'Ni': 58.6934,
        'Cu': 63.546,
        'Zn': 65.38, }
    try:
        res = symb2mass[elem]
    except NameError:
        print("Mass for atom %s is not available \n add it to symb2mass dictionary")
    return res


def refine_file_lines(fname):
    lines = []
    with open(fname, 'r+') as file:
        for line in file:
            line = line.strip()
            if line:
                lines.append(line)
    return lines


class BOSSReader(object):

    def __init__(self, zmatrix, optim, charge=0, lbcc=False):
        self.zmat = zmatrix
        self.impDat = {}
        self.MolData = {}
        self.refine_data(optim, charge, lbcc)

    
    def Get_OPT(self, optim, charge):
        current_path = os.getcwd()
        assert os.path.isfile(self.zmat), f'File named {self.zmat} does not exist'
        
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
        
        #print('MOLECULE HAS A CHARGE of %d' % charge)
        if optim > 0:
            print(f'Optimization level requested: {optim}')
            for opt_lev in range(optim):
                print(f'Performing Stage {opt_lev + 1} of Charge Generation')
                execfile = execs[charge]
                coma = f'{execfile} {self.zmat[:-2]}'
                subprocess.run(coma, shell=True)
                subprocess.run(f'cp sum {self.zmat}', shell=True)

                execfile_opt = execs['OPT']
                coma_opt = f'{execfile_opt} {self.zmat[:-2]}'
                subprocess.run(coma_opt, shell=True)
                subprocess.run(f'cp sum {self.zmat}', shell=True)
                subprocess.run(f'head -1 {self.zmat}', shell=True)
        
        execfile_spm = f'{boss_dir}/scripts/xSPM > {current_path}/olog'
        coma_spm = f'{execfile_spm} {self.zmat[:-2]}'
        subprocess.run(coma_spm, shell=True)
        subprocess.run(f'cd {current_path}; /bin/cp sum {self.zmat}', shell=True)
        return None

    
    def get_addihed(self, data):
        add = []
        nadd = 0
        for line in data:
            if line[0].isdigit():
                add.append(line.split()[0:4])
                nadd = nadd + 1
        return (add)

    
    def get_atinfo(self, data):
        ats = []
        nat = 0
        for line in data:
            if line[0].isdigit() and float(line.split()[2]) > 1:
                ats.append(line)
                nat += 1
        return (ats)

    
    def get_charge(self, data):
        TotQ = {}
        for line in data[1:]:
            words = line.split()
            TotQ['-'.join(words[:-1])] = round(float(words[-1]), 3)
        return TotQ

    
    def get_tors(self, data):
        tors = []
        ntor = 0
        for line in data:
            if 'All Solutes' in line:
                tors.append(line.split()[4:8])
                for tor in line.split()[4:8]:
                    if abs(float(tor)) > 0.0:
                        ntor = ntor + 1
        return (tors)

    
    def get_QLJ(self, data):
        qlj = []
        nqlj = 0
        for line in data:
            if 'All Solutes' in line and line[0].isalpha():
                qlj.append([line.split()[0], line.split()[2],
                            line.split()[3], line.split()[4]])
                nqlj += 1
        return (qlj)

    
    def get_angs(self, data):
        angs = {'cl1': [], 'cl2': [], 'cl3': [], 'R': [], 'K': []}
        nang = 0
        for line in data:
            if line[0].isdigit() and float(line.split()[4]) > 0:
                word = line.split()
                angs['cl1'].append(int(word[0]))
                angs['cl2'].append(int(word[1]))
                angs['cl3'].append(int(word[2]))
                angs['R'].append(float(word[3]))
                angs['K'].append(float(word[4]))
                nang = nang + 1
            #        print 'Total No of Non-zero Angles in BOSS is %d' % (nang)
        return (angs)

    
    def get_XYZ(self, data):
        XYZ = {'at_num': [], 'X': [], 'Y': [], 'Z': [], 'at_symb': []}
        for line in data:
            if line[0].isdigit() and len(line.split()) == 5:
                word = line.split()
                if int(word[0]) > 0:
                    XYZ['at_num'].append(int(word[0]))
                    XYZ['X'].append(float(word[1]))
                    XYZ['Y'].append(float(word[2]))
                    XYZ['Z'].append(float(word[3]))
                    XYZ['at_symb'].append(word[4])
        XYZ = pd.DataFrame(XYZ)
        return XYZ

    
    def get_pairs(self, data):
        data = data[1:]
        plnos = []
        for i in range(0, len(data)):
            if 'Atom' in data[i]:
                plnos.append(i)
        plnos.append(len(data))
        pair_dat = {i: ' '.join(data[plnos[i]:plnos[i + 1]])
                    for i in range(len(plnos) - 1)}
        for nu in range(len(plnos) - 1):
            pair_dat[nu] = list(pair_dat[nu][10:].split())
            pair_dat[nu] = np.array([int(a) - 2 for a in pair_dat[nu]])
        pairs = []
        for k in pair_dat.keys():
            for j in pair_dat[k]:
                pairs.append('%6d%6d%6d\n' % (k - 1, j, 1))
        return pairs

    
    def get_bonds(self, data):
        bnds = {'cl1': [], 'cl2': [], 'RIJ': [], 'KIJ': [], 'TIJ': []}
        nbnd = 0
        for line in data:
            if line[0].isdigit() and float(line.split()[3]) > 0:
                word = line.split()
                bnds['cl1'].append(int(word[0]))
                bnds['cl2'].append(int(word[1]))
                bnds['RIJ'].append(float(word[2]))
                bnds['KIJ'].append(float(word[3]))
                bnds['TIJ'].append(line[-5:])
                nbnd += 1
        return (bnds)

    
    def prep_lbcc(self, bond_data, qdata):
        db = bcc_db()
        bnd_df = pd.DataFrame(bond_data)
        bnd_df = bnd_df[['cl1', 'cl2']]
        bnd_df.columns = ['I', 'J']
        q_df = pd.DataFrame(columns=['TY', 'Q'])
        q_df.loc[0] = ['1', 0.000]
        q_df.loc[1] = ['2', 0.000]
        for i in range(len(qdata)):
            q_df.loc[i + 2] = [qdata[i][0], float(qdata[i][1])]
        bond, cha, QBC1 = new_mol_info(db, q_df, bnd_df)
        lbcc_qdat = []
        for i in range(len(qdata)):
            lbcc_qdat.append(
                [qdata[i][0], str(cha.QBCC.values[i]), qdata[i][2], qdata[i][3]])
        bond.to_csv('LBCC_BONDS.csv', index=False)
        cha.to_csv('LBCC_CHARGES.csv', index=False)
        return np.array(cha.QBCC), lbcc_qdat

    
    def cleanup(self):
        current_path = os.getcwd() 
        os.system('cd '+current_path+';/bin/rm sum log olog out plt.pdb')

    
    def get_ImpDat(self, optim, charge):
        current_path = os.getcwd()
        self.Get_OPT(optim, charge)
        odat = refine_file_lines(current_path + '/out')
        sdat = refine_file_lines(current_path + '/sum')
        MolData = {}
        impDat = {}
        MolData['PDB'] = refine_file_lines(current_path + '/plt.pdb')
        for nl in range(len(odat)):
            if 'Z-Matrix for Reference Solutes' in odat[nl]:
                impDat['ATMinit'] = nl
            elif 'Net Charge' in odat[nl]:
                impDat['TotalQ'] = nl
            elif 'OPLS Force Field Parameters' in odat[nl]:
                impDat['ATMfinal'] = nl
                impDat['NBDinit'] = nl
            elif 'Fourier Coefficients' in odat[nl]:
                impDat['TORinit'] = nl
                impDat['NBDfinal'] = nl
            elif 'Bond Stretching Parameters' in odat[nl]:
                impDat['TORfinal'] = nl
                impDat['BNDinit'] = nl
            elif 'Angle Bending Parameters' in odat[nl]:
                impDat['BNDfinal'] = nl
                impDat['ANGinit'] = nl
            elif 'Non-bonded Pairs List' in odat[nl]:
                impDat['ANGfinal'] = nl
                impDat['PAIRinit'] = nl
            elif 'Solute 0:   X          Y          Z' in odat[nl]:
                impDat['XYZinit'] = nl
            elif 'Atom I      Atom J      RIJ' in odat[nl]:
                impDat['XYZfinal'] = nl
            elif 'Checking' in odat[nl]:
                impDat['PAIRfinal'] = nl
                
        #### THIS PART IS READ FROM SUM FILE ###
        for ml in range(len(sdat)):
            if 'Additional Dihedrals follow' in sdat[ml]:
                impDat['ADDinit'] = ml
            elif 'Domain Definitions follow' in sdat[ml]:
                impDat['ADDfinal'] = ml
                
        #### THIS PART IS READ FROM SUM FILE ###
        MolData['ATOMS'] = self.get_atinfo(
            odat[impDat['ATMinit']:impDat['ATMfinal']])
        MolData['Q_LJ'] = self.get_QLJ(
            odat[impDat['NBDinit']:impDat['NBDfinal']])
        MolData['BONDS'] = self.get_bonds(
            odat[impDat['BNDinit']:impDat['BNDfinal']])
        MolData['ANGLES'] = self.get_angs(
            odat[impDat['ANGinit']:impDat['ANGfinal']])
        MolData['TORSIONS'] = self.get_tors(
            odat[impDat['TORinit']:impDat['TORfinal']])
        MolData['ADD_DIHED'] = self.get_addihed(
            sdat[impDat['ADDinit']:impDat['ADDfinal']])
        MolData['XYZ'] = self.get_XYZ(
            odat[impDat['XYZinit']:impDat['XYZfinal']])
        MolData['PAIRS'] = self.get_pairs(
            odat[impDat['PAIRinit']:impDat['PAIRfinal']])
        MolData['TotalQ'] = self.get_charge(
            odat[impDat['TotalQ']:impDat['TotalQ'] + 4])
        return MolData

    
    def refine_data(self, optim, charge, lbcc):
        current_path = os.getcwd()
        if lbcc and (charge == 0):
            lbcc_MD = self.get_ImpDat(optim, charge)
            QLBCC, DATA_Q_LJ = self.prep_lbcc(
                lbcc_MD['BONDS'], lbcc_MD['Q_LJ'])
            lbcc_MD['Q_LJ'] = DATA_Q_LJ
            BCC_file2zmat(self.zmat, QLBCC,
                          oname=current_path + '/%s_BCC.z' % self.zmat[:-2])
            os.system('mv %s.z %s_NO_LBCC.z' %
                      (self.zmat[:-2], self.zmat[:-2]))
            os.system('mv %s_BCC.z %s.z' % (self.zmat[:-2], self.zmat[:-2]))
            self.MolData = lbcc_MD
        elif lbcc and (charge != 0):
            print('LBCC IS SUPPORTED ONLY FOR NEUTRAL MOLECULES')
        else:
            self.MolData = self.get_ImpDat(optim, charge)
        return None

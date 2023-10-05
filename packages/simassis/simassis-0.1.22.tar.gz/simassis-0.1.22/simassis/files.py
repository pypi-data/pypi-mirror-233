import numpy as np
import sys
import os
import shutil

from simassis.general import u_rotate, mases, angle, mases_to_symbols, charges, eV_per_Angstrom_2_Ha_per_Bohr, Angstrom_2_Bohr, ev2H, atom_symbols


def path_restart(fpath):
    if os.path.exists(fpath):
        shutil.rmtree(fpath, ignore_errors=True)
        os.makedirs(fpath)
    else:
        os.makedirs(fpath)

def list_of_files(fpath):
    return [f for f in os.listdir(fpath) if os.path.isfile(os.path.join(fpath, f))]

def list_of_directories(fpath):
    return list(set(os.listdir(fpath))-set(list_of_files(fpath)))

def subpaths_in_folder(path):
    paths = [x[0] for x in os.walk(path)]
    pas = []
    for p in range(len(paths)):
        g = True
        for pt in range(len(paths)):
            if p is not pt:
                if paths[p] in paths[pt]:
                    g = False
        if g:
            pas.append(paths[p]+'/')
    return pas

def list_of_out_directories(fpath):
    dire = list_of_directories(fpath)
    number = [int(n[30:]) for n in dire]
    idx = np.argsort(number)
    dire = np.array(dire)[idx]
    dire = dire.tolist()
    return dire

def _parsing_poscar(lines):
        name = lines[0][:-1]
        lattice_cons = float(lines[1])
        basex = np.array([float(l)*lattice_cons for l in lines[2].split()])
        basey = np.array([float(l)*lattice_cons for l in lines[3].split()])
        basez = np.array([float(l)*lattice_cons for l in lines[4].split()])
        atoms = [int(l) for l in lines[6].split()]
        atoms_tot = sum(atoms)
        header_tot = 8
        positions = lines[header_tot:]
        positions = [p[:-1] for p in positions[:atoms_tot]]
        
        positions = np.array([p.split() for p in positions], float)
        return name, basex, basey, basez, atoms_tot, positions
    
def _rotating_positions(basex, basey, basez, positions):
    #fixing x    
    if basex[1] != 0 or basex[2] != 0:
        rotation_vecotr = np.cross([1,0,0], basex)
        rotation_angle = angle([1,0,0], basex)
        rotation_matrix = u_rotate(rotation_angle, rotation_vecotr)
        basez = np.dot(basez, rotation_matrix)
        basey = np.dot(basey, rotation_matrix)
        basex = np.dot(basex, rotation_matrix)
        for i in range(len(positions)):
            positions[i, :] = np.dot(positions[i,:], rotation_matrix)
        
    #fixing y
    if basey[2] != 0:
        rotation_vecotr = [1,0,0]
        rotation_angle = -angle([0,1,0], [0, basey[1], basey[2]])
        rotation_matrix = u_rotate(rotation_angle, rotation_vecotr)
        basez = np.dot(basez, rotation_matrix)
        basey = np.dot(basey, rotation_matrix)
        basex = np.dot(basex, rotation_matrix)
        for i in range(len(positions)):
            positions[i, :] = np.dot(positions[i,:], rotation_matrix)

    return basex, basey, basez, positions

def _positive_vectors(basex, basey, basez, positions):
    if basex[0]<0:
        basex = basex*-1
        positions[:, 0] = positions[:, 0]*-1
    if basey[1]<0:
        basey = basey*-1
        positions[:, 1] = positions[:, 1]*-1
    if basez[2]<0:
        basez = basez*-1
        positions[:, 2] = positions[:, 2]*-1
    for i in range(3):
        if np.abs(basex[i])<.00001:
            basex[i] = 0
        if np.abs(basey[i])<.00001:
            basey[i] = 0
        if np.abs(basez[i])<.00001:
            basez[i] = 0
                
    return basex, basey, basez, positions

def poscar_to(file_in, args):
    file = open(file_in)
    lines = file.readlines()
    file.close()
    
    cart_dir = lines[7][:-1]

    name, basex, basey, basez, atoms_tot, positions = _parsing_poscar(lines) 
    atoms_type = list(filter(None,lines[5][:-1].split()))
    atoms_quantity = np.array(list(filter(None,lines[6][:-1].split())), int)
    atoms_variety = len(atoms_quantity)
    if 'Direct' in cart_dir:
        base = np.array([basex, basey, basez]).T
        positions = np.dot(base, positions.T).T

    positions_splited = []
    nl = 0
    for i in range(atoms_variety):
        positions_splited.append(positions[nl:nl+atoms_quantity[i]])
        nl = nl + atoms_quantity[i]
    return configuration(name, basex, basey, basez, cart_dir, atoms_type, atoms_quantity, atoms_variety, positions_splited)

def lammps_to(filein, args):
    file = open(filein)
    lines = file.readlines()
    file.close()
    
    if 'Masses' in lines[9]:
        shift = 0
    elif 'Masses' in lines[10]:
        shift = 1
    else:
        print('something wrong with position of first few lines')
        shift = 1000000

    name = lines[0]
    atoms_quantity_total = int(lines[2].split()[0])
    atoms_variety = int(lines[3].split()[0])
    atoms_type = lines[11+shift:11+shift+atoms_variety]
    atoms_type = [float(a.split()[1]) for a in atoms_type]
    atoms_type = [mases_to_symbols[a] for a in atoms_type]
    
    basis = lines[5:8+shift]
    basis = [b.split() for b in basis]

    xl = np.asanyarray(basis[0][:2],float)
    yl = np.asanyarray(basis[1][:2],float)
    zl = np.asanyarray(basis[2][:2],float)
    if shift == 0:
        xy = 0
        xz = 0
        yz = 0
    if shift == 1:
        xy = float(basis[3][0])
        xz = float(basis[3][1])
        yz = float(basis[3][2])
    
    basex = np.array([xl[1]-xl[0], 0, 0])
    basey = np.array([xy, yl[1]-yl[0], 0])
    basez = np.array([xz, yz, zl[1]-zl[0]])
    
    positions = lines[14+shift+atoms_variety:14+shift+atoms_variety+atoms_quantity_total]
    if 'charge' in args:
        positions = np.asanyarray([p.split()[:6] for p in positions])
    else:
        positions = np.asanyarray([p.split()[:5] for p in positions])
    pos_idx = positions[:,0].astype(int)-1
    pos_type = positions[:,1].astype(int)-1
    if 'charge' in args:
        positions = positions[:,3:].astype(float)
    else:
        positions = positions[:,2:].astype(float)
    pos_type = pos_type[pos_idx]
    positions = positions[pos_idx,:]
    
    positions_splited = []
    atoms_quantity = []
    for a in range(atoms_variety):
        positions_splited.append(positions[pos_type==a,:])
        atoms_quantity.append(np.sum(pos_type==a))
    return configuration(name, basex, basey, basez, 'Cartesian', atoms_type, atoms_quantity, atoms_variety, positions_splited)

def lammps_dump_to(filein, args):
    file = open(filein)
    lines = file.readlines()
    file.close()

    frame = args[0]
    steps = len([l for l in lines if 'ITEM: TIMESTEP' in l])
    step_len = len(lines)/steps
    if frame<0:
        frame = steps+frame
    frame_beg = int(frame*step_len + 9)
    frame_end = int((frame+1)*step_len)
        
    name = 'noname'
    atoms_quantity_total = int(lines[3].split()[0])

    basis = lines[5:8]
    basis = [b.split() for b in basis]

    xl = np.asanyarray(basis[0][:2],float)
    yl = np.asanyarray(basis[1][:2],float)
    zl = np.asanyarray(basis[2][:2],float)

    basex = np.array([xl[1]-xl[0], 0, 0])
    basey = np.array([0, yl[1]-yl[0], 0])
    basez = np.array([0, 0, zl[1]-zl[0]])

    data = lines[frame_beg:frame_end]
    data = np.array([d.split() for d in data], dtype=float)
    atom_types = np.array(data[:,0]-1, dtype=int)
    atom_masses = data[:,1]
    atom_masses_unique = []
    for a in atom_masses:
        if a not in atom_masses_unique:
            atom_masses_unique.append(a)
    atoms_variety = len(atom_masses_unique)
    atoms_type = [mases_to_symbols[a] for a in atom_masses_unique]

    positions = data[:,2:]
    positions_splited = []
    atoms_quantity = []
    for a in range(atoms_variety):
        positions_splited.append(positions[atom_types==a,:])
        atoms_quantity.append(np.sum(atom_types==a))
    return configuration(name, basex, basey, basez, 'Cartesian', atoms_type, atoms_quantity, atoms_variety, positions_splited)

def rmc_to(file_in, args):
    file = open(file_in)
    lines = file.readlines()
    file.close()
    
    name = lines[1].split(' RMC')[0][1:]

    atoms_type = []
    spec = ''
    for i in range(len(name)):
        temp = name[i:]
        new_atom = True
        for cut in range(len(temp)):
            if temp[:-cut] in atom_symbols and new_atom:
                atoms_type.append(temp[:-cut])
                new_atom = False

    idx = np.array([i for i in range(len(lines)) if 'Defining vectors are' in lines[i]])[-1]
    basis = lines[idx+1:idx+4]
    basis = np.array([b.split() for b in basis], dtype=float)
    basex = basis[:,0]*2
    basey = basis[:,1]*2
    basez = basis[:,2]*2
    cart_dir = 'Cartesian'

    atoms_quantity = np.array([l.split('molecules')[0] for l in lines if 'molecules of type ' in l], dtype=int)
    atoms_variety = len(atoms_type)

    idx = np.array([i for i in range(len(lines)) if 'molecules of type' in lines[i]])[-1]
    positions = lines[idx+4:]
    positions = np.array([p.split() for p in positions], dtype=float)
    positions = np.dot(basis, positions.T).T
    positions_splited = np.split(positions, np.cumsum(atoms_quantity))[:-1]
    return configuration(name, basex, basey, basez, cart_dir, atoms_type, atoms_quantity, atoms_variety, positions_splited)

def to_poscar(
        name,
        basex, basey, basez,
        cart_dir,
        atoms_type, atoms_quantity, atoms_variety,
        positions_splited,
        fileout,
        args,
        ):    
    poscar = [name[:-1]]
    poscar.append('\n')
    poscar.append('1.0\n')
    poscar.append('\t'+"{:15.10f}".format(basex[0])+'         '+"{:15.10f}".format(basex[1])+'         '+"{:15.10f}".format(basex[2]) + '\n')
    poscar.append('\t'+"{:15.10f}".format(basey[0])+'         '+"{:15.10f}".format(basey[1])+'         '+"{:15.10f}".format(basey[2]) + '\n')
    poscar.append('\t'+"{:15.10f}".format(basez[0])+'         '+"{:15.10f}".format(basez[1])+'         '+"{:15.10f}".format(basez[2]) + '\n')
    poscar.append(''.join(["{:>5}".format(at) for at in atoms_type]) + '\n')
    poscar.append(''.join(["{:>5}".format(aq) for aq in atoms_quantity]) + '\n')
    poscar.append(cart_dir+'\n')
    for positions in positions_splited:
        if len(positions.shape)>1:
            for p in positions:
                poscar.append("{:16.9f}".format(p[0]) +'    '+ "{:16.9f}".format(p[1]) +'    '+ "{:16.9f}".format(p[2]) + '\t' + '\n')
        else:
            poscar.append(str(positions[0]) + '\t' + str(positions[1]) + '\t' + str(positions[2]) + '\t' + '\n')
    poscar = "".join(poscar)
    
    file = open(fileout, 'w')
    file.write(poscar)
    file.close()
    
def to_lammps(
        name,
        basex, basey, basez,
        cart_dir,
        atoms_type, atoms_quantity, atoms_variety,
        positions_splited,
        fileout,
        args,
        ):

    #rotating bases and positions
    for i in range(len(positions_splited)):
        basex_, basey_, basez_, positions_splited[i] = _rotating_positions(
                basex, basey, basez,
                positions_splited[i],
                )
    basex, basey, basez = basex_, basey_, basez_
    
    for i in range(len(positions_splited)):
        basex_, basey_, basez_, positions_splited[i] = _positive_vectors(
                basex, basey, basez,
                positions_splited[i],)
    basex, basey, basez = basex_, basey_, basez_

    text = [name]
    text.append('\n')
    text.append(str(np.sum(atoms_quantity))+' atoms\n')
    text.append(str(atoms_variety)+' atom types\n')
    text.append('\n')
    text.append(
            str(0) + ' ' +
            str(basex[0]) + ' ' +
            'xlo xhi\n'
            )
    text.append(
            str(0) + ' ' +
            str(basey[1]) + ' ' +
            'ylo yhi\n'
            )
    text.append(
            str(0) + ' ' +
            str(basez[2]) + ' ' +
            'zlo zhi\n'
            )
    if 'triclinic' in args:
        text.append(
                str(basey[0]) + ' ' +
                str(basez[0]) + ' ' +
                str(basez[1]) + ' ' +
                'xy xz yz\n'
                )
    text.append('\n')
    text.append('Masses\n')
    text.append('\n')
    for a in range(len(atoms_type)):
        text.append(str(a+1) + ' ' + str(mases[atoms_type[a]]) + '\n')
    text.append('\n')
    text.append('Atoms\n')
    text.append('\n')

    if 'charge' in args:
        n = 1
        for at in range(len(atoms_type)):
            for a in positions_splited[at]:
                text.append(
                        '   ' +
                        str(n) + ' ' +
                        str(at+1) + ' ' +
                        str(charges[atoms_type[at]]) + ' ' +
                        str(a[0]) + ' ' + 
                        str(a[1]) + ' ' + 
                        str(a[2]) + ' ' + 
                        '\n'
                        )
                n += 1
    else:
        n = 1
        for at in range(len(atoms_type)):
            for a in positions_splited[at]:
                text.append(
                        '   ' +
                        str(n) + ' ' +
                        str(at+1) + ' ' +
                        str(a[0]) + ' ' + 
                        str(a[1]) + ' ' + 
                        str(a[2]) + ' ' + 
                        '\n'
                        )
                n += 1

    text = "".join(text)
    file = open(fileout, 'w')
    file.write(text)
    file.close()

class configuration:
    def __init__(
            self,
            name, 
            basex, basey, basez, 
            cart_dir, 
            atoms_type, atoms_quantity, atoms_variety,
            positions_splited,
            ):
        self.name = name
        self.basex = basex
        self.basey = basey
        self.basez = basez
        self.cart_dir = cart_dir
        self.atoms_type = atoms_type
        self.atoms_quantity = atoms_quantity
        self.atoms_variety = atoms_variety
        self.positions_splited = positions_splited

    def write(self, file_format, fileout, args=[]):
        if file_format=='vasp':
            to_poscar(
                        self.name,
                        self.basex, self.basey, self.basez,
                        self.cart_dir,
                        self.atoms_type, self.atoms_quantity, self.atoms_variety,
                        self.positions_splited,
                        fileout,
                        args,
                    )
        if file_format=='lammps':
            to_lammps(
                        self.name,
                        self.basex, self.basey, self.basez,
                        self.cart_dir,
                        self.atoms_type, self.atoms_quantity, self.atoms_variety,
                        self.positions_splited,
                        fileout,
                        args,
                    )
        if file_format=='lammps-dump':
            to_lammps_dump(
                        self.name,
                        self.basex, self.basey, self.basez,
                        self.cart_dir,
                        self.atoms_type, self.atoms_quantity, self.atoms_variety,
                        self.positions_splited,
                        fileout,
                        args,
                    )

def read_configuration(fname, file_format, args=[]):
    if file_format=='vasp':
        return poscar_to(fname, args)
    elif file_format=='lammps':
        return lammps_to(fname, args)
    elif file_format=='lammps-dump':
        return lammps_dump_to(fname, args)
    elif file_format=='rmc':
        return rmc_to(fname, args)
    else:
        print('wrong file format')
        return 0

def reading_elfacar_file(fname):
    file = open(fname)
    lines = file.readlines()
    file.close()

    basis = lines[2:5]
    basis = np.array([b.split() for b in basis], dtype=float)
    atoms = np.array(lines[6].split(), dtype=int)
    n_na = atoms[0]
    n_bi = atoms[1]
    n_o = atoms[3]
    n_all = np.sum(atoms)
    positions = lines[8:8+n_all]
    positions = np.array([p.split() for p in positions], dtype=float)
    positions_bi = positions[n_na:n_na+n_bi]
    positions_ox = positions[-n_o:]
    
    binning = np.array(lines[8+n_all+1].split(), dtype=int)
    n_lines = int(np.ceil(binning[0]*binning[1]*binning[2]/10))
    data = lines[8+n_all+2:]
    data = [d.split() for d in data]
    data = np.array([item for sublist in data for item in sublist], dtype=float)
    
    M = np.zeros((binning))
    czik = 0
    for z in range(binning[2]):
        for y in range(binning[1]):
            for x in range(binning[0]):
                M[x,y,z] = data[czik]
                czik = czik + 1
    return positions_bi, positions_ox, basis, M, binning, n_lines

def parsing_elfcar(position_bi, positions_ox, basis, M, binning, dcut):
    positions_bi_binning = np.floor(position_bi*binning)/binning
    positions_bi_shifted = np.mod(position_bi-positions_bi_binning+.5, 1)
    positions_ox_shifted = np.mod(positions_ox-positions_bi_binning+.5, 1)
    
    positions_ox_scaled = np.zeros_like(positions_ox_shifted)
    positions_ox_scaled[:,0] = positions_ox_shifted[:,0]*basis[0,0]
    positions_ox_scaled[:,1] = positions_ox_shifted[:,1]*basis[1,1]
    positions_ox_scaled[:,2] = positions_ox_shifted[:,2]*basis[2,2]
    
    positions_bi_scaled = np.zeros_like(positions_bi_shifted)
    positions_bi_scaled[0] = positions_bi_shifted[0]*basis[0,0]
    positions_bi_scaled[1] = positions_bi_shifted[1]*basis[1,1]
    positions_bi_scaled[2] = positions_bi_shifted[2]*basis[2,2]
    
    d = np.sum((positions_ox_scaled-positions_bi_scaled)**2, 1)**.5
    idx = d < 4
    positions_ox_shifted_near_bi = positions_ox_shifted[idx,:]
    
    #shifting volumetric data
    positions_bi_binning = np.array(positions_bi_binning*binning, dtype=int)
    dx = (int(binning[0]/2) - positions_bi_binning[0]) 
    dy = (int(binning[1]/2) - positions_bi_binning[1])
    dz = (int(binning[2]/2) - positions_bi_binning[2])
    
    if dx**2>0:
        new_M = np.zeros_like(M)
        new_M[dx:,:,:] = M[:-dx,:,:]
        new_M[:dx,:,:] = M[-dx:,:,:]
    
    if dy**2>0:
        M = new_M
        new_M = np.zeros_like(M)
        new_M[:,dy:,:] = M[:,:-dy,:]
        new_M[:,:dy,:] = M[:,-dy:,:]
    
    if dz**2>0:
        M = new_M
        new_M = np.zeros_like(M)
        new_M[:,:,dz:] = M[:,:,:-dz]
        new_M[:,:,:dz] = M[:,:,-dz:]

    position = []
    weight = []
    for z in range(binning[2]):
        for y in range(binning[1]):
            for x in range(binning[0]):
                r = (
                                (x - binning[0]/2)**2 + 
                                (y - binning[1]/2)**2 + 
                                (z - binning[2]/2)**2
                                )**.5
                if r > dcut:
                    new_M[x,y,z] = 0
                if r <= 2:
                    new_M[x,y,z] = new_M[x,y,z]*r/3
                position.append([x,y,z])
                weight.append(new_M[x,y,z])
    position = np.array(position)
    weight = np.array(weight)**20
    
    lp = np.sum(position.T*weight, 1)/np.sum(weight)
    lp = [
          lp[0]/binning[0],
          lp[1]/binning[1],
          lp[2]/binning[2],
          ]
    shifting_factor = (1/binning)/2
    positions_ox_shifted_near_bi = positions_ox_shifted_near_bi+shifting_factor
    positions_bi_shifted = positions_bi_shifted+shifting_factor
    return positions_ox_shifted_near_bi, positions_bi_shifted, new_M, lp

def read_charge(fpath):
    file = open(fpath)
    lines = file.readlines()
    file.close()
    
    brak = [i for i in range(len(lines)) if '---' in lines[i]]
    lines = lines[brak[0]+1:brak[1]]
    return np.array([l.split()[4] for l in lines], dtype=float)

def vasp_to_runner_data_train(finput):
    samples = list_of_directories(finput)
    text = ''
    for sample, nsample in zip(samples, range(len(samples))):
        try:
            #charges and positions   
            file = open(finput + sample + '/POTCAR')
            lines = file.readlines()
            file.close()
            energy = [lines[i+1] for i in np.arange(len(lines)) if '  PAW_PBE' in lines[i]]
            charges_default = np.array(energy, dtype=float)

            file = open(finput + sample + '/ACF.dat')
            lines = file.readlines()
            file.close()
            total_electrones = float(lines[-1].split()[-1])
            lines = lines[2:-4]
            positions = np.array([l.split()[1:4] for l in lines], dtype=float)*Angstrom_2_Bohr
            positions = np.array(positions, dtype='str')
            charges_ = np.array([l.split()[4] for l in lines], dtype=float)

            file = open(finput + sample + '/POSCAR')
            lines = file.readlines()
            atoms = lines[6].split()
            atoms_names = lines[5].split()
            file.close()
            atoms = [int(a) for a in atoms]
            charges_default_vec = []
            atoms_names_vec = []
            for a, cd, an in zip(atoms, charges_default, atoms_names):
                charges_default_vec = charges_default_vec + [cd]*a
                atoms_names_vec = atoms_names_vec + [an]*a
            charges_default_vec = np.array(charges_default_vec)
            charges = (-charges_+charges_default_vec).tolist()
            charges = [str(c) for c in charges]
            basis = lines[2:5]

            #forces
            file = open(finput + sample + '/OUTCAR')
            lines = file.readlines()[2:-4]
            file.close()
            energy = [l for l in lines if 'energy  without entropy' in l]
            energy = str(float(energy[-1].split('=')[1].split()[0])*ev2H)

            start = [i for i in range(len(lines)) if 'TOTAL-FORCE' in lines[i]]
            lines = lines[start[-1]+2:]
            stop = [i for i in range(len(lines)) if 'total drift:' in lines[i]]
            lines = lines[:stop[-1]-1]
            forces = np.array([l.split()[3:] for l in lines], dtype=float)
            forces = np.array(forces*eV_per_Angstrom_2_Ha_per_Bohr, dtype='str')

            text = text + 'begin\n'
            text = text + 'lattice         '+'   '.join((np.array(np.array(basis[0].split(), dtype=float)*Angstrom_2_Bohr, dtype=str)).tolist()) + '\n'
            text = text + 'lattice         '+'   '.join((np.array(np.array(basis[1].split(), dtype=float)*Angstrom_2_Bohr, dtype=str)).tolist()) + '\n'
            text = text + 'lattice         '+'   '.join((np.array(np.array(basis[2].split(), dtype=float)*Angstrom_2_Bohr, dtype=str)).tolist()) + '\n'
            lines = ''
            for i in range(len(atoms_names_vec)):
                line = [
                        'atom',
                        ("%.10f" % float(positions[i][0])),
                        ("%.10f" % float(positions[i][1])),
                        ("%.10f" % float(positions[i][2])),
                        atoms_names_vec[i],
                        ("%.10f" % float(charges[i])),
                        '0',
                        ("%.10f" % float(forces[i][0])),
                        ("%.10f" % float(forces[i][1])),
                        ("%.10f" % float(forces[i][2])),
                        ]
                lines = lines + ''.join(word.ljust(15) for word in line)+'\n'
            text = text + lines
            text = text + 'energy    ' + energy + '\n'
            text = text + 'charge    '+str(-np.sum(charges_default_vec)+total_electrones)+ '\n'
            text = text + 'end\n'
            print("\r" + str(int(100*(nsample+1)/len(samples))) + "%        ", end='')
        except:
            print('skipping entry!!! problem with data in folder '+sample)

    file = open(finput + '/input.data', 'w')
    file.writelines(text)
    file.close()

def fc(r, rm):
    f = np.zeros_like(r)
    for i in range(len(r)):
        if r[i]<rm:
            f[i] = 0.5*(np.cos(np.pi*r[i]/rm)+1)
        else:
            f[i] = 0
    return f

def g2(r, theta, f):
    return np.exp(-theta*r**2)*f

def r_05(r, rm, f):
    return r[np.argmin(np.abs(g2(r, rm, f) - .5))]

def theta(r, rm):
    return (r**-2)*np.log(np.cos(np.pi*r/rm)+1)

def acsf_creator(n_samples, rcut_factor, zeta_sampling, data_file):
    file = open(data_file)
    lines = file.readlines()
    file.close()

    head = lines[:1000]
    idx = [h for h in range(len(head)) if 'end' in head[h]]
    if len(idx)<1:
        print('head to small!!!!!!')
    step_l = idx[0]+1
    atoms_l = step_l - 7
    basis = head[1:4]
    basis = np.array([b.split()[1:] for b in basis], dtype=float).T
    basis_inv = np.linalg.inv(basis)
    step_1 = head[4:step_l-3]

    atom_labels = np.array([s.split()[4] for s in step_1])
    atom_types = np.unique(atom_labels)

    positions = np.array([s.split()[1:4] for s in step_1], dtype=float)
    positions_fractional = np.dot(basis_inv, positions.T).T

    positions_fractional_splited = []
    for a in atom_types:
        idx = np.where(atom_labels==a)[0]
        positions_fractional_splited.append(positions_fractional[idx,:])

    pairs = []
    rmins = []
    for at1 in range(len(atom_types)):
        for at2 in range(len(atom_types)):
            if at1>=at2:
                a1 = positions_fractional_splited[at1]
                a2 = positions_fractional_splited[at2]
                r = []
                for a in a1:
                    a2_ = np.mod(a2-a+.5, 1) - .5
                    a2_ = np.dot(basis, a2_.T).T
                    r_ = np.sum(a2_**2, 1)**.5
                    r.append(np.min(r_[r_>0]))
                rmins.append(np.min(r))
                pairs.append([atom_types[at1], atom_types[at2]])

    rmax = np.max(rmins)*rcut_factor
    symfunctions_text = []
    for pair, rmin in zip(pairs, rmins):
        r = np.linspace(0, rmax, 500)
        f = fc(r, rmax)

        r_05_max = r_05(r, 0, f)
        r_05_min = rmin
        r_05_step = (r_05_max - r_05_min)/(n_samples)

        theta_all = []
        for i in range(1, n_samples):
            theta_all.append(theta(r_05_min + r_05_step*i, rmax))
        theta_all.append(0)

        for t in theta_all:
            s = 'symfunction_short             '+pair[0]+' 2 '+pair[1]+'      '
            s = s + "{:9.8f}".format(t)
            s = s +'       0.00000000      '
            s = s + "{:9.7f}".format(rmax)
            symfunctions_text.append(s)
        if pair[0]!=pair[1]:
            for t in theta_all:
                s = 'symfunction_short             '+pair[1]+' 2 '+pair[0]+'      '
                s = s + "{:9.8f}".format(t)
                s = s +'       0.00000000      '
                s = s + "{:9.7f}".format(rmax)
                symfunctions_text.append(s)

    for at0 in range(len(atom_types)):
        for at1 in range(len(atom_types)):
            for at2 in range(len(atom_types)):
                if at1>=at2:
                    positions_shifted_0 = positions_fractional_splited[at0]
                    positions_shifted_1 = positions_fractional_splited[at1]
                    positions_shifted_2 = positions_fractional_splited[at2]
                    rall = []
                    for p in range(positions_shifted_0.shape[0]):
                        positions_shifted_1_ = np.mod(positions_shifted_1 - positions_shifted_0[p,:]+.5,1)-.5 
                        positions_shifted_1_ = np.dot(basis, positions_shifted_1_.T).T
                        positions_shifted_2_ = np.mod(positions_shifted_2 - positions_shifted_0[p,:]+.5,1)-.5 
                        positions_shifted_2_ = np.dot(basis, positions_shifted_2_.T).T

                        r01_ = np.sum(positions_shifted_1_**2, 1)**.5
                        r02_ = np.sum(positions_shifted_2_**2, 1)**.5
                        idx1 = np.where((r01_<rmax) * (r01_>0))[0]
                        idx2 = np.where((r02_<rmax) * (r02_>0))[0]
                        if len(idx1)>0 and len(idx2)>0:
                            positions_shifted_1_ = positions_shifted_1_[idx1,:]
                            positions_shifted_2_ = positions_shifted_2_[idx2,:]

                            r01_ = r01_[idx1]
                            r02_ = r02_[idx2]

                            x12 = np.subtract.outer(positions_shifted_1_[:,0], positions_shifted_2_[:,0])
                            y12 = np.subtract.outer(positions_shifted_1_[:,1], positions_shifted_2_[:,1])
                            z12 = np.subtract.outer(positions_shifted_1_[:,2], positions_shifted_2_[:,2])
                            r12_ = (x12**2 + y12**2 + z12**2)**.5
                            r01_02_sum = np.add.outer(r01_**2, r02_**2)
                            rall_ = (r01_02_sum + r12_**2)*(r01_02_sum>0)
                            rall_ = np.reshape(rall_, rall_.shape[0]*rall_.shape[1])
                            rall_ = rall_[rall_>0] 
                            rall.append(np.mean(rall_))
                    etha = np.log(2)/np.mean(rall)

                    for et in [etha, 0]:
                        for z in zeta_sampling:
                            s = 'symfunction_short             '+atom_types[at0]+' 3 '+atom_types[at1]+' '+atom_types[at2]+'      '
                            s = s + "{:9.8f}".format(et)
                            s = s +'      -1.00000000       '+"{:9.8f}".format(z)+'      '
                            s = s + "{:9.7f}".format(rmax)
                            symfunctions_text.append(s)
                            s = 'symfunction_short             '+atom_types[at0]+' 3 '+atom_types[at1]+' '+atom_types[at2]+'      '
                            s = s + "{:9.8f}".format(et)
                            s = s +'       1.00000000       '+"{:9.8f}".format(z)+'      '
                            s = s + "{:9.7f}".format(rmax)
                            symfunctions_text.append(s)
    return symfunctions_text

def _path_despiking(x, t, atom):
    nospike = np.abs(x[t+1, atom]-x[t-1, atom])/2
    if np.abs(x[t, atom]-x[t-1, atom])>2*nospike and np.abs(x[t, atom]-x[t+1, atom])>2*nospike:
        x[t, atom] = (x[t-1, atom] + x[t+1, atom])/2
    return x[t, atom]


def _path_continuing(x, t, atom):
    if x[t, atom]-x[t-1, atom]>.5:
        x[t:, atom] = x[t:, atom]-1
    if x[t, atom]-x[t-1, atom]<-.5:
        x[t:, atom] = x[t:, atom]+1
    return x[t, atom]

def xread(foldern, filen):
    file = open(foldern+filen)
    lines = file.readlines()
    file.close()    
    
    #header parsing and constants
    lattice = [float(i) for i in lines[1].split()][0]
    base_x = [float(i)*lattice for i in lines[2].split()]
    base_y = [float(i)*lattice for i in lines[3].split()]
    base_z = [float(i)*lattice for i in lines[4].split()]
    basis = np.zeros((3,3))
    basis[0,:] = base_x
    basis[1,:] = base_y
    basis[2,:] = base_z
    
    head = lines[:7]
    
    breaks = [i for i in range(len(lines)) if 'unknown system' in lines[i] ]
    idx = np.ones(len(lines))
    for b in breaks:
        idx[b:b+7] = 0
    idx = idx==1
    lines = np.array(lines)[idx]

    at_names = [i for i in head[5].split()]
    at_nums =  [float(i) for i in head[6].split()]
    at_nums = [int(x) for x in at_nums]
    at_nums_cum = np.cumsum([0] + at_nums)
    one_step = int(sum(at_nums)+1)
    total_steps = int((len(lines))/one_step)

    #initialising containers
    x = dict()
    y = dict()
    z = dict()
    for name, ion in zip(at_names, at_nums):
        x[name] = np.zeros((total_steps, ion))
        y[name] = np.zeros((total_steps, ion))
        z[name] = np.zeros((total_steps, ion))

    #puting data into containers
    for time in range(total_steps):
        step = []
        for at in range(np.sum(at_nums)):
            step.append([float(i) for i in lines[1+at+time*one_step].split()])
        step = np.array(step)
        for i in range(len(at_nums)):
            x[at_names[i]][time,:] = step[at_nums_cum[i]:at_nums_cum[i+1], 0]
            y[at_names[i]][time,:] = step[at_nums_cum[i]:at_nums_cum[i+1], 1]
            z[at_names[i]][time,:] = step[at_nums_cum[i]:at_nums_cum[i+1], 2]

#    path despiking
    for czik in range(2):
        for at_name, at_num in zip(at_names, at_nums):
            for at in range(at_num):
                for t in range(1, total_steps-1):
                    x[at_name][t, at] = _path_despiking(x[at_name], t, at)
                    y[at_name][t, at] = _path_despiking(y[at_name], t, at)
                    z[at_name][t, at] = _path_despiking(z[at_name], t, at)

#    continuing trajectories
    for at_name, at_num in zip(at_names, at_nums):
        for at in range(at_num):
            for t in range(1, total_steps):
                x[at_name][t, at] = _path_continuing(x[at_name], t, at)
                y[at_name][t, at] = _path_continuing(y[at_name], t, at)
                z[at_name][t, at] = _path_continuing(z[at_name], t, at)
            M = np.array([x[at_name][:,at], y[at_name][:,at], z[at_name][:,at]])
            M = np.dot(M.T, basis)
            x[at_name][:, at] = M[:,0]
            y[at_name][:, at] = M[:,1]
            z[at_name][:, at] = M[:,2]

    new_file = foldern + 'xdata' 
    np.savez(new_file,
             x=x, y=y, z=z,
             basis=basis,
             )
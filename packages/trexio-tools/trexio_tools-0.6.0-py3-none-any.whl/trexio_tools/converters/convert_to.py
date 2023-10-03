#!/usr/bin/env python3
"""
convert output of GAMESS/GAU$$IAN to trexio
"""

import sys
import os
from functools import reduce
from . import cart_sphe as cart_sphe
import numpy as np

try:
    import trexio
except:
    print("Error: The TREXIO Python library is not installed")
    sys.exit(1)





def run_molden(t, filename):

    out = ["[Molden Format]"]
    out += ["Converted from TREXIO"]

    out += ["[Atoms] AU"]

    nucl_num = trexio.read_nucleus_num(t)
    charge = trexio.read_nucleus_charge(t)
    if trexio.has_ecp_z_core(t):
       z_core = trexio.read_ecp_z_core(t)
       charge = [ x + y for x,y in zip(charge,z_core) ]
    name   = trexio.read_nucleus_label(t)
    coord  = trexio.read_nucleus_coord(t)
    for i in range(nucl_num):
        out += [ "%3s %4d %4d %18.14f %18.14f %18.14f"%tuple(
                 [name[i], i+1, int(charge[i])] + list(coord[i])  ) ]



    basis_type = trexio.read_basis_type(t)
    if basis_type.lower() == "gaussian":

        out += ["[GTO]"]
        prim_num = trexio.read_basis_prim_num(t)
        shell_num = trexio.read_basis_shell_num(t)
        nucleus_index = trexio.read_basis_nucleus_index(t)
        shell_ang_mom = trexio.read_basis_shell_ang_mom(t)
        shell_factor = trexio.read_basis_shell_factor(t)
        shell_index = trexio.read_basis_shell_index(t)
        exponent = trexio.read_basis_exponent(t)
        coefficient = trexio.read_basis_coefficient(t)
        prim_factor = trexio.read_basis_prim_factor(t)

        contr = [ { "exponent"      : [],
                    "coefficient"   : [],
                    "prim_factor"   : []  }  for _ in range(shell_num) ]
        for j in range(prim_num):
            i = shell_index[j]
            contr[i]["exponent"]    += [ exponent[j] ]
            contr[i]["coefficient"] += [ coefficient[j] ]
            contr[i]["prim_factor"] += [ prim_factor[j] ]

        basis = {}
        for k in range(nucl_num):
            basis[k] = { "shell_ang_mom" : [],
                        "shell_factor"  : [],
                        "shell_index"   : [],
                        "contr"         : [] }

        for i in range(shell_num):
            k = nucleus_index[i]
            basis[k]["shell_ang_mom"] += [ shell_ang_mom[i] ]
            basis[k]["shell_factor"]  += [ shell_factor[i] ]
            basis[k]["shell_index"]   += [ shell_index[i] ]
            basis[k]["contr"]         += [ contr[i] ]


        ang_mom_conv = [ "s", "p", "d", "f", "g" ]
        for k in range(nucl_num):
          out += [ "%6d  0"%(k+1) ]
          for l in range(len(basis[k]["shell_index"])):
              ncontr = len(basis[k]["contr"][l]["exponent"])
              out += [ "%2s %8d 1.00" % (
                        ang_mom_conv[ basis[k]["shell_ang_mom"][l] ],
                        ncontr) ]
              for j in range(ncontr):
                out += [ "%20.10E    %20.10E"%(
                          basis[k]["contr"][l]["exponent"][j],
                          basis[k]["contr"][l]["coefficient"][j] ) ]
          out += [""]

    # end if basis_type.lower() == "gaussian"



#   5D: D 0, D+1, D-1, D+2, D-2
#   6D: xx, yy, zz, xy, xz, yz
#
#   7F: F 0, F+1, F-1, F+2, F-2, F+3, F-3
#  10F: xxx, yyy, zzz, xyy, xxy, xxz, xzz, yzz, yyz, xyz
#
#   9G: G 0, G+1, G-1, G+2, G-2, G+3, G-3, G+4, G-4
#  15G: xxxx yyyy zzzz xxxy xxxz yyyx yyyz zzzx zzzy,
#       xxyy xxzz yyzz xxyz yyxz zzxy

    mo_num = trexio.read_mo_num(t)
    cartesian = trexio.read_ao_cartesian(t)
    if cartesian:
      order = [ [0],
                [0, 1, 2],
                [0, 3, 5, 2, 3, 4],
                [0, 6, 9, 3, 1, 2, 5, 8, 7, 4],
                [0, 10, 14, 1, 2, 6, 11, 9, 13, 3, 5, 12, 4, 7, 8] ]
    else:
       out += [ "[5D]", "[7F]", "[9G]" ]
       order = [ [0], [1, 2, 0],
                 [ i for i in range(5) ],
                 [ i for i in range(7) ],
                 [ i for i in range(9) ] ]

    ao_num = trexio.read_ao_num(t)
    o = []
    icount = 0
    for i in range(shell_num):
       l = shell_ang_mom[i]
       for k in order[l]:
          o.append( icount+k )
       icount += len(order[l])


    elec_alpha_num = trexio.read_electron_up_num(t)
    elec_beta_num  = trexio.read_electron_dn_num(t)
    if trexio.has_mo_occupation(t):
       occ = trexio.read_mo_occupation(t)
    else:
       occ = [ 0. for i in range(mo_num) ]
       for i in range(elec_alpha_num):
         occ[i] += 1.
       for i in range(elec_beta_num):
         occ[i] += 1.

    mo_coef = trexio.read_mo_coefficient(t)
    if trexio.has_mo_symmetry(t):
      sym = trexio.read_mo_symmetry(t)
    else:
      sym = [ "A1" for _ in range(mo_num) ]


    out += ["[MO]"]

    for i in range(mo_num):
       out += [ "Sym= %s"%(sym[i]),
#               "Ene= 0.0",
                "Spin= Alpha",
                "Occup= %f"%(occ[i]) ]
       for k in range(ao_num):
           out += [ "%6d  %20.10E"%(k+1, mo_coef[i,o[k]]) ]

    if trexio.has_ecp_z_core(t):
       out += [ "[CORE]" ]
       for i,k in enumerate(z_core):
           out += [ "%4d : %4d"%(i, k) ]

    out += [ "" ]
    out_file = open(filename,"w")
    out_file.write("\n".join(out))

    return




def run_cart_phe(inp, filename, to_cartesian):
    out = trexio.File(filename, 'u', inp.back_end)

    shell_ang_mom = trexio.read_basis_shell_ang_mom(inp)

    # Build transformation matrix
    count_sphe = 0
    count_cart = 0
    accu = []
    shell = []
    for i, l in enumerate(shell_ang_mom):
      p, r = count_cart, count_sphe
      (x,y) = cart_sphe.data[l].shape
      count_cart += x
      count_sphe += y
      q, s = count_cart, count_sphe
      accu.append( (l, p,q, r,s) )
      if to_cartesian != 0: n = x
      else: n = y
      for _ in range(n):
          shell.append(i)

    cart_normalization = np.ones(count_cart)
    R = np.zeros( (count_cart, count_sphe) )
    for (l, p,q, r,s) in accu:
      R[p:q,r:s] = cart_sphe.data[l]
      cart_normalization[p:q] = cart_sphe.normalization[l]

    S = np.eye(count_sphe)

    ao_num_in  = trexio.read_ao_num(inp)


    if to_cartesian == 0:
        print("Transformation from cartesian to spherical is not implemented")
        return

#        # See http://users.df.uba.ar/dmitnik/estructura3/bases/biblio/transformationGaussianSpherical.pdf
#        # If S is the overlap of cartesian functions, R @ S @ R.T = I, so R^{-1} = S @ R.T
#        if trexio.has_ao_1e_int_overlap(inp):
#            X = trexio.read_ao_1e_int_overlap(inp)
#        else:
#            print("Transformation from Cartesian to Spherical requires AO overlap matrix.")
#            return -1
#
#        S = np.zeros((count_cart, count_cart))
#        for (l, p,q, r,s) in accu:
#            S[p:q,p:q] = X[p:q,p:q]
#
#        R = R.T @ S

    elif to_cartesian == -1:
        R = np.eye(ao_num_in)

    # Update AOs
    ao_num_out = R.shape[0]
    trexio.write_ao_cartesian(out, to_cartesian)
    trexio.write_ao_num(out, ao_num_out)
    trexio.write_ao_shell(out, shell)

    normalization = np.array( [ 1. ] * ao_num_in )
    if trexio.has_ao_normalization(inp):
      normalization = trexio.read_ao_normalization(inp)

    trexio.write_ao_normalization(out, cart_normalization)

    R_norm_inv = np.array(R)

    # Update MOs
    if trexio.has_mo_coefficient(inp):
      X = trexio.read_mo_coefficient(inp)
      for i in range(R.shape[1]):
         if normalization[i] != 1.:
            X[:,i] *= normalization[i]
      Y  = X @ R.T
      trexio.write_mo_coefficient(out, Y)

    # Update 1e Integrals
    if trexio.has_ao_1e_int_overlap(inp):
      X = trexio.read_ao_1e_int_overlap(inp)
      for i in range(R.shape[1]):
            X[:,i] /= normalization[i]
      for i in range(R.shape[1]):
            X[i,:] /= normalization[i]
      Y = R_norm_inv @ X @ R_norm_inv.T
      trexio.write_ao_1e_int_overlap(out, Y)


    if trexio.has_ao_1e_int_kinetic(inp):
      X = trexio.read_ao_1e_int_kinetic(inp)
      for i in range(R.shape[1]):
         if normalization[i] != 1.:
            X[:,i] /= normalization[i]
            X[i,:] /= normalization[i]
      trexio.write_ao_1e_int_kinetic(out, R_norm_inv @ X @ R_norm_inv.T)

    if trexio.has_ao_1e_int_potential_n_e(inp):
      X = trexio.read_ao_1e_int_potential_n_e(inp)
      for i in range(R.shape[1]):
         if normalization[i] != 1.:
            X[:,i] /= normalization[i]
            X[i,:] /= normalization[i]
      trexio.write_ao_1e_int_potential_n_e(out, R_norm_inv @ X @ R_norm_inv.T)

    if trexio.has_ao_1e_int_ecp(inp):
      X = trexio.read_ao_1e_int_ecp(inp)
      for i in range(R.shape[1]):
         if normalization[i] != 1.:
            X[:,i] /= normalization[i]
            X[i,:] /= normalization[i]
      trexio.write_ao_1e_int_ecp(out, R_norm_inv @ X @ R_norm_inv.T)

    if trexio.has_ao_1e_int_core_hamiltonian(inp):
      X = trexio.read_ao_1e_int_core_hamiltonian(inp)
      for i in range(R.shape[1]):
         if normalization[i] != 1.:
            X[:,i] /= normalization[i]
            X[i,:] /= normalization[i]
      trexio.write_ao_1e_int_core_hamiltonian(out, R_norm_inv @ X @ R_norm_inv.T)

    # Remove 2e integrals: too expensive to transform
    if trexio.has_ao_2e_int_eri(inp):
      print("Warning: Two-electron integrals are not converted")
      trexio.delete_ao_2e_int_eri(out)

    if trexio.has_ao_2e_int_eri_lr(inp):
      trexio.delete_ao_2e_int_eri_lr(out)


def run_normalized_aos(t, filename):
    # Start by copying the file
    os.system('cp -r %s %s' % (t.filename, filename))
    run_cart_phe(t, filename, to_cartesian=-1)
    return


def run_cartesian(t, filename):
    # Start by copying the file
    os.system('cp -r %s %s' % (t.filename, filename))
    cartesian = trexio.read_ao_cartesian(t)
    if cartesian > 0:
        return

    run_cart_phe(t, filename, to_cartesian=1)
    return

def run_spherical(t, filename):
    # Start by copying the file
    os.system('cp -r %s %s' % (t.filename, filename))
    cartesian = trexio.read_ao_cartesian(t)
    if cartesian == 0:
        return

    run_cart_phe(t, filename, to_cartesian=0)
    return


def run(trexio_filename, filename, filetype):

    trexio_file = trexio.File(trexio_filename,mode='r',back_end=trexio.TREXIO_AUTO)

    if filetype.lower() == "molden":
        run_molden(trexio_file, filename)
    elif filetype.lower() == "cartesian":
        run_cartesian(trexio_file, filename)
    elif filetype.lower() == "spherical":
        run_spherical(trexio_file, filename)
#    elif filetype.lower() == "normalized_aos":
#        run_normalized_aos(trexio_file, filename)
#    elif filetype.lower() == "fcidump":
#        run_fcidump(trexio_file, filename)
    else:
        raise NotImplementedError(f"Conversion from TREXIO to {filetype} is not supported.")


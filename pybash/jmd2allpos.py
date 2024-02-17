#!/usr/bin/env python

#built with python 3

# Jacob Clary 1/2023
# to add:

#script to serve as a python shell to keep same file structure

import os, sys
import numpy as np
import argparse

def find_key(key_input, tempfile):
    #finds line where key occurs in stored input, last instance
    key_input = str(key_input)
    line = len(tempfile)                  #default to end
    for i in range(0,len(tempfile)):
        if key_input in tempfile[i]:
            line = i
    return line

def find_next_key(key_input, tempfile, startline):
    #finds first line where key occurs in stored input starting from startline
    key_input = str(key_input)
    line = len(tempfile)                  #default to end
    for i in range(startline,len(tempfile)):
        if key_input in tempfile[i]:
            line = i
            break
    return line

def find_all_key(key_input, tempfile):
    #finds all lines where key occurs in in lines
    L = []     #default
    key_input = str(key_input)
    for i in range(0,len(tempfile)):
        if key_input in tempfile[i]:
            L.append(i)
    if not L:
        L = [len(tempfile)]
    return L

def readfile(filename):
    #read a file into a list of strings
    f = open(filename,'r')
    tempfile = f.readlines()
    f.close()
    return tempfile

def writefile(filename,tempfile):
    #write tempfile (list of strings) to filename
    f = open(filename,'w')
    f.writelines(tempfile)
    f.close()

def check_file_mild(filename):
    #check if file exists but only return flag, doesn't die
    if not os.path.isfile(filename):
        print('\'' + filename + '\' file doesn\'t exist!')
        return False
    return True

def dir2cart_mat(coords,latt):
    #convert fractional coordinates to direct relative to lattice matrix (different than above)
    #    numbers may be different but still correct
    #    lattice needs to be list of lists
    coords_new = np.matmul(coords,latt)
    return coords_new

def latt_decompose(latt):
    #convert lattice to 6 components (needs to be list of lists)
    a = (latt[0][0]**2 + latt[0][1]**2 + latt[0][2]**2)**0.5
    b = (latt[1][0]**2 + latt[1][1]**2 + latt[1][2]**2)**0.5
    c = (latt[2][0]**2 + latt[2][1]**2 + latt[2][2]**2)**0.5
    alpha = np.arccos((latt[1][0]*latt[2][0] + latt[1][1]*latt[2][1] + latt[1][2]*latt[2][2])/b/c)
    beta = np.arccos((latt[0][0]*latt[2][0] + latt[0][1]*latt[2][1] + latt[0][2]*latt[2][2])/a/c)
    gamma = np.arccos((latt[1][0]*latt[0][0] + latt[1][1]*latt[0][1] + latt[1][2]*latt[0][2])/a/b)
    return a,b,c,alpha,beta,gamma

def getitercoords(step,out,Nions,lines):
    line = lines[step]
    line = find_next_key('Ionic positions in cartesian',out,startline=line)+1

    coords = out[line:line+Nions]
    coords = [x.split()[2:5] for x in coords]
    coords = [[float(y) for y in x] for x in coords]
    return coords

def parse_args():
    #get arguments from command line
    parser = argparse.ArgumentParser(description="Script to convert JDFTx MD out file into POSCARs containing all of the structures")
    parser.add_argument('-f', default='out',type=str,help='name of JDFTx aiMD out file to read')
    parser.add_argument('-o', default='allposcars',type=str, help='named of directory to store POSCARs in')
    args = parser.parse_args()
    return args

def main():

    #store arguments
    args = parse_args()
    outfilename = args.f
    outdir = args.o + '/'
 
#     if not os.path.isdir(outdir):
#         # os.makedirs(outdir)
#     else:
#         print('{:} directory already exists! Will overwrite files there!'.format(outdir))
 
    #read files
    if check_file_mild(outfilename):
        out = readfile(outfilename)
    else:
        print('out file missing! Quitting...')
        sys.exit()

    lines = find_all_key('IonicDynamics:',out)
    if not lines:
        print('IonicDyanmics: not found in out file! Did you actually do an aiMD run???')
    Nsteps = len(lines) 
   
    #get Nions
    line = find_key(' atoms',out)
    Nions = int(out[line].split()[4])
    #print(Nions)
    line = find_key('forces-output-coords',out)
    #print(line)
    line = find_next_key('ion ',out,startline=line) #there could be tags in between forces tag and ion lines
    #print(line)
    coords = out[line:line+Nions]
    coords = [x.split() for x in coords]
    #print(coords)
    elements = [x[1] for x in coords]
    #print(elements)
    coords = np.array([x[2:5] for x in coords])
    #print(coords)
    #ele = ['C','F','H','O','Pt','S']
    ele = []
    for e in elements:
        if not e in ele:
            ele.append(e)
    elenums = [elements.count(x) for x in ele] 
    elestr = [' '.join(ele)+'\n',' '.join([str(x) for x in elenums])+'\n']

    #make poscar files
    #first lattice, will be used of no R = lines present in out file
    line = find_next_key('R =', out, startline=0)+1
    ang2bohr = 1.88973
    latt = out[line:line+3]
    latt = [x.split()[1:4] for x in latt]
    latt = [[float(y) for y in x] for x in latt]
    latt = np.array(latt).T/ang2bohr
    lattstr = [' '.join(['{:19.15f}'.format(y) for y in x])+'\n' for x in latt]

    for i in range(Nsteps):
        if (i+1)%10 == 0:
            print('Update: working on step {:}'.format(i+1))

        mdstep = int(out[lines[i]].split()[2])
        poscar = ['comment\n','1.0\n']
        
        lattline = find_next_key('R =', out, startline=lines[i])
        if lattline != len(out):
            lattline += 1
            latt = out[lattline:lattline+3]
            latt = [x.split()[1:4] for x in latt]
            latt = [[float(y) for y in x] for x in latt]
            latt = np.array(latt).T/ang2bohr
            lattstr = [' '.join(['{:19.15f}'.format(y) for y in x])+'\n' for x in latt]
        else:
            print('No lattice found for step {:}!'.format(mdstep))
        poscar.extend(lattstr)
        poscar.extend(elestr)
        poscar.append('Direct\n')
        print(Nions)
        print(lines)
        coords = getitercoords(i,out,Nions,lines)
        #print(coords)
        coordstr = [' '.join(['{:19.15f}'.format(y) for y in x])+'\n' for x in coords]
        poscar.extend(coordstr)
 
        # writefile(outdir + 'POSCAR_'+str(mdstep),poscar)
        writefile(outfilename[:-9]+'.vasp',poscar)
        # break  # HACK
        if i ==1: break  # HACK
      
    
if __name__ == '__main__':
    main()



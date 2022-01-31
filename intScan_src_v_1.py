#! /Library/Frameworks/Python.framework/Versions/3.9/bin/python3

import platform
import math

osVer = platform.system()
proVer = '1.0'
rlsDate = '2022-01-30'

# Program information section
print("*******************************************************************************")
print("*                                                                             *")
print("*                               i n t . S c a n                               *")
print("*                                                                             *")
#print(f"*     =================== Version {proVer} for Source Code ===================     *")

if osVer == 'Darwin':
	print(f"*     ====================== Version {proVer} for macOS ======================     *")
elif osVer == 'Windows':
	print(f"*     ================ Version {proVer} for Microsoft Windows ================     *")
else:
	print(f"*     ====================== Version {proVer} for Linux ======================     *")

print(f"*                          Release date: {rlsDate}                           *")
print("*                                                                             *")
print("*                             -- Catch me with --                             *")
print("*                         E-mail  wongzit@yahoo.co.jp                         *")
print("*                       Homepage  https://wongzit.github.io                   *")
print("*                                                                             *")
print("*******************************************************************************")
print("\nPRESS Ctrl+c to exit the program.\n")

print("int.Scan input file (.txt):")
if osVer == 'Windows':
	fileName = input("(e.g.: C:\\intScan\\examples\\10cpp_c60.txt)\n")
	if fileName.strip()[0] == '\'' and fileName.strip()[-1] == '\'':
		fileName = fileName.strip()[1:-1]
	elif fileName.strip()[0] == '\"' and fileName.strip()[-1] == '\"':
		fileName = fileName.strip()[1:-1]
	else:
		fileName = fileName.strip()
else:
	fileName = input("(e.g.: /intScan/examples/10cpp_c60.txt)\n")
	if fileName.strip()[0] == '\"' and fileName.strip()[-1] == '\"':
		fileName = fileName.strip()[1:-1]
	elif fileName.strip()[0] == '\'' and fileName.strip()[-1] == '\'':
		fileName = fileName.strip()[1:-1]
	else:
		fileName = fileName.strip()

slashN = 0
for a in range(len(fileName)):
	if fileName[a] == '/' or fileName[a] == '\\':
		slashN = a

fileName2 = fileName[slashN+1:]

with open(f'{fileName[:-4]}_inp.txt', 'r') as routeFile:
	routeLine = routeFile.readlines()

bsseFlag = 0

with open(fileName, 'r') as usrInpFile:
	dimerCoor = usrInpFile.readlines()

atmNoMol1 = 1
atmNoMol2 = 1
movAtm1 = 1
movAtm2 = 1
stepNo = 10
stepSize = 0.1

coor0 = []

for i in range(len(dimerCoor)):
	if i == 0:
		atmNoMol1 = int(dimerCoor[i].strip().split()[0])
		atmNoMol2 = int(dimerCoor[i].strip().split()[1])
		movAtm1 = int(dimerCoor[i].strip().split()[2])
		movAtm2 = int(dimerCoor[i].strip().split()[3])
		stepNo = int(dimerCoor[i].strip().split()[4])
		stepSize = float(dimerCoor[i].strip().split()[5])
	elif dimerCoor[i] != '\n':
		coor0.append([dimerCoor[i].strip().split()[0], float(dimerCoor[i].strip().split()[1]), float(dimerCoor[i].strip().split()[2]), float(dimerCoor[i].strip().split()[3])])

vec = [coor0[movAtm2-1][1]-coor0[movAtm1-1][1], coor0[movAtm2-1][2]-coor0[movAtm1-1][2], coor0[movAtm2-1][3]-coor0[movAtm1-1][3]]

vecLen = math.sqrt(vec[0]*vec[0]+vec[1]*vec[1]+vec[2]*vec[2])
vecUnit = [vec[0]/vecLen, vec[1]/vecLen, vec[2]/vecLen]

molCoor1 = coor0[:atmNoMol1]
molCoor2 = coor0[atmNoMol1:]

xyzFile = open(f'{fileName[:-4]}.xyz', 'w')

for j in range(1, stepNo+1):
	xyzFile.write(f'{str(atmNoMol1+atmNoMol2)}\n')
	xyzFile.write(f'# Step {j}\n')
	gjfFile = open(f'{fileName[:-4]}_step_{j}.gjf', 'w')
	for n in routeLine:
		if n[0] == '%':
			if n != '%chk=\n':
				gjfFile.write(n)
			else:
				gjfFile.write(f'%chk={fileName2[:-4]}_step_{j}.chk\n')
		elif n[0] == '#':
			if 'counter' in n:
				bsseFlag = 1
			gjfFile.write(n)
		elif n != '\n':
			gjfFile.write(f'\n{fileName[:-4]}_step_{j}.gjf\n\n{n}')
	for k in molCoor1:
#		if k[0] != 'Bq':
		xyzFile.write(f'{k[0]}                 {round(float(k[1]),8):f}    {round(float(k[2]),8):f}    {round(float(k[3]),8):f}\n')
		if bsseFlag == 1 and k[0] != 'Bq':
			gjfFile.write(f'{k[0]}(Fragment=1)                 {round(float(k[1]),8):f}    {round(float(k[2]),8):f}    {round(float(k[3]),8):f}\n')
		elif k[0] != 'Bq':
			gjfFile.write(f'{k[0]}                 {round(float(k[1]),8):f}    {round(float(k[2]),8):f}    {round(float(k[3]),8):f}\n')
	for l in molCoor2:
#		if l[0] != 'Bq':
		xyzFile.write(f'{l[0]}                 {round(float(l[1]+j*stepSize*vecUnit[0]),8):f}    {round(float(l[2]+j*stepSize*vecUnit[1]),8):f}    {round(float(l[3]+j*stepSize*vecUnit[2]),8):f}\n')
		if bsseFlag == 1 and l[0] != 'Bq':
			gjfFile.write(f'{l[0]}(Fragment=2)                 {round(float(l[1]+j*stepSize*vecUnit[0]),8):f}    {round(float(l[2]+j*stepSize*vecUnit[1]),8):f}    {round(float(l[3]+j*stepSize*vecUnit[2]),8):f}\n')
		elif l[0] != 'Bq':
			gjfFile.write(f'{l[0]}                 {round(float(l[1]+j*stepSize*vecUnit[0]),8):f}    {round(float(l[2]+j*stepSize*vecUnit[1]),8):f}    {round(float(l[3]+j*stepSize*vecUnit[2]),8):f}\n')
	gjfFile.write('\n\n')
	gjfFile.close()

xyzFile.close()

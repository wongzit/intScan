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
print("*                              Energy  Extractor                              *")
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

print("int.Scan output file (.log):")
if osVer == 'Windows':
	fileName = input("(e.g.: C:\\intScan\\examples\\benzene_dimer.txt)\n")
	if fileName.strip()[0] == '\'' and fileName.strip()[-1] == '\'':
		fileName = fileName.strip()[1:-1]
	elif fileName.strip()[0] == '\"' and fileName.strip()[-1] == '\"':
		fileName = fileName.strip()[1:-1]
	else:
		fileName = fileName.strip()
else:
	fileName = input("(e.g.: /intScan/examples/benzene_dimer.txt)\n")
	if fileName.strip()[0] == '\"' and fileName.strip()[-1] == '\"':
		fileName = fileName.strip()[1:-1]
	elif fileName.strip()[0] == '\'' and fileName.strip()[-1] == '\'':
		fileName = fileName.strip()[1:-1]
	else:
		fileName = fileName.strip()

unbrN = 0
for k in range(len(fileName)):
	if fileName[k] == '_':
		unbrN = k

fileName2 = fileName[:unbrN+1]

energyList = []
energyList2 = []
fileNameList = []

for l in range(1, 99999):
	currentName = fileName2 + str(l) + '.log'
	try:
		with open(currentName, 'r') as outpUt:
			fileNameList.append(currentName)
	except FileNotFoundError:
		break

for m in fileNameList:
	with open(m, 'r') as outPut:
		outLine = outPut.readlines()

	for i in outLine:
		if 'Counterpoise corrected energy =' in i:
			energyList.append(float(i.split()[4]))

	for l in outLine:
		if 'SCF Done' in l:
			energyList2.append(float(l.split()[4]))
			break

outFile = open(f'{fileName2}energy.txt', 'w')
if len(energyList) != 0:
	outFile.write('                            Created by int.Scan\n\n')
	outFile.write('   No.      Corrected Energy (Hartree)      Sum Energy of Fragments (Hartree)\n')
	outFile.write('-------------------------------------------------------------------------------\n')
	for o in range(len(energyList)):
		outFile.write(f'    {o+1}          {energyList[o]}                     {energyList2[o]}\n')
else:
	outFile.write('            Created by int.Scan\n\n')
	outFile.write('   No.      Sum Energy of Fragments (Hartree)\n')
	outFile.write('-----------------------------------------------\n')
	for p in range(len(energyList2)):
		outFile.write(f'    {p+1}                     {energyList2[p]}\n')

outFile.close()

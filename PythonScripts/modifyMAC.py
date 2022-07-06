#!/usr/bin/python

import os,sys,time,math,datetime,pickle,itertools,fnmatch
from array import array

inputDir = '/home/ilhan/Geant_Helical/'
laserTarget = 'Solid_Target'
inputDir += laserTarget+'/'
if not os.path.exists('./'+laserTarget): os.system('mkdir '+laserTarget)
rootFiles = []
for root, dirs, files in os.walk(inputDir, topdown=False):
   for name in files:
      rootFiles.append(os.path.join(root, name))
rootFiles = [item for item in rootFiles if item.endswith('.root')]

EkRanges = ['1100-1150','1500-1550']#,'0-3000']

tarBox = -1. #cm
Nslice = -1
beamPos = 0 #cm, w.r.t. vacuum/target interface
printMod = 100
beamOn = 1000
braggPeakPos = 15 #mm, 
configDir = './'+laserTarget+'/tbox'+str(tarBox).replace('.','p').replace('p0','')+'cm'
if tarBox==-1: configDir = './'+laserTarget+'/tboxVard'
configDir+= '_bp'+str(beamPos).replace('.','p').replace('p0','')+'cm'
configDir+= '_bOn'+'k'.join(str(beamOn).rsplit('000', 1))
if not os.path.exists(configDir): os.system('mkdir '+configDir)
for rfile in rootFiles:
	laserInt = rfile.split('/')[-2]
	EkRange = rfile.split('Ek')[-1].replace('.root','')
	if EkRange not in EkRanges: continue
# 	if 'carbon_5e23_CP' not in rfile: continue
	outDirStr = 'i'+laserInt+'_p11_Ek'+EkRange
	if not os.path.exists(configDir+'/'+outDirStr): os.system('mkdir '+configDir+'/'+outDirStr)
	macfileR = open('/home/ssagir/Simulation/BraggPeak/CarbonPIC_build/carbon.mac','r')
	macfileW = open(configDir+'/'+outDirStr+'/carbon.mac','w')
	print 'Doing '+configDir+'/'+outDirStr+'/carbon.mac'
	translateX = 0.
	tarBox_ = tarBox
	Ekmax = float(EkRange.split('-')[-1])
# 	if Ekmax<=30: tarBox_, translateX = 1., 0.05
# 	elif Ekmax<=40: tarBox_, translateX = 2., 0.1
	if Ekmax<=1150: tarBox_, translateX = 3., 0.6
# 	elif Ekmax<=60: tarBox_, translateX = 4., 0.5
	elif Ekmax<=1550: tarBox_, translateX = 5., 1.1
	elif Ekmax<=2000: tarBox_, translateX = 5., 1.2
	elif Ekmax<=2150: tarBox_, translateX = 6., 1.6
# 	elif Ekmax<=90: tarBox_, translateX = 7., 1.6
# 	elif Ekmax<=100: tarBox_, translateX = 9., 2.5
# 	elif Ekmax<=120: tarBox_, translateX = 12., 3.5
# 	elif Ekmax<=150: tarBox_, translateX = 18., 5.8
# 	elif Ekmax<=205: tarBox_, translateX = 30., 11.
# 	elif Ekmax<=250: tarBox_, translateX = 40., 17.
# 	elif Ekmax<=300: tarBox_, translateX = 60., 20.
	if tarBox>0: tarBox_ = tarBox
	elif tarBox_<0: tarBox_ = 50.
	braggPeakPos = (tarBox_/2+translateX)*10
	Nslice_ = int(tarBox_/0.075) # for slice thinkness = 0.75mm
	if Nslice>0: Nslice_ = Nslice
	if Nslice_>150: Nslice_ = 150
	if EkRange=='0-3000':
		translateX = 0
		tarBox_, Nslice_ = 7., 100
	for line in macfileR:
		line = line.replace('/carbonPIC/det/setSizeX  4 cm','/carbonPIC/det/setSizeX  '+str(tarBox_)+' cm')
		#line = line.replace('/carbonPIC/det/setSizeYZ 4 cm','/carbonPIC/det/setSizeYZ '+str(tarBox_)+' cm')
		#line = line.replace('/carbonPIC/det/setSliceSizeYZ 4 cm','/carbonPIC/det/setSliceSizeYZ '+str(tarBox_)+' cm')
		line = line.replace('/carbonPIC/det/sliceNumber 50','/carbonPIC/det/sliceNumber '+str(Nslice_))
		#line = line.replace('/score/mesh/boxSize 2. 2. 2. cm','/score/mesh/boxSize '+str(tarBox_/2)+' '+str(tarBox_/2)+' '+str(tarBox_/2)+' cm')
		line = line.replace('/score/mesh/boxSize 2. 2. 2. cm','/score/mesh/boxSize '+str(tarBox_/2)+' 2. 2. cm')
		line = line.replace('/score/mesh/nBin 50 1 1','/score/mesh/nBin '+str(Nslice_)+' 1 1')
		#line = line.replace('/score/mesh/boxSize 0.1 2. 2. cm','/score/mesh/boxSize 0.1 '+str(tarBox_/2)+' '+str(tarBox_/2)+' cm')
		#line = line.replace('/score/mesh/nBin 1 1 50','/score/mesh/nBin 1 1 '+str(Nslice_))
		line = line.replace('/score/mesh/translate/xyz 1.2 0. 0. cm','/score/mesh/translate/xyz '+str(translateX)+' 0. 0. cm')
		#line = line.replace('/score/mesh/nBin 50 50 50','/score/mesh/nBin '+str(Nslice_)+' '+str(Nslice_)+' '+str(Nslice_))
		line = line.replace('/score/mesh/nBin 50 50 50','/score/mesh/nBin '+str(Nslice_)+' 50 50')
		line = line.replace('/carbonPIC/gun/input dummy.root','/carbonPIC/gun/input '+rfile)
		line = line.replace('/carbonPIC/gun/initPosX -2 cm','/carbonPIC/gun/initPosX '+str(beamPos-tarBox_/2)+' cm')
		line = line.replace('/carbonPIC/event/printModulo 50','/carbonPIC/event/printModulo '+str(printMod))
		line = line.replace('/analysis/h1/set 2 50 25 35 mm','/analysis/h1/set 2 100 '+str(braggPeakPos-5)+' '+str(braggPeakPos+5)+' cm')
		line = line.replace('/run/beamOn 5000','/run/beamOn '+str(beamOn))
		macfileW.write(line)
	macfileR.close()
	macfileW.close()


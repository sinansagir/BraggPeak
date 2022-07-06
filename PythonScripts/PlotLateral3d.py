#!/usr/bin/python

import os,sys,time,math,itertools,getopt
import ROOT as rt
import numpy as np
from array import array
rt.gROOT.SetBatch(1)
rt.gStyle.SetOptStat(0)

laserTarget = 'Solid_Target' # Plasma_Target veya Solid_Target
beamPos = 'bp-5cm' # bp0cm, bp-1p5cm, bp-5cm veya bp-10cm
laserInt = '5e23' # 5e21, 5e22, 1e23 veya 5e23
EkRange = '1100-1150'
EkRange = '1500-1550'
# EkRange = '1900-2000'
# EkRange = '0-3000'
nBeam = '1k'

try: 
	opts, args = getopt.getopt(sys.argv[1:], "", ["laserTarget=",
	                                              "beamPos=",
	                                              "laserInt=",
	                                              "EkRange=",
	                                              ])
	print opts,args
except getopt.GetoptError as err:
	print str(err)
	sys.exit(1)

for opt, arg in opts:
	print opt, arg
	if opt == '--laserTarget': laserTarget = arg
	elif opt == '--beamPos': beamPos = arg
	elif opt == '--laserInt': laserInt = arg
	elif opt == '--EkRange': EkRange = arg
	
doseFiles = [

laserTarget+'/tboxVard_'+beamPos+'_bOn'+nBeam+'/icarbon_'+laserInt+'_LP_p11_Ek'+EkRange,
laserTarget+'/tboxVard_'+beamPos+'_bOn'+nBeam+'/icarbon_'+laserInt+'_CP_p11_Ek'+EkRange,

]
textBox = '#splitline{#splitline{I = '+laserInt.split('e')[0]+'#times10^{'+laserInt.split('e')[1]+'}}{Beam @ x='+beamPos.replace('bp','').replace('p','.')+'}}{E_{^{12}C} = '+EkRange+' MeV}'
setLogyTotal = False
setLogyTotal2 = False
setLogyEntry = False
normalize = True
drawStr3d = "LEGO" #"BOX1,2,2Z,3", "ISO", "LEGO1,2,2Z,3"

W = 800
H = 600
# references for T, B, L, R
T = 0.10*H
B = 0.12*H
L = 0.12*W
R = 0.12*W
tagPosX = 0.75
tagPosY = 0.78

cTotal = {}
cEntry = {}
hTotal = {}
hTotal2 = {}
hEntry = {}
for dFile in doseFiles:
	saveStr='_'+laserInt+'_Ek'+EkRange+'_tboxVard_'+beamPos+'_bOn'+nBeam+'_'+dFile.split('/')[-1].split('_')[-3]
	try:
		with open(dFile+'/DoseLateralMesh3d.txt',"r") as f:
			thelines = f.readlines()
	except:
		print dFile+'/Proton.root does not exist! Skipping...'
		continue	
	xmax = -1.
	ymax = -1.
	zmax = -1.
	for theline in thelines:
		if theline.startswith('# '): continue
		depthx_ = int(theline.strip().split(',')[0])
		depthy_ = int(theline.strip().split(',')[1])
		depthz_ = int(theline.strip().split(',')[2])
		if depthx_>xmax: xmax = depthx_
		if depthy_>ymax: ymax = depthy_
		if depthz_>zmax: zmax = depthz_
	depthx = np.linspace(0,xmax,xmax+1)
	depthy = np.linspace(0,ymax,ymax+1)
	depthz = np.linspace(0,zmax,zmax+1)
	total  = np.zeros((len(depthx),len(depthy),len(depthz)))
	total2 = np.zeros((len(depthx),len(depthy),len(depthz)))
	entry  = np.zeros((len(depthx),len(depthy),len(depthz)))
	for theline in thelines:
		if theline.startswith('# '): continue
		depthx_ = int(theline.strip().split(',')[0])
		depthy_ = int(theline.strip().split(',')[1])
		depthz_ = int(theline.strip().split(',')[2])
		total_ = float(theline.strip().split(',')[3])
		total2_= float(theline.strip().split(',')[4])
		entry_ = int(theline.strip().split(',')[5])
		total[depthx_][depthy_][depthz_] = total_
		total2[depthx_][depthy_][depthz_] = total2_
		entry[depthx_][depthy_][depthz_] = entry_
	xbins=array('d', depthx*0.75) # *0.75 is valid if 0.75mm slicing option is used in carbon.mac!!
	ybins=array('d', depthy*0.8-depthy[-1]*0.8/2) # *0.8 is valid if 0.8mm(=40./50) slicing option is used in proton.mac!!
	zbins=array('d', depthz*0.8-depthz[-1]*0.8/2) # *0.8 is valid if 0.8mm(=40./50) slicing option is used in proton.mac!!

	BraggX = 0.
	Ekmax = float(dFile.split('Ek')[-1].split('-')[-1])
	if Ekmax<=1150: BraggX = 21.
	if Ekmax<=1550: BraggX = 36.
	elif Ekmax<=70: BraggX = 30. #?
	elif Ekmax<=80: BraggX = 46.
	elif Ekmax<=90: BraggX = 50.4
	elif Ekmax<=100: BraggX = 70.
	elif Ekmax<=120:
		xbins=array('d', depthx*(120./150)) # if 150 sliceNumber used in proton.mac!!
		BraggX = 95.
	elif Ekmax<=150:
		xbins=array('d', depthx*(180./150)) # if 150 sliceNumber used in proton.mac!!
		BraggX = 148.
	elif Ekmax<=205:
		xbins=array('d', depthx*(300./150)) # if 150 sliceNumber used in proton.mac!!
		BraggX = 260.
	elif Ekmax<=250:
		xbins=array('d', depthx*(400./150)) # if 150 sliceNumber used in proton.mac!!
		BraggX = 370.
	BraggXind = np.argmin(np.abs(np.array(xbins)-BraggX))
	print 'Bragg Peak Depth',xbins[BraggXind],'mm at index',BraggXind

	Nbinsx = len(xbins)
	Nbinsy = len(ybins)
	Nbinsz = len(zbins)
	hTotal[dFile+'xy'] = rt.TH2D("Total"+dFile+"xy","",Nbinsx-1,xbins,Nbinsy-1,ybins)
	hEntry[dFile+'xy'] = rt.TH2D("Entry"+dFile+"xy","",Nbinsx-1,xbins,Nbinsy-1,ybins)
	for ixbin in range(1,Nbinsx):
		for iybin in range(1,Nbinsy):
			hTotal[dFile+'xy'].SetBinContent(ixbin,iybin,total[ixbin-1][iybin-1][Nbinsz/2])
			hEntry[dFile+'xy'].SetBinContent(ixbin,iybin,entry[ixbin-1][iybin-1][Nbinsz/2])
	if normalize: hTotal[dFile+'xy'].Scale(100./(hTotal[dFile+'xy'].GetMaximum()+1e-30))
	hTotal[dFile+'xz'] = rt.TH2D("Total"+dFile+"xz","",Nbinsx-1,xbins,Nbinsz-1,zbins)
	hEntry[dFile+'xz'] = rt.TH2D("Entry"+dFile+"xz","",Nbinsx-1,xbins,Nbinsz-1,zbins)
	for ixbin in range(1,Nbinsx):
		for izbin in range(1,Nbinsz):
			hTotal[dFile+'xz'].SetBinContent(ixbin,izbin,total[ixbin-1][Nbinsy/2][izbin-1])
			hEntry[dFile+'xz'].SetBinContent(ixbin,izbin,entry[ixbin-1][Nbinsy/2][izbin-1])
	if normalize: hTotal[dFile+'xz'].Scale(100./(hTotal[dFile+'xz'].GetMaximum()+1e-30))
	hTotal[dFile+'yz'] = rt.TH2D("Total"+dFile+"yz","",Nbinsy-1,ybins,Nbinsz-1,zbins)
	hEntry[dFile+'yz'] = rt.TH2D("Entry"+dFile+"yz","",Nbinsy-1,ybins,Nbinsz-1,zbins)
	for iybin in range(1,Nbinsy):
		for izbin in range(1,Nbinsz):
			hTotal[dFile+'yz'].SetBinContent(iybin,izbin,total[BraggXind][iybin-1][izbin-1])
			hEntry[dFile+'yz'].SetBinContent(iybin,izbin,entry[BraggXind][iybin-1][izbin-1])
	if normalize: hTotal[dFile+'yz'].Scale(100./(hTotal[dFile+'yz'].GetMaximum()+1e-30))
	hTotal[dFile+'xyz'] = rt.TH3D("Total"+dFile+"xyz","",Nbinsx-1,xbins,Nbinsy-1,ybins,Nbinsz-1,zbins)
	hEntry[dFile+'xyz'] = rt.TH3D("Entry"+dFile+"xyz","",Nbinsx-1,xbins,Nbinsy-1,ybins,Nbinsz-1,zbins)
	for ixbin in range(1,Nbinsx):
		for iybin in range(1,Nbinsy):
			for izbin in range(1,Nbinsz):
				hTotal[dFile+'xyz'].SetBinContent(ixbin,iybin,izbin,total[ixbin-1][iybin-1][izbin-1])
				hEntry[dFile+'xyz'].SetBinContent(ixbin,iybin,izbin,entry[ixbin-1][iybin-1][izbin-1])
	
	chLatex = rt.TLatex()
	chLatex.SetNDC()
	chLatex.SetTextSize(0.04)
	chLatex.SetTextAlign(21) # align center

	for plane in ['xy','xz','yz']:
		cTotal[dFile+plane] = rt.TCanvas("cTotal"+dFile+plane,"",50,50,W,H)
		cTotal[dFile+plane].SetLeftMargin( L/W )
		cTotal[dFile+plane].SetRightMargin( R/W )
		cTotal[dFile+plane].SetTopMargin( T/H )
		cTotal[dFile+plane].SetBottomMargin( B/H )
		cTotal[dFile+plane].SetFillColor(0)
		cTotal[dFile+plane].SetBorderMode(0)
		cTotal[dFile+plane].SetFrameFillStyle(0)
		cTotal[dFile+plane].SetFrameBorderMode(0)
		if setLogyTotal: cTotal[dFile+plane].SetLogy()
		if plane.startswith('x'): hTotal[dFile+plane].GetXaxis().SetTitle("Depth [mm]")
		else: hTotal[dFile+plane].GetXaxis().SetTitle("Lateral-y [mm]")
		if plane.endswith('z'): hTotal[dFile+plane].GetYaxis().SetTitle("Lateral-z [mm]")
		else: hTotal[dFile+plane].GetYaxis().SetTitle("Lateral-y [mm]")
		if normalize: hTotal[dFile+plane].GetZaxis().SetTitle("Dose [%]")
		else: hTotal[dFile+plane].GetZaxis().SetTitle("Dose [Gy]")
		hTotal[dFile+plane].Draw("COLZ")
		chLatex.DrawLatex(tagPosX, tagPosY, textBox)
		chLatex.DrawLatex(tagPosX+0.05, tagPosY-0.1, dFile.split('/')[-1].split('_')[-3])
		cTotal[dFile+plane].SaveAs('plots_'+laserTarget+'/Dose'+plane.upper()+saveStr+'.pdf')
		cTotal[dFile+plane].SaveAs('plots_'+laserTarget+'/Dose'+plane.upper()+saveStr+'.png')

# 		cEntry[dFile+plane] = rt.TCanvas("cEntry"+dFile+plane,"",50,50,W,H)
# 		cEntry[dFile+plane].SetLeftMargin( L/W )
# 		cEntry[dFile+plane].SetRightMargin( R/W )
# 		cEntry[dFile+plane].SetTopMargin( T/H )
# 		cEntry[dFile+plane].SetBottomMargin( B/H )
# 		cEntry[dFile+plane].SetFillColor(0)
# 		cEntry[dFile+plane].SetBorderMode(0)
# 		cEntry[dFile+plane].SetFrameFillStyle(0)
# 		cEntry[dFile+plane].SetFrameBorderMode(0)
# 		if setLogyEntry: cEntry[dFile+plane].SetLogy()
# 		if plane.startswith('x'): hTotal[dFile+plane].GetXaxis().SetTitle("Depth [mm]")
# 		else: hTotal[dFile+plane].GetXaxis().SetTitle("Lateral-y [mm]")
# 		if plane.endswith('z'): hTotal[dFile+plane].GetYaxis().SetTitle("Lateral-z [mm]")
# 		else: hTotal[dFile+plane].GetYaxis().SetTitle("Lateral-y [mm]")
# 		hEntry[dFile+plane].GetZaxis().SetTitle("Entries")
# 		hEntry[dFile+plane].Draw("COLZ")
# 		chLatex.DrawLatex(tagPosX, tagPosY, textBox)
# 		cEntry[dFile+plane].SaveAs('plots_'+laserTarget+'/Entry'+plane.upper()+saveStr+'.pdf')
# 		cEntry[dFile+plane].SaveAs('plots_'+laserTarget+'/Entry'+plane.upper()+saveStr+'.png')
# 
# 	cTotal[dFile+'xyz'] = rt.TCanvas("cTotal"+dFile+'xyz',"",50,50,W,H)
# 	cTotal[dFile+'xyz'].SetLeftMargin( L/W )
# 	cTotal[dFile+'xyz'].SetRightMargin( R/W )
# 	cTotal[dFile+'xyz'].SetTopMargin( T/H )
# 	cTotal[dFile+'xyz'].SetBottomMargin( B/H )
# 	cTotal[dFile+'xyz'].SetFillColor(0)
# 	cTotal[dFile+'xyz'].SetBorderMode(0)
# 	cTotal[dFile+'xyz'].SetFrameFillStyle(0)
# 	cTotal[dFile+'xyz'].SetFrameBorderMode(0)
# 	if setLogyTotal: cTotal[dFile+'xyz'].SetLogy()
# 	hTotal[dFile+'xyz'].GetXaxis().SetTitle("Depth [mm]")
# 	hTotal[dFile+'xyz'].GetYaxis().SetTitle("Lateral-y [mm]")
# 	hTotal[dFile+'xyz'].GetZaxis().SetTitle("Lateral-z [mm]")
# 	hTotal[dFile+'xyz'].Draw(drawStr3d)
# 	chLatex.DrawLatex(tagPosX, tagPosY, textBox)
# 	cTotal[dFile+'xyz'].SaveAs('plots_'+laserTarget+'/Dose3d'+saveStr+'.pdf')
# 	cTotal[dFile+'xyz'].SaveAs('plots_'+laserTarget+'/Dose3d'+saveStr+'.png')
# 	#cTotal[dFile+'xyz'].SaveAs('plots/Dose3d'+saveStr+'.root')
# 
# 	cEntry[dFile+'xyz'] = rt.TCanvas("cEntry"+dFile+'xyz',"",50,50,W,H)
# 	cEntry[dFile+'xyz'].SetLeftMargin( L/W )
# 	cEntry[dFile+'xyz'].SetRightMargin( R/W )
# 	cEntry[dFile+'xyz'].SetTopMargin( T/H )
# 	cEntry[dFile+'xyz'].SetBottomMargin( B/H )
# 	cEntry[dFile+'xyz'].SetFillColor(0)
# 	cEntry[dFile+'xyz'].SetBorderMode(0)
# 	cEntry[dFile+'xyz'].SetFrameFillStyle(0)
# 	cEntry[dFile+'xyz'].SetFrameBorderMode(0)
# 	if setLogyEntry: cEntry[dFile+'xyz'].SetLogy()
# 	hEntry[dFile+'xyz'].GetXaxis().SetTitle("Depth [mm]")
# 	hEntry[dFile+'xyz'].GetYaxis().SetTitle("Lateral-y [mm]")
# 	hEntry[dFile+'xyz'].GetZaxis().SetTitle("Lateral-z [mm]")
# 	hEntry[dFile+'xyz'].Draw(drawStr3d)
# 	chLatex.DrawLatex(tagPosX, tagPosY, textBox)
# 	cEntry[dFile+'xyz'].SaveAs('plots_'+laserTarget+'/Entry3d'+saveStr+'.pdf')
# 	cEntry[dFile+'xyz'].SaveAs('plots_'+laserTarget+'/Entry3d'+saveStr+'.png')


#!/usr/bin/python

import os,sys,time,math,itertools,getopt
import ROOT as rt
import numpy as np
from array import array
rt.gROOT.SetBatch(1)
rt.gStyle.SetOptStat(0)

laserTarget = 'Plasma_Target' # Plasma_Target veya Solid_Target
beamPos = 'bp-1p5cm' # bp0cm, bp-1p5cm, bp-5cm veya bp-10cm
laserInt = '5e23' # 5e21, 5e22, 1e23 veya 5e23
EkRange = '145-150'

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

doseFiles = {

laserTarget+'/tboxVard_'+beamPos+'_bOn50k/i'+laserInt+'_m1_p11_Ek'+EkRange:[rt.kBlue,'HP m1'],
laserTarget+'/tboxVard_'+beamPos+'_bOn50k/i'+laserInt+'_m2_p11_Ek'+EkRange:[rt.kBlack,'HP m2'],
laserTarget+'/tboxVard_'+beamPos+'_bOn50k/i'+laserInt+'_m3_p11_Ek'+EkRange:[rt.kMagenta,'HP m3'],
laserTarget+'/tboxVard_'+beamPos+'_bOn50k/i'+laserInt+'_m4_p11_Ek'+EkRange:[rt.kCyan,'HP m4'],
laserTarget+'/tboxVard_'+beamPos+'_bOn50k/i'+laserInt+'_LP_p11_Ek'+EkRange:[rt.kRed,'LP'],
laserTarget+'/tboxVard_'+beamPos+'_bOn50k/i'+laserInt+'_CP_p11_Ek'+EkRange:[rt.kOrange,'CP'],

}
saveStr='_'+laserInt+'_Ek'+EkRange+'_tboxVard_'+beamPos+'_bOn50k'
xmin=0
xmax=50
textBox = '#splitline{#splitline{I = '+laserInt.split('e')[0]+'#times10^{'+laserInt.split('e')[1]+'}}{Beam @ x='+beamPos.replace('bp','').replace('p','.')+'}}{E_{p} = '+EkRange+' MeV}'
setLogyTotal = False
setLogyTotal2 = False
setLogyEntry = False

hTotal = {}
hTotalfrac = {}
hTotal2 = {}
hEntry = {}
for dFile in doseFiles.keys():
	try:
		with open(dFile+'/DoseLateralMesh.txt',"r") as f:
			thelines = f.readlines()
	except:
		print dFile+'/Proton.root does not exist! Skipping...'
		continue	
	xmax = -1.
	total = []
	total2 = []
	entry = []
	for theline in thelines:
		if theline.startswith('# '): continue
		depth_ = float(theline.strip().split(',')[2])
		total_ = float(theline.strip().split(',')[3])
		total2_ = float(theline.strip().split(',')[4])
		entry_ = int(theline.strip().split(',')[5])
		if depth_>xmax: xmax = depth_
		total.append(total_)
		total2.append(total2_)
		entry.append(entry_)
	depth = np.linspace(0,xmax,xmax+1)
	xbins=array('d', depth*0.8-depth[-1]*0.8/2) # *0.8 is valid if 0.8mm(=40./50) slicing option is used in proton.mac!!
	hTotal[dFile] = rt.TH1D("Total"+dFile,"",len(xbins)-1,xbins)
	hEntry[dFile] = rt.TH1D("Entry"+dFile,"",len(xbins)-1,xbins)
	for ibin in range(1,len(xbins)):
		hTotal[dFile].SetBinContent(ibin,total[ibin-1])
		hTotal[dFile].SetBinError(ibin,0)
		hEntry[dFile].SetBinContent(ibin,entry[ibin-1])
	
	hTotal[dFile].SetMarkerStyle(20)
	hTotal[dFile].SetMarkerSize(1.2)
	hTotal[dFile].SetMarkerColor(doseFiles[dFile][0])
	hTotal[dFile].SetLineWidth(2)
	hTotal[dFile].SetLineColor(doseFiles[dFile][0])
	hTotal[dFile].GetXaxis().SetTitle("Lateral-z [mm]")
	hTotal[dFile].GetYaxis().SetTitle("Dose [Gy]")

	hEntry[dFile].SetMarkerStyle(20)
	hEntry[dFile].SetMarkerSize(1.2)
	hEntry[dFile].SetMarkerColor(doseFiles[dFile][0])
	hEntry[dFile].SetLineWidth(2)
	hEntry[dFile].SetLineColor(doseFiles[dFile][0])
	hEntry[dFile].GetXaxis().SetTitle("Lateral-z [mm]")
	hEntry[dFile].GetYaxis().SetTitle("Entries")
	
W = 800
H = 600
# references for T, B, L, R
T = 0.10*H
B = 0.12*H
L = 0.12*W
R = 0.04*W
tagPosX = 0.85
tagPosY = 0.55
chLatex = rt.TLatex()
chLatex.SetNDC()
chLatex.SetTextSize(0.04)
chLatex.SetTextAlign(21) # align center

dFile0 = sorted(hTotal.keys())[0]
cTotal = rt.TCanvas("cTotal","",50,50,W,H)
cTotal.SetLeftMargin( L/W )
cTotal.SetRightMargin( R/W )
cTotal.SetTopMargin( T/H )
cTotal.SetBottomMargin( B/H )
cTotal.SetFillColor(0)
cTotal.SetBorderMode(0)
cTotal.SetFrameFillStyle(0)
cTotal.SetFrameBorderMode(0)
if setLogyTotal: cTotal.SetLogy()
hTotal[dFile0].Draw("LP")
hTotal[dFile0].SetMinimum(min([hTotal[hist].GetMinimum() for hist in hTotal.keys()])*0.9)
hTotal[dFile0].SetMaximum(max([hTotal[hist].GetMaximum() for hist in hTotal.keys()])*1.1)
#hTotal[dFile0].GetXaxis().SetRangeUser(xmin,xmax)
for dFile in sorted(hTotal.keys()):
	hTotal[dFile].Draw("sameLP")
legTotal = rt.TLegend(0.75,0.64,0.95,0.89)
legTotal.SetShadowColor(0)
legTotal.SetFillColor(0)
legTotal.SetFillStyle(0)
legTotal.SetLineColor(0)
legTotal.SetLineStyle(0)
legTotal.SetBorderSize(0) 
#legTotal.SetNColumns(2)
legTotal.SetTextFont(62)#42)
for dFile in sorted(hTotal.keys()):
	legTotal.AddEntry(hTotal[dFile],doseFiles[dFile][1],"l")
legTotal.Draw("same")
chLatex.DrawLatex(tagPosX, tagPosY, textBox)
cTotal.SaveAs('plots_'+laserTarget+'/TotalLateralZ'+saveStr+'.pdf')
cTotal.SaveAs('plots_'+laserTarget+'/TotalLateralZ'+saveStr+'.png')

cTotalfrac = rt.TCanvas("cTotalfrac","",50,50,W,H)
cTotalfrac.SetLeftMargin( L/W )
cTotalfrac.SetRightMargin( R/W )
cTotalfrac.SetTopMargin( T/H )
cTotalfrac.SetBottomMargin( B/H )
cTotalfrac.SetFillColor(0)
cTotalfrac.SetBorderMode(0)
cTotalfrac.SetFrameFillStyle(0)
cTotalfrac.SetFrameBorderMode(0)
if setLogyTotal: cTotalfrac.SetLogy()
for dFile in sorted(hTotal.keys()): 
	hTotalfrac[dFile] = hTotal[dFile].Clone(hTotal[dFile].GetName().replace('Total','Totalfrac'))
	hTotalfrac[dFile].Scale(100./(hTotalfrac[dFile].GetMaximum()+1e-30))
hTotalfrac[dFile0].Draw("LP")
hTotalfrac[dFile0].SetMinimum(min([hTotalfrac[hist].GetMinimum() for hist in hTotalfrac.keys()])*0.9)
hTotalfrac[dFile0].SetMaximum(max([hTotalfrac[hist].GetMaximum() for hist in hTotalfrac.keys()])*1.1)
#hTotal[dFile0].GetXaxis().SetRangeUser(xmin,xmax)
for dFile in sorted(hTotalfrac.keys()):
	hTotalfrac[dFile].Draw("sameLP")
legTotalfrac = rt.TLegend(0.75,0.64,0.95,0.89)
legTotalfrac.SetShadowColor(0)
legTotalfrac.SetFillColor(0)
legTotalfrac.SetFillStyle(0)
legTotalfrac.SetLineColor(0)
legTotalfrac.SetLineStyle(0)
legTotalfrac.SetBorderSize(0) 
#legTotal.SetNColumns(2)
legTotalfrac.SetTextFont(62)#42)
for dFile in sorted(hTotalfrac.keys()):
	legTotalfrac.AddEntry(hTotalfrac[dFile],doseFiles[dFile][1],"l")
legTotalfrac.Draw("same")
chLatex.DrawLatex(tagPosX, tagPosY, textBox)
cTotalfrac.SaveAs('plots_'+laserTarget+'/TotalLateralZfrac'+saveStr+'.pdf')
cTotalfrac.SaveAs('plots_'+laserTarget+'/TotalLateralZfrac'+saveStr+'.png')

# cEntry = rt.TCanvas("cEntry","",50,50,W,H)
# cEntry.SetLeftMargin( L/W )
# cEntry.SetRightMargin( R/W )
# cEntry.SetTopMargin( T/H )
# cEntry.SetBottomMargin( B/H )
# cEntry.SetFillColor(0)
# cEntry.SetBorderMode(0)
# cEntry.SetFrameFillStyle(0)
# cEntry.SetFrameBorderMode(0)
# if setLogyEntry: cEntry.SetLogy()
# hEntry[dFile0].Draw("LP")
# hEntry[dFile0].SetMaximum(max([hEntry[hist].GetMaximum() for hist in hEntry.keys()])*1.1)
# #hEntry[dFile0].GetXaxis().SetRangeUser(xmin,xmax);
# for dFile in sorted(doseFiles.keys()):
# 	hEntry[dFile].Draw("sameLP")
# legEntry = rt.TLegend(0.75,0.64,0.95,0.89)
# legEntry.SetShadowColor(0)
# legEntry.SetFillColor(0)
# legEntry.SetFillStyle(0)
# legEntry.SetLineColor(0)
# legEntry.SetLineStyle(0)
# legEntry.SetBorderSize(0) 
# #legEntry.SetNColumns(2)
# legEntry.SetTextFont(62)#42)
# for dFile in sorted(doseFiles.keys()):
# 	legEntry.AddEntry(hEntry[dFile],doseFiles[dFile][1],"l")
# legEntry.Draw("same")
# chLatex.DrawLatex(tagPosX, tagPosY, textBox)
# cEntry.SaveAs('plots_'+laserTarget+'/EntryLateralZ'+saveStr+'.pdf')
# cEntry.SaveAs('plots_'+laserTarget+'/EntryLateralZ'+saveStr+'.png')

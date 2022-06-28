#!/usr/bin/python

import os,sys,time,math,itertools,getopt
import ROOT as rt
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

# 'Solid_Target/tboxVard_bp-1p5cm_bOn50k/i5e23_LP_p11_Ek145-150':[rt.kRed,'LP Ek145-150'],
# 'Solid_Target/tboxVard_bp-1p5cm_bOn50k/i5e23_LP_p11_Ek200-205':[rt.kOrange,'LP Ek200-205'],
# 'Solid_Target/tboxVard_bp-1p5cm_bOn50k/i5e23_LP_p11_Ek245-250':[rt.kCyan,'LP Ek245-250'],

}
saveStr='_'+laserInt+'_Ek'+EkRange+'_tboxVard_'+beamPos+'_bOn50k'
xmin=0
xmax=400
if EkRange=='0-1000' and laserTarget=='Plasma_Target': xmax=100
textBox = '#splitline{#splitline{I = '+laserInt.split('e')[0]+'#times10^{'+laserInt.split('e')[1]+'}}{Beam @ x='+beamPos.replace('bp','').replace('p','.')+'}}{E_{p} = '+EkRange+' MeV}'
setLogyEdepMM = False
setLogyBragg = False
setLogyEdep = False
setLogyEdepfrac = False
setLogyDose = False
setLogyDosefrac = False
if EkRange=='0-1000':
	textBox = textBox.replace('E_{p} = 0-1000 MeV','')
	setLogyEdepMM = True
	setLogyBragg = True
	setLogyEdep = True
	setLogyEdepfrac = True
	setLogyDose = True
	setLogyDosefrac = True
EdepUnits = {#Scaling to MeV
'eV':1.e-6,
'keV':1.e-3,
'MeV':1.,
'GeV':1.e3,
'TeV':1.e6,
}

RFiles = {}
hEdepMM = {}
hBragg = {}
hEdep = {}
hEdepfrac = {}
hDose = {}
hDosefrac = {}
for dFile in doseFiles.keys():
	try: 
		RFiles[dFile] = rt.TFile(dFile+'/Proton.root')
		hEdepMM[dFile] = RFiles[dFile].Get('1').Clone(dFile)
		hBragg[dFile] = RFiles[dFile].Get('2').Clone(dFile)
	except:
		print dFile+'/Proton.root does not exist! Skipping...'
		continue

	with open(dFile+'/DoseFile.txt',"r") as f:
		thelines = f.readlines()
	depth = []
	Edep = []
	Edepfrac = []
	Dose = []
	Dosefrac = []
	for theline in thelines:
		if not theline.startswith(' layer '): continue
		depth_ = float(theline.strip().split()[2])
		if depth_>xmax: break
		Edep_ = float(theline.strip().split()[3])
		EdepUnit_ = theline.strip().split()[4]
		Edep_*=EdepUnits[EdepUnit_]
		Edepfrac_ = float(theline.strip().split()[5])
		if EdepUnit_ not in EdepUnits.keys(): print "WARNING! Edep unit "+EdepUnit_+" is not defined !!!!"
		Dose_ = float(theline.strip().split()[6])
		DoseUnit_ = theline.strip().split()[7]
		if DoseUnit_!='Gy': print "WARNING! Dose unit is not Gy !!!!"
		Dosefrac_ = float(theline.strip().split()[8])
		if math.isnan(Dosefrac_): Dosefrac_=0
		depth.append(depth_)
		Edep.append(Edep_)
		Edepfrac.append(Edepfrac_)
		Dose.append(Dose_)
		Dosefrac.append(Dosefrac_)
	xbins=array('d', [0]+depth)
	hEdep[dFile] = rt.TH1D("Edep"+dFile,"",len(xbins)-1,xbins)
	hEdepfrac[dFile] = rt.TH1D("Edep Fraction"+dFile,"",len(xbins)-1,xbins)
	hDose[dFile] = rt.TH1D("Dose"+dFile,"",len(xbins)-1,xbins)
	hDosefrac[dFile] = rt.TH1D("Dose Fraction"+dFile,"",len(xbins)-1,xbins)
	for ibin in range(1,len(xbins)):
		hEdep[dFile].SetBinContent(ibin,Edep[ibin-1])
		hEdepfrac[dFile].SetBinContent(ibin,Edepfrac[ibin-1])
		hDose[dFile].SetBinContent(ibin,Dose[ibin-1])
		hDosefrac[dFile].SetBinContent(ibin,Dose[ibin-1]*100/(max(Dose)+1e-20))
		#hDosefrac[dFile].SetBinContent(ibin,Dosefrac[ibin-1])
	
	hEdepMM[dFile].SetMarkerStyle(20)
	hEdepMM[dFile].SetMarkerSize(1.2)
	hEdepMM[dFile].SetMarkerColor(doseFiles[dFile][0])
	hEdepMM[dFile].SetLineWidth(2)
	hEdepMM[dFile].SetLineColor(doseFiles[dFile][0])
	hEdepMM[dFile].GetXaxis().SetTitle("Depth [mm]")
	hEdepMM[dFile].GetYaxis().SetTitle("E_{dep} [MeV/mm]")

	hBragg[dFile].SetMarkerStyle(20)
	hBragg[dFile].SetMarkerSize(1.2)
	hBragg[dFile].SetMarkerColor(doseFiles[dFile][0])
	hBragg[dFile].SetLineWidth(2)
	hBragg[dFile].SetLineColor(doseFiles[dFile][0])
	hBragg[dFile].GetXaxis().SetTitle("Depth [mm]")
	hBragg[dFile].GetYaxis().SetTitle("E_{dep} [MeV/mm]")

	hEdep[dFile].SetMarkerStyle(20)
	hEdep[dFile].SetMarkerSize(1.2)
	hEdep[dFile].SetMarkerColor(doseFiles[dFile][0])
	hEdep[dFile].SetLineWidth(2)
	hEdep[dFile].SetLineColor(doseFiles[dFile][0])
	hEdep[dFile].GetXaxis().SetTitle("Depth [mm]")
	hEdep[dFile].GetYaxis().SetTitle("E_{dep} [MeV]")

	hEdepfrac[dFile].SetMarkerStyle(20)
	hEdepfrac[dFile].SetMarkerSize(1.2)
	hEdepfrac[dFile].SetMarkerColor(doseFiles[dFile][0])
	hEdepfrac[dFile].SetLineWidth(2)
	hEdepfrac[dFile].SetLineColor(doseFiles[dFile][0])
	hEdepfrac[dFile].GetXaxis().SetTitle("Depth [mm]")
	hEdepfrac[dFile].GetYaxis().SetTitle("E_{dep}/E_{beam} [%]")

	hDose[dFile].SetMarkerStyle(20)
	hDose[dFile].SetMarkerSize(1.2)
	hDose[dFile].SetMarkerColor(doseFiles[dFile][0])
	hDose[dFile].SetLineWidth(2)
	hDose[dFile].SetLineColor(doseFiles[dFile][0])
	hDose[dFile].GetXaxis().SetTitle("Depth [mm]")
	hDose[dFile].GetYaxis().SetTitle("Dose [Gy]")

	hDosefrac[dFile].SetMarkerStyle(20)
	hDosefrac[dFile].SetMarkerSize(1.2)
	hDosefrac[dFile].SetMarkerColor(doseFiles[dFile][0])
	hDosefrac[dFile].SetLineWidth(2)
	hDosefrac[dFile].SetLineColor(doseFiles[dFile][0])
	hDosefrac[dFile].GetXaxis().SetTitle("Depth [mm]")
	hDosefrac[dFile].GetYaxis().SetTitle("Dose [%]")

W = 800
H = 600
# references for T, B, L, R
T = 0.10*H
B = 0.12*H
L = 0.12*W
R = 0.04*W
tagPosX = 0.85
tagPosY = 0.53
chLatex = rt.TLatex()
chLatex.SetNDC()
chLatex.SetTextSize(0.04)
chLatex.SetTextAlign(21) # align center

filePath0 = sorted(hEdepMM.keys())[0]
filePath0Ekmin = float(filePath0.split('Ek')[-1].split('-')[0])
for filePath in hEdepMM.keys():
	if filePath0Ekmin < float(filePath.split('Ek')[-1].split('-')[0]):
		filePath0 = filePath
		filePath0Ekmin = float(filePath.split('Ek')[-1].split('-')[0])
cEdepMM = rt.TCanvas("cEdepMM","",50,50,W,H)
cEdepMM.SetLeftMargin( L/W )
cEdepMM.SetRightMargin( R/W )
cEdepMM.SetTopMargin( T/H )
cEdepMM.SetBottomMargin( B/H )
cEdepMM.SetFillColor(0)
cEdepMM.SetBorderMode(0)
cEdepMM.SetFrameFillStyle(0)
cEdepMM.SetFrameBorderMode(0)
if setLogyEdepMM: cEdepMM.SetLogy()
cEdepMM.SetFillColor(0)
cEdepMM.SetBorderMode(0)
cEdepMM.SetFrameFillStyle(0)
cEdepMM.SetFrameBorderMode(0)
hEdepMM[filePath0].Draw("LP")
hEdepMM[filePath0].SetMaximum(max([hEdepMM[hist].GetMaximum() for hist in hEdepMM.keys()]))
if setLogyEdepMM: hEdepMM[filePath0].SetMinimum(1e-4)
hEdepMM[filePath0].GetXaxis().SetRangeUser(xmin,xmax)
for dFile in sorted(hEdepMM.keys()):
	hEdepMM[dFile].Draw("sameLP")
legEdepMM = rt.TLegend(0.75,0.64,0.95,0.89)
legEdepMM.SetShadowColor(0)
legEdepMM.SetFillColor(0)
legEdepMM.SetFillStyle(0)
legEdepMM.SetLineColor(0)
legEdepMM.SetLineStyle(0)
legEdepMM.SetBorderSize(0) 
#legEdepMM.SetNColumns(2)
legEdepMM.SetTextFont(62)#42)
for dFile in sorted(hEdepMM.keys()):
	legEdepMM.AddEntry(hEdepMM[dFile],doseFiles[dFile][1],"l")
legEdepMM.Draw("same")
chLatex.DrawLatex(tagPosX, tagPosY, textBox)
cEdepMM.SaveAs('plots_'+laserTarget+'/EdepMM'+saveStr+'.pdf')
cEdepMM.SaveAs('plots_'+laserTarget+'/EdepMM'+saveStr+'.png')

cBragg = rt.TCanvas("cBragg","",50,50,W,H)
cBragg.SetLeftMargin( L/W )
cBragg.SetRightMargin( R/W )
cBragg.SetTopMargin( T/H )
cBragg.SetBottomMargin( B/H )
cBragg.SetFillColor(0)
cBragg.SetBorderMode(0)
cBragg.SetFrameFillStyle(0)
cBragg.SetFrameBorderMode(0)
if setLogyBragg: cBragg.SetLogy()
cBragg.SetFillColor(0)
cBragg.SetBorderMode(0)
cBragg.SetFrameFillStyle(0)
cBragg.SetFrameBorderMode(0)
hBragg[filePath0].Draw("LP")
hBragg[filePath0].SetMaximum(max([hBragg[hist].GetMaximum() for hist in hBragg.keys()]))
if setLogyBragg: hBragg[filePath0].SetMinimum(0.001)
hBragg[filePath0].GetXaxis().SetRangeUser(10,20)
for dFile in sorted(hBragg.keys()):
	hBragg[dFile].Draw("sameLP")
legBragg = rt.TLegend(0.75,0.64,0.95,0.89)
legBragg.SetShadowColor(0)
legBragg.SetFillColor(0)
legBragg.SetFillStyle(0)
legBragg.SetLineColor(0)
legBragg.SetLineStyle(0)
legBragg.SetBorderSize(0) 
#legBragg.SetNColumns(2)
legBragg.SetTextFont(62)#42)
for dFile in sorted(hBragg.keys()):
	legBragg.AddEntry(hBragg[dFile],doseFiles[dFile][1],"l")
legBragg.Draw("same")
chLatex.DrawLatex(tagPosX, tagPosY, textBox)
cBragg.SaveAs('plots_'+laserTarget+'/Bragg'+saveStr+'.pdf')
cBragg.SaveAs('plots_'+laserTarget+'/Bragg'+saveStr+'.png')

cEdep = rt.TCanvas("cEdep","",50,50,W,H)
cEdep.SetLeftMargin( L/W )
cEdep.SetRightMargin( R/W )
cEdep.SetTopMargin( T/H )
cEdep.SetBottomMargin( B/H )
cEdep.SetFillColor(0)
cEdep.SetBorderMode(0)
cEdep.SetFrameFillStyle(0)
cEdep.SetFrameBorderMode(0)
if setLogyEdep: cEdep.SetLogy()
cEdep.SetFillColor(0)
cEdep.SetBorderMode(0)
cEdep.SetFrameFillStyle(0)
cEdep.SetFrameBorderMode(0)
hEdep[filePath0].Draw("LP")
hEdep[filePath0].SetMaximum(max([hEdep[hist].GetMaximum() for hist in hEdep.keys()]))
if setLogyEdep: hEdep[filePath0].SetMinimum(0.1)
hEdep[filePath0].GetXaxis().SetRangeUser(xmin,xmax);
for dFile in sorted(hEdep.keys()):
	hEdep[dFile].Draw("sameLP")
legEdep = rt.TLegend(0.75,0.64,0.95,0.89)
legEdep.SetShadowColor(0)
legEdep.SetFillColor(0)
legEdep.SetFillStyle(0)
legEdep.SetLineColor(0)
legEdep.SetLineStyle(0)
legEdep.SetBorderSize(0) 
#legEdep.SetNColumns(2)
legEdep.SetTextFont(62)#42)
for dFile in sorted(hEdep.keys()):
	legEdep.AddEntry(hEdep[dFile],doseFiles[dFile][1],"l")
legEdep.Draw("same")
chLatex.DrawLatex(tagPosX, tagPosY, textBox)
cEdep.SaveAs('plots_'+laserTarget+'/Edep'+saveStr+'.pdf')
cEdep.SaveAs('plots_'+laserTarget+'/Edep'+saveStr+'.png')

cEdepfrac = rt.TCanvas("cEdepfrac","",50,50,W,H)
cEdepfrac.SetLeftMargin( L/W )
cEdepfrac.SetRightMargin( R/W )
cEdepfrac.SetTopMargin( T/H )
cEdepfrac.SetBottomMargin( B/H )
cEdepfrac.SetFillColor(0)
cEdepfrac.SetBorderMode(0)
cEdepfrac.SetFrameFillStyle(0)
cEdepfrac.SetFrameBorderMode(0)
if setLogyEdepfrac: cEdepfrac.SetLogy()
cEdepfrac.SetFillColor(0)
cEdepfrac.SetBorderMode(0)
cEdepfrac.SetFrameFillStyle(0)
cEdepfrac.SetFrameBorderMode(0)
hEdepfrac[filePath0].Draw("LP")
hEdepfrac[filePath0].SetMaximum(max([hEdepfrac[hist].GetMaximum() for hist in hEdepfrac.keys()]))
if setLogyEdepfrac: hEdepfrac[filePath0].SetMinimum(0.001)
hEdepfrac[filePath0].GetXaxis().SetRangeUser(xmin,xmax)
for dFile in sorted(hEdepfrac.keys()):
	hEdepfrac[dFile].Draw("sameLP")
legEdepfrac = rt.TLegend(0.75,0.64,0.95,0.89)
legEdepfrac.SetShadowColor(0)
legEdepfrac.SetFillColor(0)
legEdepfrac.SetFillStyle(0)
legEdepfrac.SetLineColor(0)
legEdepfrac.SetLineStyle(0)
legEdepfrac.SetBorderSize(0) 
#legEdepfrac.SetNColumns(2)
legEdepfrac.SetTextFont(62)#42)
for dFile in sorted(hEdepfrac.keys()):
	legEdepfrac.AddEntry(hEdepfrac[dFile],doseFiles[dFile][1],"l")
legEdepfrac.Draw("same")
chLatex.DrawLatex(tagPosX, tagPosY, textBox)
cEdepfrac.SaveAs('plots_'+laserTarget+'/Edepfrac'+saveStr+'.pdf')
cEdepfrac.SaveAs('plots_'+laserTarget+'/Edepfrac'+saveStr+'.png')

cDose = rt.TCanvas("cDose","",50,50,W,H)
cDose.SetLeftMargin( L/W )
cDose.SetRightMargin( R/W )
cDose.SetTopMargin( T/H )
cDose.SetBottomMargin( B/H )
cDose.SetFillColor(0)
cDose.SetBorderMode(0)
cDose.SetFrameFillStyle(0)
cDose.SetFrameBorderMode(0)
if setLogyDose: cDose.SetLogy()
cDose.SetFillColor(0)
cDose.SetBorderMode(0)
cDose.SetFrameFillStyle(0)
cDose.SetFrameBorderMode(0)
hDose[filePath0].Draw("LP")
hDose[filePath0].SetMaximum(max([hDose[hist].GetMaximum() for hist in hDose.keys()]))
if setLogyDose: hDose[filePath0].SetMinimum(1e-10)
hDose[filePath0].GetXaxis().SetRangeUser(xmin,xmax)
for dFile in sorted(hDose.keys()):
	hDose[dFile].Draw("sameLP")
legDose = rt.TLegend(0.75,0.64,0.95,0.89)
legDose.SetShadowColor(0)
legDose.SetFillColor(0)
legDose.SetFillStyle(0)
legDose.SetLineColor(0)
legDose.SetLineStyle(0)
legDose.SetBorderSize(0) 
#legDose.SetNColumns(2)
legDose.SetTextFont(62)#42)
for dFile in sorted(hDose.keys()):
	legDose.AddEntry(hDose[dFile],doseFiles[dFile][1],"l")
legDose.Draw("same")
chLatex.DrawLatex(tagPosX, tagPosY, textBox)
cDose.SaveAs('plots_'+laserTarget+'/Dose'+saveStr+'.pdf')
cDose.SaveAs('plots_'+laserTarget+'/Dose'+saveStr+'.png')

cDosefrac = rt.TCanvas("cDosefrac","",50,50,W,H)
cDosefrac.SetLeftMargin( L/W )
cDosefrac.SetRightMargin( R/W )
cDosefrac.SetTopMargin( T/H )
cDosefrac.SetBottomMargin( B/H )
cDosefrac.SetFillColor(0)
cDosefrac.SetBorderMode(0)
cDosefrac.SetFrameFillStyle(0)
cDosefrac.SetFrameBorderMode(0)
if setLogyDosefrac: cDosefrac.SetLogy()
cDosefrac.SetFillColor(0)
cDosefrac.SetBorderMode(0)
cDosefrac.SetFrameFillStyle(0)
cDosefrac.SetFrameBorderMode(0)
hDosefrac[filePath0].Draw("LP")
hDosefrac[filePath0].SetMaximum(max([hDosefrac[hist].GetMaximum() for hist in hDosefrac.keys()]))
if setLogyDosefrac: hDosefrac[filePath0].SetMinimum(0.001)
hDosefrac[filePath0].GetXaxis().SetRangeUser(xmin,xmax)
for dFile in sorted(hDosefrac.keys()):
	hDosefrac[dFile].Draw("sameLP")
legDosefrac = rt.TLegend(0.75,0.64,0.95,0.89)
legDosefrac.SetShadowColor(0)
legDosefrac.SetFillColor(0)
legDosefrac.SetFillStyle(0)
legDosefrac.SetLineColor(0)
legDosefrac.SetLineStyle(0)
legDosefrac.SetBorderSize(0) 
#legDosefrac.SetNColumns(2)
legDosefrac.SetTextFont(62)#42)
for dFile in sorted(hDosefrac.keys()):
	legDosefrac.AddEntry(hDosefrac[dFile],doseFiles[dFile][1],"l")
legDosefrac.Draw("same")
chLatex.DrawLatex(tagPosX, tagPosY, textBox)
cDosefrac.SaveAs('plots_'+laserTarget+'/Dosefrac'+saveStr+'.pdf')
cDosefrac.SaveAs('plots_'+laserTarget+'/Dosefrac'+saveStr+'.png')

for RFile in RFiles.keys(): RFiles[RFile].Close()

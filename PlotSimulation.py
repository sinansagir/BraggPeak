#!/usr/bin/python

import os,sys,time,math,itertools
import ROOT as rt
from array import array
rt.gROOT.SetBatch(1)
rt.gStyle.SetOptStat(0)

doseFilePaths = {
# 'results_HB_1e21m1_proton_11':[rt.kRed,'I = 1#times10^{21}m1'],
# 'results_HB_5e21m1_proton_11':[rt.kBlack,'I = 5#times10^{21}m1'],
# 'results_HB_1e22m1_proton_11':[rt.kBlue,'I = 1#times10^{22}m1'],
# 'results_HB_5e22m1_proton_11':[rt.kOrange,'I = 5#times10^{22}m1'],

'results_LP_proton_11_Ek15-20':[rt.kRed,'LP, E_{p} = 15-20 MeV'],
'results_LP_proton_11_Ek20-25':[rt.kBlack,'LP, E_{p} = 20-25 MeV'],
'results_LP_proton_11_Ek25-30':[rt.kBlue,'LP, E_{p} = 25-30 MeV'],
'results_HB_5e22m1_proton_11_Ek15-20':[rt.kOrange,'HP, E_{p} = 15-20 MeV'],
'results_HB_5e22m1_proton_11_Ek20-25':[rt.kGreen,'HP, E_{p} = 20-25 MeV'],
'results_HB_5e22m1_proton_11_Ek25-30':[rt.kMagenta,'HP, E_{p} = 25-30 MeV'],

# 'results_HB_1e21m1_proton_11':[rt.kRed,'m1'],
# 'results_HB_1e21m2_proton_11':[rt.kBlack,'m2'],
# 'results_HB_1e21m3_proton_11':[rt.kBlue,'m3'],
# 'results_HB_1e21m4_proton_11':[rt.kOrange,'m4'],

# 'results_HB_5e21m1_proton_11':[rt.kRed,'m1'],
# 'results_HB_5e21m2_proton_11':[rt.kBlack,'m2'],
# 'results_HB_5e21m3_proton_11':[rt.kBlue,'m3'],
# 'results_HB_5e21m4_proton_11':[rt.kOrange,'m4'],

# 'results_HB_1e22m1_proton_11':[rt.kRed,'m1'],
# 'results_HB_1e22m2_proton_11':[rt.kBlack,'m2'],
# 'results_HB_1e22m3_proton_11':[rt.kBlue,'m3'],
# 'results_HB_1e22m4_proton_11':[rt.kOrange,'m4'],

# 'results_HB_5e22m1_proton_11':[rt.kRed,'m1'],
# 'results_HB_5e22m2_proton_11':[rt.kBlack,'m2'],
# 'results_HB_5e22m3_proton_11':[rt.kBlue,'m3'],
# 'results_HB_5e22m4_proton_11':[rt.kOrange,'m4'],

# 'results_HB_5e22m1_proton_11_Ek25-30':[rt.kRed,'m1'],
# 'results_HB_5e22m2_proton_11_Ek25-30':[rt.kBlack,'m2'],
# 'results_HB_5e22m3_proton_11_Ek25-30':[rt.kBlue,'m3'],
# 'results_HB_5e22m4_proton_11_Ek25-30':[rt.kOrange,'m4'],

# 'results_HB_5e22m1_proton_11_Ek25-30':[rt.kRed,'m1, E_{p} = 25-30 MeV'],
# 'results_HB_5e22m2_proton_11_Ek25-30':[rt.kBlack,'m2, E_{p} = 25-30 MeV'],
# 'results_HB_5e22m1_proton_11_Ek50-55':[rt.kBlue,'m1, E_{p} = 50-55 MeV'],
# 'results_HB_5e22m2_proton_11_Ek40-45':[rt.kOrange,'m2, E_{p} = 40-45 MeV'],
}
saveStr='_5e22_LPvsHP'#'_5e22_Ekvaried'
xmin=0
xmax=10
textBox = 'I = 5#times10^{22}'
#textBox = '#splitline{I = 5#times10^{22}}{E_{p} = 25-30 MeV}'
setLogyEdepMM = False
setLogyEdep = False
setLogyEdepfrac = False
setLogyDose = False
setLogyDosefrac = False
EdepUnits = {#Scaling to MeV
'eV':1.e-6,
'keV':1.e-3,
'MeV':1.,
'GeV':1.e3,
}

RFiles = {}
hEdepMM = {}
hEdep = {}
hEdepfrac = {}
hDose = {}
hDosefrac = {}
for doseFilePath in doseFilePaths.keys():
	RFiles[doseFilePath] = rt.TFile(doseFilePath+'/Proton.root')
	hEdepMM[doseFilePath] = RFiles[doseFilePath].Get('1').Clone(doseFilePath)

	with open(doseFilePath+'/DoseFile.txt',"r") as f:
		thelines = f.readlines()
	depth = []
	Edep = []
	Edepfrac = []
	Dose = []
	Dosefrac = []
	for theline in thelines:
		if not theline.startswith(' layer '): continue
		depth_ = float(theline.strip().split()[2])
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
	hEdep[doseFilePath] = rt.TH1D("Edep"+doseFilePath,"",len(xbins)-1,xbins)
	hEdepfrac[doseFilePath] = rt.TH1D("Edep Fraction"+doseFilePath,"",len(xbins)-1,xbins)
	hDose[doseFilePath] = rt.TH1D("Dose"+doseFilePath,"",len(xbins)-1,xbins)
	hDosefrac[doseFilePath] = rt.TH1D("Dose Fraction"+doseFilePath,"",len(xbins)-1,xbins)
	for ibin in range(1,len(xbins)):
		hEdep[doseFilePath].SetBinContent(ibin,Edep[ibin-1])
		hEdepfrac[doseFilePath].SetBinContent(ibin,Edepfrac[ibin-1])
		hDose[doseFilePath].SetBinContent(ibin,Dose[ibin-1])
		hDosefrac[doseFilePath].SetBinContent(ibin,Dosefrac[ibin-1])
	
	hEdepMM[doseFilePath].SetMarkerStyle(20)
	hEdepMM[doseFilePath].SetMarkerSize(1.2)
	hEdepMM[doseFilePath].SetMarkerColor(doseFilePaths[doseFilePath][0])
	hEdepMM[doseFilePath].SetLineWidth(2)
	hEdepMM[doseFilePath].SetLineColor(doseFilePaths[doseFilePath][0])
	hEdepMM[doseFilePath].GetXaxis().SetTitle("Depth [mm]")
	hEdepMM[doseFilePath].GetYaxis().SetTitle("E_{dep} [MeV/mm]")

	hEdep[doseFilePath].SetMarkerStyle(20)
	hEdep[doseFilePath].SetMarkerSize(1.2)
	hEdep[doseFilePath].SetMarkerColor(doseFilePaths[doseFilePath][0])
	hEdep[doseFilePath].SetLineWidth(2)
	hEdep[doseFilePath].SetLineColor(doseFilePaths[doseFilePath][0])
	hEdep[doseFilePath].GetXaxis().SetTitle("Depth [mm]")
	hEdep[doseFilePath].GetYaxis().SetTitle("E_{dep} [MeV]")

	hEdepfrac[doseFilePath].SetMarkerStyle(20)
	hEdepfrac[doseFilePath].SetMarkerSize(1.2)
	hEdepfrac[doseFilePath].SetMarkerColor(doseFilePaths[doseFilePath][0])
	hEdepfrac[doseFilePath].SetLineWidth(2)
	hEdepfrac[doseFilePath].SetLineColor(doseFilePaths[doseFilePath][0])
	hEdepfrac[doseFilePath].GetXaxis().SetTitle("Depth [mm]")
	hEdepfrac[doseFilePath].GetYaxis().SetTitle("E_{dep}/E_{beam} [%]")

	hDose[doseFilePath].SetMarkerStyle(20)
	hDose[doseFilePath].SetMarkerSize(1.2)
	hDose[doseFilePath].SetMarkerColor(doseFilePaths[doseFilePath][0])
	hDose[doseFilePath].SetLineWidth(2)
	hDose[doseFilePath].SetLineColor(doseFilePaths[doseFilePath][0])
	hDose[doseFilePath].GetXaxis().SetTitle("Depth [mm]")
	hDose[doseFilePath].GetYaxis().SetTitle("Dose [Gy]")

	hDosefrac[doseFilePath].SetMarkerStyle(20)
	hDosefrac[doseFilePath].SetMarkerSize(1.2)
	hDosefrac[doseFilePath].SetMarkerColor(doseFilePaths[doseFilePath][0])
	hDosefrac[doseFilePath].SetLineWidth(2)
	hDosefrac[doseFilePath].SetLineColor(doseFilePaths[doseFilePath][0])
	hDosefrac[doseFilePath].GetXaxis().SetTitle("Depth [mm]")
	hDosefrac[doseFilePath].GetYaxis().SetTitle("Dose [%]")
	
H_ref = 600
W_ref = 800
W = W_ref
H = H_ref

# references for T, B, L, R
T = 0.10*H_ref
B = 0.12*H_ref
L = 0.12*W_ref
R = 0.04*W_ref

tagPosX = 0.85
tagPosY = 0.55
chLatex = rt.TLatex()
chLatex.SetNDC()
chLatex.SetTextSize(0.04)
chLatex.SetTextAlign(21) # align center
# chLatex.DrawLatex(tagPosX, tagPosY-0.06, tagString)
# chLatex.DrawLatex(tagPosX, tagPosY-0.12, tagString2)

filePath0 = sorted(doseFilePaths.keys())[0]
cEdepMM = rt.TCanvas("cEdepMM","cEdepMM",50,50,W,H)
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
hEdepMM[filePath0].SetTitle("")
hEdepMM[filePath0].Draw("LP")
hEdepMM[filePath0].SetMaximum(max([hEdepMM[hist].GetMaximum() for hist in hEdepMM.keys()]))
hEdepMM[filePath0].GetXaxis().SetRangeUser(xmin,xmax)
for doseFilePath in sorted(doseFilePaths.keys()):
	hEdepMM[doseFilePath].Draw("sameLP")
legEdepMM = rt.TLegend(0.75,0.64,0.95,0.89)
legEdepMM.SetShadowColor(0)
legEdepMM.SetFillColor(0)
legEdepMM.SetFillStyle(0)
legEdepMM.SetLineColor(0)
legEdepMM.SetLineStyle(0)
legEdepMM.SetBorderSize(0) 
#legEdepMM.SetNColumns(2)
legEdepMM.SetTextFont(62)#42)
for doseFilePath in sorted(doseFilePaths.keys()):
	hEdepMM[doseFilePath].Draw("same")
	legEdepMM.AddEntry(hEdepMM[doseFilePath],doseFilePaths[doseFilePath][1],"l")
legEdepMM.Draw("same")
chLatex.DrawLatex(tagPosX, tagPosY, textBox)
cEdepMM.SaveAs('plots/EdepMM'+saveStr+'.pdf')
cEdepMM.SaveAs('plots/EdepMM'+saveStr+'.png')

cEdep = rt.TCanvas("cEdep","cEdep",50,50,W,H)
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
hEdep[filePath0].GetXaxis().SetRangeUser(xmin,xmax);
for doseFilePath in sorted(doseFilePaths.keys()):
	hEdep[doseFilePath].Draw("sameLP")
legEdep = rt.TLegend(0.75,0.64,0.95,0.89)
legEdep.SetShadowColor(0)
legEdep.SetFillColor(0)
legEdep.SetFillStyle(0)
legEdep.SetLineColor(0)
legEdep.SetLineStyle(0)
legEdep.SetBorderSize(0) 
#legEdep.SetNColumns(2)
legEdep.SetTextFont(62)#42)
for doseFilePath in sorted(doseFilePaths.keys()):
	legEdep.AddEntry(hEdep[doseFilePath],doseFilePaths[doseFilePath][1],"l")
legEdep.Draw("same")
chLatex.DrawLatex(tagPosX, tagPosY, textBox)
cEdep.SaveAs('plots/Edep'+saveStr+'.pdf')
cEdep.SaveAs('plots/Edep'+saveStr+'.png')

cEdepfrac = rt.TCanvas("cEdepfrac","cEdepfrac",50,50,W,H)
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
hEdepfrac[filePath0].GetXaxis().SetRangeUser(xmin,xmax)
for doseFilePath in sorted(doseFilePaths.keys()):
	hEdepfrac[doseFilePath].Draw("sameLP")
legEdepfrac = rt.TLegend(0.75,0.64,0.95,0.89)
legEdepfrac.SetShadowColor(0)
legEdepfrac.SetFillColor(0)
legEdepfrac.SetFillStyle(0)
legEdepfrac.SetLineColor(0)
legEdepfrac.SetLineStyle(0)
legEdepfrac.SetBorderSize(0) 
#legEdepfrac.SetNColumns(2)
legEdepfrac.SetTextFont(62)#42)
for doseFilePath in sorted(doseFilePaths.keys()):
	legEdepfrac.AddEntry(hEdepfrac[doseFilePath],doseFilePaths[doseFilePath][1],"l")
legEdepfrac.Draw("same")
chLatex.DrawLatex(tagPosX, tagPosY, textBox)
cEdepfrac.SaveAs('plots/Edepfrac'+saveStr+'.pdf')
cEdepfrac.SaveAs('plots/Edepfrac'+saveStr+'.png')

cDose = rt.TCanvas("cDose","cDose",50,50,W,H)
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
hDose[filePath0].GetXaxis().SetRangeUser(xmin,xmax)
for doseFilePath in sorted(doseFilePaths.keys()):
	hDose[doseFilePath].Draw("sameLP")
legDose = rt.TLegend(0.75,0.64,0.95,0.89)
legDose.SetShadowColor(0)
legDose.SetFillColor(0)
legDose.SetFillStyle(0)
legDose.SetLineColor(0)
legDose.SetLineStyle(0)
legDose.SetBorderSize(0) 
#legDose.SetNColumns(2)
legDose.SetTextFont(62)#42)
for doseFilePath in sorted(doseFilePaths.keys()):
	legDose.AddEntry(hDose[doseFilePath],doseFilePaths[doseFilePath][1],"l")
legDose.Draw("same")
chLatex.DrawLatex(tagPosX, tagPosY, textBox)
cDose.SaveAs('plots/Dose'+saveStr+'.pdf')
cDose.SaveAs('plots/Dose'+saveStr+'.png')

cDosefrac = rt.TCanvas("cDosefrac","cDosefrac",50,50,W,H)
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
hDosefrac[filePath0].GetXaxis().SetRangeUser(xmin,xmax)
for doseFilePath in sorted(doseFilePaths.keys()):
	hDosefrac[doseFilePath].Draw("sameLP")
legDosefrac = rt.TLegend(0.75,0.64,0.95,0.89)
legDosefrac.SetShadowColor(0)
legDosefrac.SetFillColor(0)
legDosefrac.SetFillStyle(0)
legDosefrac.SetLineColor(0)
legDosefrac.SetLineStyle(0)
legDosefrac.SetBorderSize(0) 
#legDosefrac.SetNColumns(2)
legDosefrac.SetTextFont(62)#42)
for doseFilePath in sorted(doseFilePaths.keys()):
	legDosefrac.AddEntry(hDosefrac[doseFilePath],doseFilePaths[doseFilePath][1],"l")
legDosefrac.Draw("same")
chLatex.DrawLatex(tagPosX, tagPosY, textBox)
cDosefrac.SaveAs('plots/Dosefrac'+saveStr+'.pdf')
cDosefrac.SaveAs('plots/Dosefrac'+saveStr+'.png')

for RFile in RFiles.keys(): RFiles[RFile].Close()

import os,sys,time,sdf,pickle
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import ROOT as rt
from array import array

#                          _ 
#  _._ _..._ .-',     _.._(`)) 
# '-. `     '  /-._.-'    ',/ 
#    )         \            '. 
#   / _    _    |             \ 
#  |  a    a    /              | 
#  \   .-.                     ;   
#   '-('' ).-'       ,'       ; 
#      '-;           |      .' 
#         \           \    / 
#         | 7  .__  _.-\   \ 
#         | |  |  ``/  /`  / 
#        /,_|  |   /,_/   / 
#           /,_/      '`-' 

start_time = time.time()
input = '5e23'
m_number = 'm_1/'
#inputDir = '/run/user/1001/gvfs/smb-share:server=169.254.1.2,share=ozgur/'+str(input)
#inputDir = '/home/ilhan/Epoch_LP_CP/'+str(input)
inputDir = '/run/user/1004/gvfs/smb-share:server=kmufiziknas.local,share=ilhan/helical_beam/'+str(m_number)+str(input)
particle = 'proton'
theNum = 11
c2 = 2.99792458*2.99792458e16
MeV = 6.241509e12
mass_positron = 9.10938291e-31
mass_electron = 9.10938291e-31
mass_proton = 9.10938291e-31*1836.2
mass_photon = 0.0
Ek_min = 50
Ek_max=60
f_out = rt.TFile("Geant4input_"+str(input)+"_"+particle+"_"+str(theNum)+'Ek'+str(Ek_min)+'-'+str(Ek_max)+'.root', "RECREATE")
# hist2d = rt.TH2D(particle+'_7um_values_2d','Energy distribution',6000, 0.5, 6000.5, 1800, -90., 90.)
# hist3d = rt.TH3D(particle+'_7um_values_3d','Energy distribution',100, 0.5, 6000.5, 100, -90., 90., 100, -90., 90.)
t_out = rt.TTree("ana","ana")
b_KE = array('d',[0])
b_We = array('d',[0])
b_Np = array('I',[0])
b_px = array('d',[0])
b_py = array('d',[0])
b_pz = array('d',[0])
t_out.Branch("b_KE", b_KE, "b_KE/D")
t_out.Branch("b_We", b_We, "b_We/D")
t_out.Branch("b_Np", b_Np, "b_Np/I")
t_out.Branch("b_px", b_px, "b_px/D")
t_out.Branch("b_py", b_py, "b_py/D")
t_out.Branch("b_pz", b_pz, "b_pz/D")

angle_lim = [np.tan(-90.*np.pi/180),np.tan(90.*np.pi/180)]
if theNum < 10:
	data = sdf.read(inputDir+"/000%d.sdf" %theNum)
elif theNum<100:
	data = sdf.read(inputDir+"/00%d.sdf" %theNum)
else:
	data = sdf.read(inputDir+"/0%d.sdf" %theNum)
mass = eval('mass_'+particle)
px = eval('data.Particles_Px_'+particle+'.data')
print("(Time elapsed %.2f minutes) Imported Px data..." % ((time.time() - start_time)/60))
py = eval('data.Particles_Py_'+particle+'.data')
print("(Time elapsed %.2f minutes) Imported Py data..." % ((time.time() - start_time)/60))
PYoPX = np.divide(py, px)
print("(Time elapsed %.2f minutes) Calculated Py/Px..." % ((time.time() - start_time)/60))
i = np.where((PYoPX >= angle_lim[0]) & (PYoPX <= angle_lim[1]) & (px>4.7301e-22))
del PYoPX
print("(Time elapsed %.2f minutes) Applied cut on Py/Px..." % ((time.time() - start_time)/60))
px = px[i]
py = py[i]
pz = eval('data.Particles_Pz_'+particle+'.data')[i]
print("(Time elapsed %.2f minutes) Imported Pz data..." % ((time.time() - start_time)/60))
Kinetic_Energy_MeV = (np.sqrt(mass*mass*c2*c2 + (px*px+py*py+pz*pz)*c2) - mass*c2)*MeV
print("(Time elapsed %.2f minutes) Calculated kinetic energy..." % ((time.time() - start_time)/60))
Weight = eval('data.Particles_Weight_'+particle+'.data')[i]
print("(Time elapsed %.2f minutes) Imported Weight data..." % ((time.time() - start_time)/60))
min_weight = min(Weight)
max_weight = max(Weight)
Nentries = len(Weight)
print("Nentries :"), Nentries
print("Minimum Weight :"),min_weight
print("Maximum Weight :"),max_weight
count_progress = 0
for i_ke,i_we,i_px,i_py,i_pz in zip(Kinetic_Energy_MeV,Weight,px,py,pz):
	if count_progress%1e6==0: 
		print("(Time elapsed %.2f minutes) Finished writing %.2f percent ..." % ((time.time() - start_time)/60,count_progress*100/Nentries))
	if i_ke<Ek_min or i_ke>Ek_max: 
		count_progress+=1
		continue
	b_KE[0] = i_ke
	b_We[0] = i_we
	b_Np[0] = int(round(i_we/min_weight))
	b_px[0] = i_px
	b_py[0] = i_py
	b_pz[0] = i_pz
	t_out.Fill()
	count_progress+=1
# 	vec = rt.TVector3(i_pz, i_py, i_px)
# 	theta = vec.Theta() * 180. / np.pi
# 	phi = vec.Phi() * 180. / np.pi
# 	if i_pz < 0: theta = -theta
# 	hist2d.Fill(i_ke, theta, i_we)
# 	hist3d.Fill(i_ke, theta, phi, i_we)
	
t_out.Write()
# hist2d.Write()
# hist3d.Write()
f_out.Close()
del px,py,pz,Weight,Kinetic_Energy_MeV

print("--- %.2f minutes ---" % ((time.time() - start_time)/60))

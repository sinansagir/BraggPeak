#!/bin/bash

for laserTarget in Plasma_Target Solid_Target;
do
for laserInt in 5e21 1e22 5e22 1e23 5e23;
do
for beamPos in bp0cm bp-1p5cm bp-5cm bp-10cm;
do
if [[ "$laserInt" = "5e23" ]]; then
	if [[ "$laserTarget" = "Solid_Target" ]]; then
		EkRangeList=(55-60 95-100 145-150 200-205 245-250 0-1000)
	else
		EkRangeList=(25-30 35-40 55-60 75-80 95-100 115-120 0-1000)
	fi
else
	EkRangeList=(0-1000)
fi
# EkRangeList=(25-30 35-40 55-60 75-80)
for EkRange in ${EkRangeList[@]};
do
    python PlotSimulation.py --laserTarget=$laserTarget --laserInt=$laserInt --EkRange=$EkRange --beamPos=$beamPos 
    python PlotLateral.py --laserTarget=$laserTarget --laserInt=$laserInt --EkRange=$EkRange --beamPos=$beamPos
    python PlotLateral3d.py --laserTarget=$laserTarget --laserInt=$laserInt --EkRange=$EkRange --beamPos=$beamPos 
done
done
done
done


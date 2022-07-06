#!/bin/bash

for laserTarget in Solid_Target;
do
for laserInt in 5e23;
do
for beamPos in bp0cm bp-5cm;
do
EkRangeList=(1100-1150 1500-1550)
for EkRange in ${EkRangeList[@]};
do
    python PlotSimulation.py --laserTarget=$laserTarget --laserInt=$laserInt --EkRange=$EkRange --beamPos=$beamPos 
    python PlotLateral.py --laserTarget=$laserTarget --laserInt=$laserInt --EkRange=$EkRange --beamPos=$beamPos
    python PlotLateral3d.py --laserTarget=$laserTarget --laserInt=$laserInt --EkRange=$EkRange --beamPos=$beamPos 
done
done
done
done


#!/bin/bash

geantPath=/home/ssagir/Simulation/BraggPeak/CarbonPIC_build/
theConf=Solid_Target/tboxVard_bp0cm_bOn50k
theDirs=`find $theConf -type d`
for thepath in $theDirs;
do
if [[ "$thepath" = *"FORDUMMIES"* ]]; then
# if [[ "$thepath" = *"5e23_"*"_p11_Ek2100-2150"* ]]; then
# if [[ "$thepath" = *"5e23_"*"_p11_Ek1100-1150"* || "$thepath" = *"5e23_"*"_p11_Ek0-3000"* ]]; then
	if test -f "${thepath}/carbon.mac"; then
		cd ${thepath}
		rm *.txt *.root run.out
		${geantPath}/carbonPIC carbon.mac >& run.out &
		cd -
	else
		echo "${thepath}/carbon.mac does not exists!"
	fi
fi
done


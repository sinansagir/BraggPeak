#!/bin/bash

geantPath=/home/ssagir/Simulation/BraggPeak/ProtonPIC_build/
theConf=Plasma_Target/tboxVard_bp-5cm_bOn50k
theDirs=`find $theConf -type d`
for thepath in $theDirs;
do
if [[ "$thepath" = *"i5e23_"*"_p11_Ek55-60"* ]]; then
# if [[ "$thepath" = *"i5e23_"*"_p11_Ek25-30"* || "$thepath" = *"i5e23_"*"_p11_Ek35-40"* || "$thepath" = *"i5e23_"*"_p11_Ek55-60"* || "$thepath" = *"i5e23_"*"_p11_Ek75-80"* ]]; then
	if test -f "${thepath}/proton.mac"; then
		cd ${thepath}
		rm *.txt *.root run.out
		${geantPath}/protonPIC proton.mac >& run.out &
		cd -
	else
		echo "${thepath}/proton.mac does not exists!"
	fi
fi
done


check_dir(){
	for file in $1*.aig
	do
	echo "${file}"
	#~/extavy/build/avy/src/avypdr ${file} -v 2 > ${file%.aig}.txt
	#~/extavy/build/avy/src/avypdr ${file} -v 2 -q > ${file%.aig}_q.txt
	done
}

for dir in ~/beem/*/
do
	check_dir ${dir} &
done
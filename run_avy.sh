check_dir(){
	for file in $1*.aig
	do
	echo "${file}"
	~/extavy/build/avy/src/avypdr ${file} -v 2 > ${file%.aig}.txt
	~/extavy/build/avy/src/avypdr ${file} -v 2 -q > ${file%.aig}_q.txt
	done
}

for dir in ~/beem/*/
do
	check_dir ${dir} &
	#echo "${dir}"
    #dir=${dir%*/}      # remove the trailing "/"
    #echo "${dir##*/}"    # print everything after the final "/"
done
# for FILE in *
# do
# 	echo -e "$FILE\nLoops Rule\!" > $FILE
# done
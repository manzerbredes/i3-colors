#!/bin/bash

[ $# -ne 1 ] && { echo "Usage: $0 <run | break>"; exit 1; }

##### Arguments #####
wai=$(dirname $(readlink -f $0))
out=$(mktemp)
[ "$1" == "break" ] && int=1 || int=0
#####################

##### Utils Functions #####
passed(){
    echo -e "$1 ===> \e[32mpassed :)\e[0m"
}
fail(){
   echo -e "$1 ===> \e[5m\e[31mfail :(\e[0m"
}
clean(){
    rm ${out}
}
##################### #####

##### Run Integration Tests #####
nb_pass=0
nb_fail=0
for test in $(find ${wai} -type f -name "test-*.sh")
do
    test_name=$(basename $test)
    expectations="${wai}/${test_name%.*}.out"
    bash ${test} > "${out}" 2>&1 # Run Test
    diff_out=$(diff "${out}" "${expectations}")

    if [ ! -z "${diff_out}" ]
    then
        fail "${test_name}"
        nb_fail=$(( nb_fail + 1 ))

        if [ $int -eq 1 ]
        then
            echo "========== Diff =========="
            echo -e "${diff_out}"
            clean
            exit 1            
        fi  
    else
        nb_pass=$(( nb_pass + 1 ))
        passed "${test_name}"
    fi
done
clean
#################################


echo -e "\n===== STATS ====="
echo "${nb_pass} pass"
echo "${nb_fail} fails"


#!/bin/bash

wai=$(dirname $(readlink -f $0))
out=$(mktemp)
int=0

passed(){
    echo -e "$1 ===> \e[32mpassed :)\e[0m"
}

fail(){
   echo -e "$1 ===> \e[5m\e[31mfail :(\e[0m"
}

[ $# -gt 0 ] && [ $1 == "-b" ] && int=1

##### Run Integration Tests #####
nb_pass=0
nb_fail=0
for test in $(find ${wai} -type f -name "test-*.sh")
do
    test_name=$(basename $test)
    expectations="${test_name%.*}.out"
    bash $test > $out 2>&1
    log=$(diff -q "${out}" "${expectations}")

    if [ ! -z "$log" ]
    then
        fail "${test_name}"
        nb_fail=$(( nb_fail + 1 ))

        if [ $int -eq 1 ]
        then
            echo "========== Diff =========="
            diff "${out}" "${expectations}"
            exit 1
        fi  
    else
        nb_pass=$(( nb_test + 1 ))
        passed "${test_name}"
    fi
done
#################################


echo -e "\n===== STATS ====="
echo "${nb_pass} pass"
echo "${nb_fail} fails"

##### Clear #####
rm ${out}
#################


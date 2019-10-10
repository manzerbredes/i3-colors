#!/bin/bash

[ $# -ne 1 ] && { echo "Usage: $0 <run | break | verbose | reset>"; exit 1; }

##### Arguments #####
wai=$(dirname $(readlink -f $0))
out=$(mktemp)
[ "$1" == "break" ] && int=1 || int=0
[ "$1" == "verbose" ] && verbose=1 || verbose=0
[ "$1" == "reset" ] && reset=1 || reset=0
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
    if [ $reset -eq 1 ]
    then
        bash ${test} > "${out}" 2>&1 # Run Test
        cat "${out}" > "${expectations}"
        continue
    else
        bash ${test} > "${out}" 2>&1 # Run Test
    fi
    diff_out=$(diff "${out}" "${expectations}")

    if [ ! -z "${diff_out}" ]
    then
        fail "${test_name}"
        nb_fail=$(( nb_fail + 1 ))

        if [ $int -eq 1 ] || [ $verbose -eq 1 ]
        then
            echo "========== Diff =========="
            echo -e "${diff_out}"
            if [ $verbose -eq 0 ]
            then
                clean
                exit 1
            fi
        fi  
    else
        nb_pass=$(( nb_pass + 1 ))
        passed "${test_name}"
    fi
done
clean
#################################


if [ $reset -eq 0 ]
then
    echo -e "\n===== STATS ====="
    echo "${nb_pass} pass"
    echo "${nb_fail} fails"

    [ ${nb_fail} -gt 0 ] && exit 1
else
    echo "Reset done."
fi

#!/bin/bash

wai=$(dirname $(readlink -f $0))
theme_loc="${wai}/../themes/"
git_root=$(git rev-parse --show-toplevel)

for shot in ${theme_loc}/*.jpg
do
    name=$(basename ${shot})
    name=${name%.*}
    shot_path=$(realpath --relative-to="${git_root}" "${theme_log}/${shot}")
    
    echo -e "${name}"':\n!['${name}']('${shot_path}')\n'

done

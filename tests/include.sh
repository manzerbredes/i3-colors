#!/bin/bash

wai=$(dirname $(readlink -f $0))
exec=${wai}/../src/i3-colors.py
data=${wai}/data

load() {
    tmp=$(mktemp)
    cp ${1} ${tmp}
    echo ${tmp}
}

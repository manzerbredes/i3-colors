#!/bin/bash

wai=$(dirname $(readlink -f $0))
source "${wai}/include.sh"
tmp=$(mktemp)

##### Test extract theme on a config file then apply it
$exec extract ${data}/config-with-vars > $tmp
$exec apply -d $tmp ${data}/config
rm $tmp


#!/bin/bash

wai=$(dirname $(readlink -f $0))
source "${wai}/include.sh"

##### Load config file
config_file=$(load ${data}/config)

##### Test apply on theme with no variables
$exec apply ${data}/google ${config_file}
cat $config_file
##### Test apply on theme with variables
$exec apply ${data}/seti ${config_file}
cat $config_file 

##### Clear temporary file
rm $config_file

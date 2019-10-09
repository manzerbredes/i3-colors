#!/bin/bash

wai=$(dirname $(readlink -f $0))
source "${wai}/include.sh"

##### Test extract a theme that uses variables on a config file
$exec extract ${data}/config-with-vars


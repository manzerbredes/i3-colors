#!/bin/bash

wai=$(dirname $(readlink -f $0))
source "${wai}/include.sh"

##### Test extract a theme that do not use variables on a config file
$exec extract ${data}/config


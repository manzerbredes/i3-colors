#!/bin/bash

wai=$(dirname $(readlink -f $0))
source "${wai}/include.sh"

##### Test extract on a config file
$exec extract ${data}/config


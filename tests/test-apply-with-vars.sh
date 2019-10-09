#!/bin/bash

wai=$(dirname $(readlink -f $0))
source "${wai}/include.sh"

##### Test apply on theme with variables
$exec apply -d ${data}/seti ${data}/config

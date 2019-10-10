#!/bin/bash

wai=$(dirname $(readlink -f $0))
source "${wai}/include.sh"

##### Test apply on theme with no variables
$exec apply -d ${data}/google ${data}/config-brackets-same-line


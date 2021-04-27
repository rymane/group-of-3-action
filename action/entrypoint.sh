#!/bin/sh -l
echo "Script executed from: ${PWD}"
echo ${ls}

output=$(python3 action/group-of-three.py $1 $2 $3 $4)
echo $output
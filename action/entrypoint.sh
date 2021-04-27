#!/bin/sh -l
echo "Script executed from: ${PWD}"
echo "Files are: ${LS}"

output= $(python3 ../../action/group-of-three.py "$1" "$2" "$3" "$4")
echo output
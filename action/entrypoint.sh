#!/bin/sh -l

output=$(python3 action/group-of-three.py "$1" "$2" "$3" "$4")

echo $output
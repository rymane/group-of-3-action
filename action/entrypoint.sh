#!/bin/sh -l

json_output=$(python3 action/group-of-three.py "$1" "$2" "$3" "$4")

echo $json_output
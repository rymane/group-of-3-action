#!/bin/sh -l

output=$(python3 action/group-of-three.py "$1" "$2" "$3" "$4")

output="${output//'%'/'%25'}"
output="${output//$'\n'/'%0A'}"
output="${output/$'\r'/'%0D'}"

echo "heeeeeeeej"
echo $output >> output.output
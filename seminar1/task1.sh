#!/bin/bash
find_jammy=$(cat /etc/os-release | grep jammy)
ex_code1=$?
find_version=$(cat /etc/os-release | grep '22.04.1')
ex_code2=$?
if [[ $ex_code1 -eq 0 && $ex_code2 -eq 0 ]]
then 
	echo "TEST IS SUCCESSFUL"
else
	echo "TEST IS FAILED"
fi

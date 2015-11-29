#!/usr/bin/env bash

find ../ ! -path '*.git/*' -print0 | while read -d $'\0' file
do
	owner=$(stat --format '%U' "${file}")
	echo "${owner}" > /dev/null
	if [[ "${owner}" = root ]]; then
		sudo chown 1000:100 --from=0:0 "${file}";
	fi
done
#!/usr/bin/env bash

echo "${PWD}"

find "${PWD}" ! -iname '*.pyc' ! -path '**/__pycache__/**' ! -path '**/.git/**' -print0 | while read -d $'\0' _file
do
	owner=$(stat --format '%U' "${_file}")
	echo "${owner}" > /dev/null
	if [[ "${owner}" = 'root' ]]; then
		mode=$(stat --format '%a' "${_file}")
		echo "${mode}" > /dev/null
		sudo chown 1000:100 "${_file}"
		sudo -u 1000 chmod "${mode}" "${_file}"
		if ! [[ "${_file}" =~ .*\.git\/.* ]]; then
			git add "${_file}"
		fi
	fi
done

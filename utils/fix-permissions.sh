#!/usr/bin/env bash

find "${PWD}" -print0 | while read -d $'\0' file
do
	owner=$(stat --format '%U' "${file}")
	echo "${owner}" > /dev/null
	if [[ "${owner}" = 'root' ]]; then
		mode=$(stat --format '%a' "${file}")
		echo "${mode}" > /dev/null
		sudo chown 1000:100 "${file}";
		sudo -u 1000 chmod "${mode}" "${file}"
		if ! [[ "${file}" =~ .*\.git\/.* ]]; then
			git add "${file}"
		fi
	fi
done

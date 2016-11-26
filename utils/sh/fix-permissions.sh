#!/usr/bin/env bash

echo "${PWD}"

{ find "${PWD}" \
	! -iname '*.pyc' \
	! -path '**/__pycache__/**' \
	! -path '**/.git/**' \
	! -path '**/node_modules/**' \
	-print0
} | while read -d $'\0' _file
do
	owner=$(stat --format '%U' "${_file}")

	if [[ "${owner}" = 'root' ]]; then
		mode=$(stat --format '%a' "${_file}")

		sudo chown 1000:100 "${_file}"

		if [[ '1000' = "$(id -u)" ]]; then
			chmod "${mode}" "${_file}"
		else
			sudo -u 1000 chmod "${mode}" "${_file}"
		fi

		if [[ *'.git'* != "${_file}" ]]; then
			git add "${_file}"
		fi
	fi
done

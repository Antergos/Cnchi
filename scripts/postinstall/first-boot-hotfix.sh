#!/bin/bash


mate() {
	# Work-around bug where mate panel doesn't load the default
	# configuration properly on first run.
	mate-panel --reset

	return 0
}


self_destruct() {
	rm "${HOME}/.config/autostart/first-boot-hotfix.desktop"
}


mate && self_destruct

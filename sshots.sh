#!/bin/bash

[[ -z "$1" ]] && echo "Missing parameter" && exit 1

[[ "$1" == "-all" ]] && scrot 'fullscreen_%F_%T_$wx$h.png' -d 2 -c -q 90 -e 'mv $f ~/Screenshots/'

[[ "$1" == "-sel" ]] && scrot 'selection_%F_%T_$wx$h.png' -s -q 90 -e 'mv $f ~/Screenshots/'

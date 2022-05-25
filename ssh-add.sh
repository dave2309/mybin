#!/bin/sh

/usr/bin/ssh-add -l &>/dev/null
if [ $? -eq 0 ]; then
    for key in $HOME/.ssh/*.local
    do
        /usr/bin/ssh-askpass /usr/bin/ssh-add $key
    done
fi
if [ $? -eq 2 ]; then
    echo "no ssh agent found"
fi

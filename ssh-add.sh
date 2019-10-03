#!/bin/sh

/usr/bin/ssh-add -l &>/dev/null
echo $?
if [ $? -eq 0 ]; then
    /usr/bin/ssh-add $HOME/.ssh/agtm-llt05.local
    /usr/bin/ssh-add $HOME/.ssh/agtm-wsl20.local
    /usr/bin/ssh-add $HOME/.ssh/xenial-vm.vagrant.local
fi
if [ $? -eq 2 ]; then
    echo "no ssh agent found"
fi

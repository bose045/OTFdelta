#!/bin/bash

# Remote server details
remote_user="XXXXpprbs"
remote_host="blp04.ccni.rpi"

# Command to execute remotely
remote_command="ls -l ."

# SSH and execute the command
#ssh -o BatchMode=yes -o ConnectTimeout=10 "${remote_user}@${remote_host}" "${remote_command}"

ssh  -o BatchMode=yes -o ConnectTimeout=10 "dcsfen01" "${remote_command}"

# Check if SSH was successful
if [ $? -eq 0 ]; then
    echo "SSH command executed successfully."
else
    echo "SSH failed to execute the command."
fi


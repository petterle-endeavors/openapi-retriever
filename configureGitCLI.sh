#!/bin/bash

# Check if the correct number of parameters are passed
if [ "$#" -ne 2 ]; then
    echo "Usage: ./setupGitCLI.sh [email] [name]"
    exit 1
fi

# Setup git cli with provided email and name
git config --global user.email "$1"
git config --global user.name "$2"
projen
echo "Git has been configured with Email: $1 and Name: $2"
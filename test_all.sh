#!/bin/bash

# Loop through all subdirectories in the current directory
for dir in $(find . -type d -maxdepth 1 ! -path .); do
    # Call the Bash script with the subdirectory as an argument
    ./pytest_and_clean.sh "$dir"
    if [ $? -ne 0 ]; then
        ./pytest_and_clean.sh "$dir -u"
    fi
    if [ $? -ne 0 ]; then
        ./pytest_and_clean.sh "$dir -c"
    fi
    if [ $? -ne 0 ]; then
        echo "Error: $dir"
        exit 1
    fi
done

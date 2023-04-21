#!/bin/bash

# Save the template files' paths
TEMPLATE_DIR="./template"
TEST_FILE="test_solution.py"
CONFIG_FILE="pytest.ini"

if [[ "$1" != "--only-pytest" ]]; then
    # Iterate through all the directories, excluding the "template" directory and hidden folders
    find . -type d -maxdepth 1 ! -path . ! -path "$TEMPLATE_DIR" ! -path './.*' -exec bash -c '
    TEMPLATE_DIR="$1"
    TEST_FILE="$2"
    CONFIG_FILE="$3"
    shift 3

    for dir; do
        # Replace the test_solution.py file
        cp -f "${TEMPLATE_DIR}/${TEST_FILE}" "${dir}/${TEST_FILE}"
        echo "Replaced test_solution.py in ${dir}"

        # Replace the pytest.ini file
        cp -f "${TEMPLATE_DIR}/${CONFIG_FILE}" "${dir}/${CONFIG_FILE}"
        echo "Replaced pytest.ini in ${dir}"
    done
    ' bash "${TEMPLATE_DIR}" "${TEST_FILE}" "${CONFIG_FILE}" {} +

    if [ $? -ne 0 ]; then
        echo "Update test $TEST_FILE and $CONFIG_FILE failed."
        exit 1
    fi
fi

if [[ "$1" != "--only-update" ]]; then
    # Loop through all subdirectories in the current directory
    for dir in $(find . -type d -maxdepth 1 ! -path . ! -path './.*' ! -path "./template"); do
        echo "Running pytest for $dir ..."
        # Call the Bash script with the subdirectory as an argument
        ./pytest_and_clean.sh "$dir"

        if [ $? -ne 0 ]; then
            ./pytest_and_clean.sh "$dir" -u
        fi

        if [ $? -ne 0 ]; then
            ./pytest_and_clean.sh "$dir" -c
        fi
        
        if [ $? -ne 0 ]; then
            echo "Error: $dir"
            exit 2
        fi
    done
fi

echo "$0: completed successfully."
exit 0

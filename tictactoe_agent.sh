#!/bin/bash

# Check if exactly three arguments are given
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 n k [xo]"
    exit 1
fi

# Check if the first two arguments are integers
if ! [[ "$1" =~ ^[0-9]+$ ]] || ! [[ "$2" =~ ^[0-9]+$ ]]; then
    echo "Error: 'n' and 'k' must be integers."
    echo "Usage: $0 n k [xo]"
    exit 1
fi

# Execute the Python script with provided arguments
python3 main.py $1 $2 $3

#!/bin/bash

# Set the input and output file names
input_dir="src/"
output_file="src/combined.txt"

# Combine all the Python files into a single text file
cat ${input_dir}/*.py > ${output_file}

# Optionally, remove the header lines that start with "#!" or "# coding"
sed -i '/^#![[:print:]]*$/d' ${output_file}


mv src/combined.txt src/combined.py

# Print a message indicating that the conversion is complete
echo "Conversion complete. The combined Python files are now in python ${output_file}."



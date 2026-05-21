#!/bin/bash

# Navigate to project root
project_dir=$(dirname "$(dirname "$(realpath "$0")")")
cd "$project_dir" || exit 1

# Get the full path of the file to keep
nxs_file=$(python3 -c "from pynxtools.nomad import get_package_filepath; print(get_package_filepath())")

# Define the target directory
target_dir="src/pynxtools/nomad/schema_packages"

# Delete all matching files except nxs_file
for file in "$target_dir"/nxs_metainfo_package_*.json; do
    [ -e "$file" ] || continue

    abs_file=$(realpath "$file")

    if [[ "$abs_file" != "$nxs_file" ]]; then
        echo "Deleting: $abs_file"
        rm "$file"
    else
        echo "Keeping: $abs_file"
    fi
done
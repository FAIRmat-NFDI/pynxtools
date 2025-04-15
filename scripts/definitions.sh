#!/usr/bin/env bash

# Usage:
#   ./scripts/update_or_reset_definitions.sh update   # Updates the definitions submodule
#   ./scripts/update_or_reset_definitions.sh reset    # Resets the definitions submodule
#
# This script updates or resets the definitions and generates the metainfo package.
# Only works if you have pynxtools installed in editable mode.

set -e

update_nexus_version() {
  cd src/pynxtools/definitions && echo "updating nexus-version.txt"
  printf "$(git describe --dirty --tags --long --abbrev=8 --match '*[0-9]*')" > ../nexus-version.txt
  cd ../../../
}

update_definitions_submodule() {
  echo "updating definitions submodule"
  git submodule sync --recursive
  git submodule update --init --recursive --remote --jobs=4
  git submodule foreach --recursive 'git fetch --tags'
}

reset_definitions_submodule() {
  echo "resetting definitions submodule"
  git submodule deinit -f .
  git submodule update --init
}

if [[ "$1" != "update" && "$1" != "reset" ]]; then
  echo "Error: Please specify either 'update' or 'reset'"
  echo "Usage: $0 [update|reset]"
  exit 1
fi

project_dir=$(dirname $(dirname $(realpath "$0")))
cd "$project_dir"

if [[ "$1" == "update" ]]; then
  update_definitions_submodule
elif [[ "$1" == "reset" ]]; then
  reset_definitions_submodule
fi

update_nexus_version
python ./scripts/generate_package.py
#!/usr/bin/env bash

# This script updates or resets the definitions.
# Usage:
#   ./scripts/definitions.sh update   # Updates the definitions submodule
#   ./scripts/definitions.sh reset    # Resets the definitions submodule

set -e

DEFINITIONS_FOLDER="src/pynxtools/definitions"

update_nexus_version() {
  cd $DEFINITIONS_FOLDER && echo "updating nexus-version.txt"
  printf "$(git describe --dirty --tags --long --abbrev=8 --match '*[0-9]*')" > ../nexus-version.txt
  cd ../../../
}

update_definitions_submodule() {
  echo "updating definitions submodule"
  git submodule sync $DEFINITIONS_FOLDER
  git submodule update --init --remote --jobs=4 $DEFINITIONS_FOLDER
  git -C src/pynxtools/definitions fetch --tags
}

reset_definitions_submodule() {
  echo "resetting definitions submodule"
  git submodule deinit -f $DEFINITIONS_FOLDER
  git submodule update --init $DEFINITIONS_FOLDER
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
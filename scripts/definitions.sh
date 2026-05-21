#!/usr/bin/env bash

# This script manages the definitions submodule.
# Usage:
# ./scripts/definitions.sh update
# ./scripts/definitions.sh reset
# ./scripts/definitions.sh checkout <REV>
# <REV> can be:
# - commit hash
# - tag
# - branch name
#
# If <REV> is a branch, the submodule will track that branch in .gitmodules.
# If <REV> is a commit or tag, the submodule is left in detached HEAD state.

set -euo pipefail

DEFINITIONS_FOLDER="src/pynxtools/definitions"

update_nexus_version() {
  cd "$DEFINITIONS_FOLDER" && echo "updating nexus-version.txt"
  printf "$(git describe --dirty --tags --long --abbrev=8 --match '*[0-9]*')" > ../nexus-version.txt
  cd ../../../
}

get_default_branch() {
  git -C "$DEFINITIONS_FOLDER" remote show origin | awk '/HEAD branch/ {print $NF}'
}

update_definitions_submodule() {
  echo "updating definitions submodule"
  git submodule sync "$DEFINITIONS_FOLDER"
  git submodule update --init --remote --jobs=4 "$DEFINITIONS_FOLDER"
  git -C "$DEFINITIONS_FOLDER" fetch --tags
}

reset_definitions_submodule() {
  echo "resetting definitions submodule"

  # Remove branch tracking from .gitmodules
  git config -f .gitmodules --unset \
    submodule.$DEFINITIONS_FOLDER.branch || true

  # Remove branch tracking from local config as well
  git config --unset \
    submodule."$DEFINITIONS_FOLDER".branch || true

  git submodule sync "$DEFINITIONS_FOLDER"

  # Force checkout of the commit recorded in the superproject
  git submodule update --init --force --checkout \
    "$DEFINITIONS_FOLDER"

  # Ensure clean working tree
  git -C "$DEFINITIONS_FOLDER" reset --hard
  git -C "$DEFINITIONS_FOLDER" clean -fd
}


checkout_definitions() {
  local ref="$1"

  echo "checking out definitions submodule at: $ref"

  git submodule update --init "$DEFINITIONS_FOLDER"
  git -C "$DEFINITIONS_FOLDER" fetch --tags origin

  git -C "$DEFINITIONS_FOLDER" checkout "$ref"

  # Check whether we are on a branch or detached HEAD
  local current_branch
  current_branch="$(git -C "$DEFINITIONS_FOLDER" branch --show-current)"

  if [[ -n "$current_branch" ]]; then
    echo "detected branch checkout: $current_branch"

    local default_branch
    default_branch="$(get_default_branch)"

    if [[ "$current_branch" == "$default_branch" ]]; then
      echo "removing submodule branch setting from .gitmodules (default branch)"
      git config -f .gitmodules --unset \
        submodule.$DEFINITIONS_FOLDER.branch || true
    else
      echo "setting submodule to track branch: $current_branch"
      git config -f .gitmodules \
        submodule.$DEFINITIONS_FOLDER.branch "$current_branch"
    fi
  else
    echo "detected detached checkout (commit or tag)"
    git config -f .gitmodules --unset \
      submodule.$DEFINITIONS_FOLDER.branch || true
  fi

  git submodule sync "$DEFINITIONS_FOLDER"
}

print_usage() {
echo "Usage:"
echo "  $0 update"
echo "  $0 reset"
echo "  $0 checkout <REV>"
exit 1
}

main() {
if [[ $# -lt 1 ]]; then
print_usage
fi

project_dir=$(dirname "$(dirname "$(realpath "$0")")")
cd "$project_dir"

case "$1" in
update)
update_definitions_submodule
;;
reset)
reset_definitions_submodule
;;
checkout)
[[ $# -eq 2 ]] || print_usage
checkout_definitions "$2"
;;
*)
echo "Error: Unknown command '$1'"
print_usage
;;
esac

update_nexus_version
}

main "$@"
python ./scripts/generate_package.py
#!/usr/bin/env bash

# This script manages the definitions submodule.
# Usage:
#   ./scripts/definitions.sh update
#   ./scripts/definitions.sh reset
#   ./scripts/definitions.sh commit <COMMIT>
#   ./scripts/definitions.sh branch <BRANCH>   # Use "default" to auto-detect the submodule's default branch

set -euo pipefail

DEFINITIONS_FOLDER="src/pynxtools/definitions"

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
  git submodule deinit -f "$DEFINITIONS_FOLDER"
  git submodule update --init "$DEFINITIONS_FOLDER"
}

checkout_definitions_commit() {
  local commit="$1"
  echo "checking out definitions submodule at commit: $commit"
  git submodule update --init "$DEFINITIONS_FOLDER"
  git -C "$DEFINITIONS_FOLDER" fetch
  git -C "$DEFINITIONS_FOLDER" checkout "$commit"
}

track_definitions_branch() {
  local input_branch="$1"
  local resolved_branch="$input_branch"

  if [[ "$input_branch" == "default" ]]; then
    resolved_branch="$(get_default_branch)"
    echo "resolved default branch to: $resolved_branch"
  fi

  echo "tracking definitions submodule on branch: $resolved_branch"

  git submodule update --init "$DEFINITIONS_FOLDER"
  git -C "$DEFINITIONS_FOLDER" fetch
  git -C "$DEFINITIONS_FOLDER" checkout "$resolved_branch"
  git -C "$DEFINITIONS_FOLDER" pull origin "$resolved_branch"

  local default_branch
  default_branch="$(get_default_branch)"

  if [[ "$resolved_branch" == "$default_branch" ]]; then
    if git config -f .gitmodules --get submodule.$DEFINITIONS_FOLDER.branch &>/dev/null; then
      echo "removing submodule branch setting from .gitmodules (back to default)"
      git config -f .gitmodules --unset submodule.$DEFINITIONS_FOLDER.branch
      git submodule sync "$DEFINITIONS_FOLDER"

      # Remove any resulting empty line left by the unset command
      # Works by collapsing multiple newlines into one
      sed -i '/^\s*$/N;/^\n$/D' .gitmodules
    else
      echo "no custom branch setting found in .gitmodules; nothing to remove"
    fi
  else
    echo "setting submodule to track branch: $resolved_branch in .gitmodules"
    git config -f .gitmodules submodule.$DEFINITIONS_FOLDER.branch "$resolved_branch"
    git submodule sync "$DEFINITIONS_FOLDER"
  fi
}


print_usage() {
  echo "Usage:"
  echo "  $0 update"
  echo "  $0 reset"
  echo "  $0 commit <COMMIT>"
  echo "  $0 branch <BRANCH>     # Use 'default' to track the submodule's default branch temporarily (no .gitmodules change)"
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
    commit)
      [[ $# -eq 2 ]] || print_usage
      checkout_definitions_commit "$2"
      ;;
    branch)
      [[ $# -eq 2 ]] || print_usage
      track_definitions_branch "$2"
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
# Resets the definitions and git restores the metainfo packages.
# Only works if you have pynxtools installed in editable mode.

update_nexus_version() {
  cd src/pynxtools/definitions && echo "updating nexus-version.txt"
  printf "$(git describe --dirty --tags --long --abbrev=8 --match '*[0-9]*')" > ../nexus-version.txt
  cd ../../../
}

reset_definitions_submodule() {
  echo "resetting definitions submodule"
  git submodule deinit -f .
  git submodule update --init
}

project_dir=$(dirname $(dirname $(realpath $0)))
cd $project_dir

reset_definitions_submodule
update_nexus_version
python ./scripts/generate_package.py
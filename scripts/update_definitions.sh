# Updates the definitions and generates the metainfo package.
# Only works if you have pynxtools installed in editable mode.

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

project_dir=$(dirname $(dirname $(realpath $0)))
cd $project_dir

update_definitions_submodule
update_nexus_version
python ./scripts/generate_package.py


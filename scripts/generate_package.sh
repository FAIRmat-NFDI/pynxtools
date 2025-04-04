# Only generates the metainfo package

project_dir=$(dirname $(dirname $(realpath $0)))
cd $project_dir

echo "generating NOMAD metainfo package"
echo "removed old package, now generating new version"
rm -f src/pynxtools/nomad/nxs_metainfo_package.json
python src/pynxtools/nomad/schema.py


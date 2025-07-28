#!/bin/sh
working_dir=$(pwd)
project_dir=$(dirname $(dirname $(realpath $0)))

cd $project_dir


uv pip compile --universal -p 3.12 --extra=dev \
    --extra=docs --output-file=dev-requirements.txt \
    pyproject.toml
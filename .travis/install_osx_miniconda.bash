#!/bin/bash

# We do this conditionally because it saves us some downloading if the
# version is the same.
if [[ "$PYHDF_PYTHON_VERSION" == "2.7" ]]; then
	curl https://repo.anaconda.com/miniconda/Miniconda2-latest-MacOSX-x86_64.sh > miniconda.sh;
else
	curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh > miniconda.sh;
fi
bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
hash -r
conda config --set always_yes yes --set changeps1 no
conda update -q conda
# Useful for debugging any issues with conda
conda info -a

conda create -q -n test-environment python=$PYHDF_PYTHON_VERSION numpy hdf4 nose
source activate test-environment

export LIBRARY_DIRS=$CONDA_PREFIX/lib
export INCLUDE_DIRS=$CONDA_PREFIX/include

#!/bin/sh

set -ev

if [ -z "$PYTHON" ]; then
	PYTHON=python
fi

$PYTHON setup.py build_ext --inplace

cd examples/compress/
$PYTHON ./test-compress.py >/dev/null

cd ../vgroup/
$PYTHON ./vgwrite.py
$PYTHON ./vgread.py inventory.hdf >/dev/null

cd ../inventory
$PYTHON ./inventory_1-1.py
$PYTHON ./inventory_1-2.py
$PYTHON ./inventory_1-3.py
$PYTHON ./inventory_1-4.py >/dev/null
$PYTHON ./inventory_1-5.py >/dev/null

cd ../txttohdf
$PYTHON ./txttohdf.py

cd ../hdfstruct
for f in `find .. -name '*.hdf'`; do
	echo running hdfstruct.py $f
	$PYTHON ./hdfstruct.py $f >/dev/null
done

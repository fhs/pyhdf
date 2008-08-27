DOC_PATH=~/code/pyhdf

echo "Building installation instructions..."
if [[ -x ${DOC_PATH} ]]; then
  rst2html ${DOC_PATH}/INSTALL --stylesheet="default.css" \
    --link-stylesheet | tools/grab_body.py | \
    tail -n +2 | head -n -1 \
    > source/install.html
else
  echo "!!! Source directory not available, using distributed instructions."
fi

echo "Copying images and stylesheets to target directory..."
mkdir -p output/images
cp -r images output/
cp source/*.css output/

echo "Inserting contents into templates..."
for page in "index" "install" "example" "documentation"; do
    python ./tools/insert_content.py source/template.html \
        source/sidebar.html source/news.html \
        "source/${page}.html" > "output/${page}.html"
done

rm -rf docs

mkdir docs
cd docs
sphinx-quickstart  \
    --sep \
    --dot=_ \
    -p "Blockchain Vaccination Records" \
    -a "Benedikt Bock, Alexander Preuß, Toni Stachewicz" \
    -v 0.0.1 \
    -r 0.0.1    \
    -l en \
    --suffix=.rst \
    --master=index \
    --ext-autodoc \
    --makefile   \
    --no-batchfile

sed -i '20,21 s/# //' source/conf.py
sed -i "22 s/.*/sys.path.insert(0, os.path.abspath('..\/..'))/" source/conf.py

sphinx-apidoc -f -o source/ ../blockchain/

make html

xdg-open build/html/index.html &

#/bin/sh

export VERSION="1.2.15"
export VENV=$VIRTUAL_ENV
mkdir -p $VENV/packages
cd $VENV/packages

curl -O http://oligarchy.co.uk/xapian/${VERSION}/xapian-bindings-${VERSION}.tar.gz

tar xzvf xapian-bindings-${VERSION}.tar.gz

export LD_LIBRARY_PATH=$VENV/lib

cd $VENV/packages/xapian-bindings-${VERSION}
./configure --prefix=$VENV --with-python && make && make install

python -c "import xapian"

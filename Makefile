PYTHON=`which python`
DESTDIR=/
PROJECT=guild-kamaelia
VERSION=0.0.2

all:
	@echo "make source - Create source package"
	@echo "make install - Install on local system (only during development)"
	@echo "make deb - Generate a deb package - for local testing"
	@echo "make clean - Get rid of scratch and byte files"
	@echo "make test - Run any unit tests"

source:
	$(PYTHON) setup.py sdist $(COMPILE)

install:
	$(PYTHON) setup.py install --root $(DESTDIR) $(COMPILE)

deb:
	python setup.py sdist
	cd dist && py2dsc $(PROJECT)-* && cd deb_dist/$(PROJECT)-$(VERSION) && debuild -uc -us

ppadeb:
	python setup.py sdist
	cd dist && py2dsc $(PROJECT)-* && cd deb_dist/$(PROJECT)-$(VERSION) && debuild -S && dput ppa:sparkslabs/packages $(PROJECT)_*_source.changes

use:
	sudo dpkg -i dist/deb_dist/python-$(PROJECT)*deb

purge:
	sudo apt-get purge python-$(PROJECT)

clean:
	$(PYTHON) setup.py clean
	rm -rf build/ MANIFEST
	find . -name '*.pyc' -delete

distclean:
	$(PYTHON) setup.py clean
	rm -rf dist
	rm -rf build/ MANIFEST
	find . -name '*.pyc' -delete

devloop: purge distclean deb use
	echo

test:
	behave

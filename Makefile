#!env make
###
# Makefile
###

help:
	@echo "make sdist - Create source distribution package"
	@echo "make install - Install on local system"
	@echo "make clean - Get rid of scratch and byte files"
	@echo "make test - Run tests"

sdist: test clean setuppy
	pysetup run sdist 
	mv dist/*.tar.gz ..
	rmdir dist
	rm -rf build

install: test
	pysetup install 

setuppy: setup.cfg
	rm -f setup.py
	pysetup generate-setup

clean:
	pysetup run clean
	rm -rf build
	rm -rf dist

lint:
	find . -name "build" -prune -or  -exec "file" "{}" ";" | grep Python | cut -d ':' -f 1 |  egrep -v "steps|setup.py" | xargs flake8 

test:
	pysetup run test
	behave

#!/bin/sh

nosetests -vsd --with-coverage --cover-erase --cover-html \
 --cover-package=tomahawk.base,tomahawk.command,tomahawk.rsync \
 tests/internal/

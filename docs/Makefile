# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = pyunitwizard
SOURCEDIR     = .
BUILDDIR      = _build
PYTHON        = python


.PHONY: help builddir clean-api html builddir_es pots pots_to_pos html_es clean clean_es

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html      to make standalone HTML files"
	@echo "  clean-api to remove generated autosummary stubs under api/"
	@echo "  clean     to clean the directory starting a new compilation from scratch"

builddir:
	mkdir -p $(BUILDDIR)

clean-api:
	$(PYTHON) clean_api.py

# Stale stubs are removed before building so that pages for symbols dropped
# from the public API do not survive into the rendered site.
html: clean-api builddir
	$(SPHINXBUILD) -b html $(SOURCEDIR) $(BUILDDIR)
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)"

clean: clean-api
	rm -rf $(BUILDDIR)
	rm -rf jupyter_execute


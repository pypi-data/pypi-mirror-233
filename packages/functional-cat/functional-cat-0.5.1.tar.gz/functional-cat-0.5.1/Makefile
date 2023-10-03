.PHONY: build publish

build:
	pip install build
	python -m build

publish: build
	pip install twine
	twine upload dist/*
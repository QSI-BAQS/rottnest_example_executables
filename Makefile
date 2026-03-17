TARGET=rottnest_example_executables

.PHONY: all clean test update

all: build

build:
	pip install -e .

test:
	pytest

update:
	git pull
	${MAKE} build

clean:
	pip uninstall -y $(TARGET) || true

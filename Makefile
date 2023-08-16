IMAGE_NAME := ""
PROJECT_NAME := "boxcraft"
PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
FILES_CLEAN := "__pycache__|pytest"

.PHONY: build
build:
	python3 setup.py sdist bdist_wheel

.PHONY: clean
clean:
	rm -rf dist/ build/ ${PROJECT_NAME}.egg-info

docker-build:
	@if [[ ${IMAGE_NAME} == "" ]]; then echo ">>> IMAGE_NAME is not set"; exit 1; fi
	@docker buildx build --no-cache --build-arg BUILD_DATE=`date -u +%Y-%m-%dT%H:%M:%SZ` -t ${IMAGE_NAME} .

docker-rmi:
	@if [[ ${IMAGE_NAME} == "" ]]; then echo ">>> IMAGE_NAME is not set"; exit 1; fi
	@docker rmi -f ${IMAGE_NAME}

clean-files:
	@find "${PROJECT_DIR}/${PROJECT_NAME}" -type d | grep -E ${FILES_CLEAN} | while read -r item; do \
        echo "Removing: $$item"; \
		rm -fr $$item; \
    done
# Convenience targets for building images and running the NASP rApp

PYTHON ?= python3
DOCKER ?= docker
HELM ?= helm
APP ?= src/rApp_NASP.py
CONFIG ?= src/config/config.yaml

IMAGE_NAME ?= rapp_nasp
IMAGE_TAG ?= 0.1
REGISTRY ?= zanattabruno
LOCAL_IMAGE ?= $(IMAGE_NAME):$(IMAGE_TAG)
REMOTE_IMAGE ?= $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)
CONTAINER_NAME ?= rapp-nasp
HELM_CHART ?= helm/rapp-nasp
HELM_RELEASE ?= rapp-nasp
HELM_NAMESPACE ?= ricrapp

.PHONY: help build tag push run docker-run install

help:
	@echo "Available targets:"
	@echo "  make build       Build local Docker image ($(LOCAL_IMAGE))"
	@echo "  make tag         Tag local image as $(REMOTE_IMAGE)"
	@echo "  make push        Build, tag, and push the image to the registry"
	@echo "  make run         Run the Flask app locally with the configured YAML"
	@echo "  make docker-run  Run the Docker image locally and expose the API port"
	@echo "  make install     Deploy/upgrade the Helm release"

build:
	$(DOCKER) build -t $(LOCAL_IMAGE) .

tag: build
	$(DOCKER) tag $(LOCAL_IMAGE) $(REMOTE_IMAGE)

push: tag
	@$(DOCKER) info >/dev/null 2>&1 || (echo "Docker daemon not reachable" && exit 1)
	@$(DOCKER) info | grep -q Username || (echo "Docker login required" && exit 1)
	$(DOCKER) push $(REMOTE_IMAGE)

run:
	$(PYTHON) $(APP) --config $(CONFIG)

# Provides a quick way to test the image locally
docker-run: build
	$(DOCKER) run --rm -it -p $(HOST_PORT):$(APP_PORT) --name $(CONTAINER_NAME) $(LOCAL_IMAGE)

install:
	$(HELM) upgrade --install $(HELM_RELEASE) $(HELM_CHART) \
		--namespace $(HELM_NAMESPACE)

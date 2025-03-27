FLASK_IMAGE_NAME = timeline-flask
FLUENTD_IMAGE_NAME = fluentd
TAG = latest
USER_NAME = $(DOCKER_USER)
PASSWORD = $(DOCKER_PASSWORD)

build_flask:
	docker build -t $(USER_NAME)/$(FLASK_IMAGE_NAME):$(TAG) .

build_fluentd:
	docker build -t $(USER_NAME)/$(FLUENTD_IMAGE_NAME):$(TAG) ./fluentd/

login:
	echo $(PASSWORD) | docker login -u $(USER_NAME) --password-stdin

push_images: login
	docker push $(USER_NAME)/$(FLASK_IMAGE_NAME):$(TAG)
	docker push $(USER_NAME)/$(FLUENTD_IMAGE_NAME):$(TAG)

all: build_flask build_fluentd push_images
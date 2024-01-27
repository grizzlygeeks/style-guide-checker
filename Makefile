TOPDIR=$(PWD)
WHOAMI=$(shell whoami)

run:
	python3 run.py

image:
	docker build --platform=linux/arm64 -t ${WHOAMI}/style-guide-action:arm64 .
	docker build --platform=linux/amd64 -t ${WHOAMI}/style-guide-action:amd64 .

image-push: image
	docker push ${WHOAMI}/style-guide-action:arm64
	docker push ${WHOAMI}/style-guide-action:amd64

image-run: image
	docker run -ti --rm -v ${TOPDIR}:/usr/src/app ${WHOAMI}/style-guide-action:arm64 python3 run.py
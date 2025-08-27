build:
	docker build -t equity . --no-cache

prod:
	docker build -t yashubeast/nerv:equity . --no-cache

push:
	docker push yashubeast/nerv:equity
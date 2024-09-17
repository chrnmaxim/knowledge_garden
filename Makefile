prepare:
	python walk.py
serve:
	make prepare
	npx quartz build --serve
build:
	make prepare
	npx quartz build
deploy:
	make prepare
	npx quartz sync
all:
	$(MAKE) build_image

build_image:
	python allocate.py

	mkfs.lucario system.img

	lucariofs-write system.img system/vfs.py
	lucariofs-write system.img system/stage2.py

run:
	python src/main.py

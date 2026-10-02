.PHONY: install run clean

install:
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install opencv-python pyserial screeninfo

run:
	venv/bin/python Controller.py

clean:
	-lsof 2>/dev/null | awk '/\/dev\/cu\.usbmodem[0-9]+/ {print $$2}' | sort -u | xargs kill -9 2>/dev/null
	-pkill -9 -f Controller.py 2>/dev/null
	rm -rf venv
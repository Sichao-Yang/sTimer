dist: dep
	pyinstaller --onefile --windowed --icon=asset/timer.ico stimer.py
	cp cfg.ini dist
	cp asset dist -r
	rm -rf build *.spec

dep: requirements.txt
	pip install -r requirements.txt

clean:
	rm -rf build dist *.egg-info *.spec

feature:
	python3 tongue_twister.py

cached: brown_None.pyz
	python3 tongue_twister.py -m brown_None.pyz

fresh:
	python3 tongue_twister.py -t 20000

brown_None.pyz:
	python3 tongue_twister.py -t -1

clean:
	rm -f *.pyz *.pyc

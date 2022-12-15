install:
	# install commands
	pip install --upgrade pip &&\
		pip install -r requirements.txt

run:
	# run script
	python3 -m venv env
	source env/bin/activate&&\
		pip install --upgrade pip &&\
			pip install -r requirements.txt &&\
				python3 main.py

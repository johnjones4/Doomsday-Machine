install:
		pip3 install -r requirements.txt

backup:
		python3 backup.py

webserver:
		python3 webserver.py

authenticate:
		python3 generate_credentials.py

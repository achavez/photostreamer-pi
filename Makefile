test:
	- flake8 --exclude=env/*,*/migrations/* .
	- coverage run manage.py test
	- coverage html

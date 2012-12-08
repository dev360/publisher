all: runserver

runserver:
	@cd src/publisher && python manage.py runserver

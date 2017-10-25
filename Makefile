PORT=5000

init:
	pip install -r requirements.txt
	if [ ! -f ./todo.db ]; then \
		python manage.py init_db ; \
	fi;

docker-run:
	docker build --file=./Dockerfile --tag=flask_hs3 ./
	docker run -it -p $(PORT):5000 flask_hs3

run: init
	python manage.py runserver --host 0.0.0.0
	
reset-db:
	python manage.py drop_db
	python manage.py init_db

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +


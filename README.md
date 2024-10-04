Start all services 
 - docker-compose up --build

Start service without tests and linters
 - docker-compose up --build train gatekeeper central redis celery_worker celery_beat


start all tests
 - docker-compose up --abort-on-container-exit test_train test_central test_gatekeeper

start train tests
 - docker-compose up --build test_train

start central tests
 - docker-compose up --build test_central

start gatekeeper tests
 - docker-compose up --build test_gatekeeper

run linters and formatters for all folders
 - docker-compose run flake8
 - docker-compose run black

status gatekeeper
 - http://localhost:5001/gate/status
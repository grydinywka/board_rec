# board_rec
test app for 'light it'

For looking app 'alive', follow 
https://board-of-messages.herokuapp.com/

Launch this app locally:

Work on Linux. Open teminal.

$ wget https://bootstrap.pypa.io/get-pip.py

$ sudo python get-pip.py

$ sudo pip install virtualenv

$ virtualenv board --no-site-packages

$ cd board

$ source bin/activate

(board)$ pip install Django

(board)$ mkdir src

(board)$ cd src

(board)$ git clone  git@github.com:grydinywka/board_rec.git

(board)$ cd board_rec/

(caesar)$ pip install -r requirements.txt

Next stage, we should create database. Open postgresql(if need - install one ):

=# create database board_rec_db;

=# create user board_msgs_db_user with password 'board_msgs_db_user';

=# grant connect on database board_rec_db to board_msgs_db_user;

(caesar)$ cd ../../bin

(caesar)$ gedit activate

add to end file next two lines:

DJANGO_SETTINGS_MODULE="board.development_settings"

export DJANGO_SETTINGS_MODULE

Save file

(board)$ deactivate

$ source activate

(board)$ cd ../src/board_rec/

(board)$ python manage.py migrate

(board)$ python manage.py runserver localhost:8000

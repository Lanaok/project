sudo apt install mysql-server -y
sudo mysql -padmin -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'admin';"
sudo mysql -padmin -e "create database queue_system_db"
sudo apt install python3 -y
sudo apt install python3-pip -y
sudo pip3 install virtualenvwrapper
source ~/.bashrc
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV_ARGS=' -p /usr/bin/python3 '
export PROJECT_HOME=$HOME/Devel
echo 'export WORKON_HOME="$HOME/.virtualenvs"' >> ~/.bashrc
echo 'export VIRTUALENVWRAPPER_PYTHON="/usr/bin/python3"' >> ~/.bashrc
echo 'export VIRTUALENVWRAPPER_VIRTUALENV_ARGS=" -p /usr/bin/python3"' >> ~/.bashrc
echo 'export PROJECT_HOME="$HOME/Devel"' >> ~/.bashrc
source ~/.bashrc
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv django_venv
pip install Django
pip install django-allauth
sudo apt-get install libmysqlclient-dev -y
pip install mysqlclient
cd mysite
python manage.py makemigrations
python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'admin')" | python manage.py shell
python manage.py runserver


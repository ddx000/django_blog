# Django-blog
- Use Django, Bootstrap, PostgreSQL, Gunicorn, Nginx to build a blog for my personal use.  
- Use docker-compose, PostgreSQL(AWS RDS),  deployed on AWS EC2 with SSL Certificate (Let's encrypt it).  
- Website: https://cwhuang.serveblog.net/  
- Images
    - Structure of the website
![](https://i.imgur.com/v3SJI6i.png)
    - Homepage
![](https://i.imgur.com/g2FIQm6.png)
    - Login
![](https://i.imgur.com/3oy06VQ.png)
    - Register
![](https://i.imgur.com/abZrHBY.png)
    - Post
![](https://i.imgur.com/TWgmarR.png)
    - Update Profile
![](https://i.imgur.com/qCjecO0.png)
    - Reset Password
![](https://i.imgur.com/VUpSyZ1.png)
    - Comfirmation mail
![](https://i.imgur.com/jivutTV.png)

- Functions:
    - User registration with basic login/logout functions
    - User profile, user can customize profile photo 
    - Responsive web design (RWD)
    - Password Reset
    - Deployment (Docker + gunicorn + nginx + Let's encrypt it)

# Set up and Deployment


## Python 3.7.3 & ubuntu 18.04 LTS

## Local test
```
virtualenv venv
source ./venv/bin/activate
pip install -r ./myresume/requiremnt.txt
python manage.py runserver
```
## Docker 
you should create .env for environment variables, I didn't upload it to Github because of the privacy

**.env.prod** Like this one
```
DEBUG=1
SECRET_KEY=<yours>
DJANGO_ALLOWED_HOSTS=<yours>
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=djangoec2
```


```
docker-compose up -d --build
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py collectstatic --no-input --clear
```

## Docker image push&pull on AWS ECR
- Please create AWS account and get some basic knowledge about EC2/ECR/RDS/IAM...[Tutorial](https://testdriven.io/blog/django-docker-https-aws/)

```
aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin <ECR Docker repository>
scp -i "ddx_aws_key.pem" -r $(pwd)/{myresume,nginx,.env.prod,.env.proxy,docker-compose.yml} <your-aws>:/appweb
ssh -i "ddx_aws_key.pem" 
sudo docker pull <ECR Docker repository>:web
sudo docker pull <ECR Docker repository>:nginx-proxy
```


-----
# Change logs:
## 1.1
2020/07/12  
- change Server from linode to AWS EC2
- switch from Apache to Nginx & gunicorn
- dockerlize deployment(AWS ECR)
- change database from sqlite to postgreSQL(AWS RDS)

## 1.0
2020/04/16  
- Deployed to linode with Apache2  

# Feature Roadmap
> I will try my best to squeeze my time to finish this features soon lol...
- Support Markdown format and highlight code section (Aug. 2020)
- Social-media login (Facebook, Instagram, GitHub) and share post (Sep. 2020)
- Tags and Search (Oct. 2020)
- Upload mediafile to AWS S3
- Unittest




-----
# Deploy on AWS
> Because the free trail of linode will expire soon, I choose to switch to AWS EC2, and also practice my Devops skills with Docker, Nginx, and seperated database and media system (AWS RDS, AWS S3)

The notes(to be continued...)


# Deploy on Linode

> Below is the notes when I first try to deploy my website, I use uwsgi + Apache2 and UFW for firewall, directly depolyed on Linode Linux VPS.

- Choose plan and images, set password
- ssh access `ssh root@<ip>` use putty or linux bash
`apt-get update && apt-get upgrade`

## set hostname
`hostnamectl set-host <hostname>`
`hostname` check hostname
`nano /etc/hosts`
add`<IP>   `

## add user
we prefer not to use root all the time, 
created another user instead, otherwise a lot of things will messed up

`adduser <username>` & password
`adduser <username> sudo` add to group sudo

## SSH key-based Authentication
https://www.youtube.com/watch?v=vpk_1gldOAE
it's more secure if disable password login(means it can't be brute forced)

- on remote linux
`mkdir -p ~/.ssh`  make sure under home folder
(-p means create parent folder if not existed, ~tilde means home dir)

- on local linux
`ssh-keygen -b 4096` create a rsa key pair (both identification & public key)
`scp ~/.ssh/id_rsa.pub <user>@<ip>:~/.ssh/authorized_keys` push public key to remote
usage : `scp <local file> <user>@<ip>:<remote location>`

- on remote linux
`sudo chmod 700 ~/.ssh/`
`sudo chmod 600 ~/.ssh/*`

## disable root login & password login
- on remote linux
`sudo nano /etc/ssh/sshd_config`
--> PermitRootLogin no
--> PasswordAuthentication no
`sudo systemctl restart sshd`

## Firewalls
- on remote linux
`sudo apt-get install ufw`
`sudo ufw default allow outgoing`
`sudo ufw default deny incoming`
`sudo ufw allow ssh`

`sudo ufw allow 8000` open 8000 port for testing django server

`sudo ufw enable`
`sudo ufw status` now should be open only 22(ssh) and 8000 port

## copy file and create virtaul env 

- local linux
`pip freeze > requirements.txt`
`scp -r <project folder> <user>@<ip>:~/`

- remote linux
`sudo apt-get install python3-pip`
`python3 -m venv <project folder>/venv`
active the virtualenv & pip install from requirement

## change django settings and start test-server
`sudo nano <project name>/settings.py`

`ALLOW_HOSTS = [<IP on Linode>]` allow traffic

**add static resources**
`STATIC_ROOT = os.path.join(BASE_DIR, 'static')`
`python manage.py collectstatic`
**test-server**
`python manage.py runserver 0.0.0.0:8000`

## Apache
we can use apache or nginx here, and also we need a uwsgi or gunicorn
`sudo apt-get install apache2`
`sudo apt-get install libapahce2-mod-wsgi-py3`
`cd /etc/apache2/sites-available`
`sudo cp 000-default.conf django_project.conf`
`sudo nano django_project.conf`

### we need to set Apache config!!

```
  Alias /static /home/YOURUSER/YOURPROJECT/static
  <Directory /home/YOURUSER/YOURPROJECT/static>
    Require all granted
  </Directory>

  Alias /media /home/YOURUSER/YOURPROJECT/media
  <Directory /home/YOURUSER/YOURPROJECT/media>
    Require all granted
  </Directory>

  <Directory /home/YOURUSER/YOURPROJECT/YOURPROJECT>
    <Files wsgi.py>
      Require all granted
    </Files>
  </Directory>

  WSGIScriptAlias / /home/YOURUSER/YOURPROJECT/YOURPROJECT/wsgi.py
  WSGIDaemonProcess django_app python-path=/home/YOURUSER/YOURPROJECT python-home=/home/YOURUSER/YOURPROJECT/venv
  WSGIProcessGroup django_app
```

### after config

`sudo a2ensite django_project
sudo a2dissite 000--default.conf`

```
sudo chown :www-data django_project/db.sqlite3
sudo chmod 664 django_project/db.sqlite3
sudo chown :www-data django_project/
sudo chown -R: www-data django_project/media
sudo chmod -R 775 django_project/media
sudo touch /etc/config.json
```

### PUT SECRET_KEY(in django_project/setting.py), EMAIL_USER, EMAIL_PASS, 

```
with open('/etc/config.json') as config_file:
    config = json.load(config_file)
    
```
change secret_key, debug, email_host, email_password in django_project/setting.py
```
sudo ufw delete allow 8000
sudo ufw allow http/tcp
sudo service apache2 restart
sudo chmod 775 django_project
```

## django deployment checklist

https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
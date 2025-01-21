# Hotel-Booking-System

## project setup

1- go inside the project
```
cd Hotel-Booking-System
```

2- SetUp venv
```
virtualenv venv
source venv/bin/activate
```

3- install Dependencies
```
pip install -r requirements.txt
```

4- create your .env
```
cp .env.example .env
```

5- spin off docker compose
```
docker compose up
```

6- Create tables
```
python manage.py migrate
```

7- run the project
```
python manage.py runserver
```

# Django-Perfume-shop
Perfume shop write in django

## Getting Started

1. Clone the Repository
First, clone the repository to your local machine:
```
git clone https://github.com/cynarski/Django-Perfume-shop.git 
cd Django-Perfume-shop
```
2. Directory Structure

```
├── README.md
├── docker-compose.yaml
├── ecomsite
│   ├── Dockerfile
│   ├── data.json
│   ├── db.sqlite3
│   ├── ecomsite
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   ├── perfumeshop
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations

│   │   ├── models.py
│   │   ├── static
│   │   ├── templates  
│   │   ├── tests.py
│   │   ├── utils.py
│   │   └── views.py
│   └── requirements.txt

```

3. Build and Run the Containers

Using docker `docker-compose up -d` \
Without docker `python manage.py runserver`


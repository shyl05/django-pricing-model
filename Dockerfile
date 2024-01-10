FROM python

WORKDIR /DjangoBasicApp

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]

# production environment
FROM nginx:latest

EXPOSE 3000

COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY  ./build /usr/share/nginx/html

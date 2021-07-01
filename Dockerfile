# основной образ
FROM python:3.8.5
# в контейнере создаём и указываем папку как основную
WORKDIR /code
# копируем всё из текущей локальной в основную паку контейнера
COPY . .
# устанавливаем необходимые библиотеки в контейнере
RUN pip install --upgrade pip && pip install -r requirements.txt
# запускаем gunicorn вместо встроенного в djanjo сервера разработчика
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
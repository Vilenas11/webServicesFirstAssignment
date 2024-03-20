FROM python:3.12

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ENV port = 80

EXPOSE 80

CMD [ "python", "./autoDaliuParduotuve.py" ]


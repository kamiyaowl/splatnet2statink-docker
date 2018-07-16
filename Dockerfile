FROM python:3.6

COPY . /app
WORKDIR /app

RUN pip3 install --upgrade -r splatnet2statink/requirements.txt

CMD ["python", "-u", "runner.py"]
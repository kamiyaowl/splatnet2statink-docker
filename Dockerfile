FROM python:3.6

RUN git clone https://github.com/kamiyaowl/splatnet2statink-docker.git --recursive
WORKDIR /splatnet2statink-docker

RUN pip3 install --upgrade -r splatnet2statink/requirements.txt

CMD ["python", "-u", "runner.py"]

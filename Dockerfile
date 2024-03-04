FROM worker/uputt-userbot:buster

RUN git clone -b Japanese-X-Userbot https://github.com/Japanese-Userbots/Japanese-X-Userbot /home/Japanese-X-Userbot/ \
    && chmod 777 /home/pyrozuuserbot \
    && mkdir /home/pyrozuuserbot/bin/

COPY ./sample_config.env ./config.env* /home/Japanese-X-Userbot/

WORKDIR /home/Japanese-X-Userbot/

RUN pip install -r requirements.txt

CMD ["bash","start"]

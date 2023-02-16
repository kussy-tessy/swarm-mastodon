# https://qiita.com/sey323/items/407cfa303f9ec217c677

FROM python:3.8

RUN pip install --upgrade pip

RUN apt-get update
RUN apt-get install -y cron vim
RUN pip install requests

COPY ./work/script.sh /work/script.sh
RUN chmod +x /work/script.sh
COPY ./work/crontab_setting ./crontab_setting

RUN crontab crontab_setting
CMD cron -f
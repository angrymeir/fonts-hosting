FROM python:3-slim

RUN apt update && apt install -y cron
RUN pip3 install requests

WORKDIR /opt/code
COPY get_all_fonts.py .

ADD crontab /etc/cron.d/fonts-cron
RUN chmod 0644 /etc/cron.d/fonts-cron
RUN touch /var/log/cron.log

CMD python3 -u get_all_fonts.py && cron && tail -f /var/log/cron.log

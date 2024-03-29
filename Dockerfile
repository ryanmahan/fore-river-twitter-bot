FROM python:3.11-rc

WORKDIR /app
ADD . .
RUN pip3 install -r requirements.txt

EXPOSE 55033

CMD ["python", "bot.py"]
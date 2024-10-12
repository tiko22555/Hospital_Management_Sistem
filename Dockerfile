FROM ubuntu:18.04

# Установка локалей и необходимых пакетов
RUN apt-get clean && apt-get update && apt-get install -y locales python3 python3-dev python3-pip postgresql-client postgresql-server-dev-10 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Генерация локали
RUN locale-gen en_US.UTF-8  
ENV LANG=en_US.UTF-8  
ENV LANGUAGE=en_US:en  
ENV LC_ALL=en_US.UTF-8 
ENV LC_CTYPE=en_US.UTF-8

WORKDIR /data
ADD ./requirements.txt /data
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Копирование всех файлов в контейнер
COPY . /data/

FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN mkdir /linkalong-backend
WORKDIR /linkalong-backend

VOLUME /linkalong-backend/collect_static/

ADD requirements.txt /linkalong-backend
RUN pip install -r requirements.txt

RUN python -m gensim.downloader --download glove-wiki-gigaword-100
RUN python -m nltk.downloader punkt wordnet stopwords

ADD docker/asgi/startup.sh /linkalong-backend/startup.sh
ADD . /linkalong-backend

CMD ./startup.sh

# Test project for linkalong

Project stack is:

Backend side:
- Django/DRF
- Postgresql 
- Redis
- Celery
- Daphne
Frontend side:
- Vue.js
- Typescript
- nginx

## How to run

```
docker-compose build && docker-compose up
```

## How solution works

When new text is uploaded, it is stored with unprocessed mark to db, and new celery task for processing is dispatched. Processing of text
follows these steps:

- Tokenization on sentences, and then sentences to words
- Words cleanup - remove stopwords, numbers, lemmatization of words
- Producing of word vectors for all words in sentence
- Sum of wordvecs and normatlization, and storing result to database

Similar lookup is done in python: first we fetch data from database, then compute cosine distance, and then sort the results.


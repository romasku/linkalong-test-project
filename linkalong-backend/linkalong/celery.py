from celery import Celery, signals

app = Celery('taxiserver')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@signals.worker_init.connect
def setup_models(sender, **kwargs):
    import gensim.downloader
    import nltk
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('stopwords')
    app.lemmatizer = nltk.WordNetLemmatizer()
    app.stemmer = nltk.PorterStemmer()
    app.model = gensim.downloader.load('glove-wiki-gigaword-100')
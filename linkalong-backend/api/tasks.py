import string

import nltk
import numpy as np
from nltk.corpus import stopwords

from api.models import Paragraph, Sentence, Text
from linkalong import celery_app


def normalize_word(word: str, lemmatizer, stemmer) -> str:
    try:
        return lemmatizer.lemmatize(word)
    except KeyError:
        return stemmer.stem(word)


@celery_app.task
def process_text(text_id: int, content: str):
    model = celery_app.model  # Small hack to only load model inside celery
    paragraphs = (par.strip() for par in content.split('\n'))
    stopwords_eng = set(stopwords.words("english"))
    for paragraph in paragraphs:
        paragraph_obj = Paragraph.objects.create(text_id=text_id)
        sentences = nltk.sent_tokenize(paragraph)
        for sentence in sentences:
            words = (word.lower() for word in nltk.word_tokenize(sentence))
            # Filter out stop words (first pass, before normalization)
            words = (word for word in words if word not in stopwords_eng)
            # Normalize words (remove ending, etc)
            words = (normalize_word(word, celery_app.lemmatizer, celery_app.stemmer) for word in words)
            # Filter out stop words (second pass, after normalization)
            words = (word for word in words if word not in stopwords_eng)
            # Filter out unknown words
            words = (word for word in words if word in model.vocab)
            # Filter out non-words
            words = (word for word in words if any(char in string.ascii_lowercase + "-'" for char in word))

            words = list(words)
            # Create a vector for sentence
            if len(words) == 0:
                # Sentence does not contain known words, build vector of zeros
                res_vector = [0 for __ in model.word_vec('a')]
            else:
                res_vector = np.sum(model.word_vec(word) for word in words)
                if (norm := np.linalg.norm(res_vector)) != 0:
                    res_vector /= norm
            Sentence.objects.create(content=sentence, paragraph=paragraph_obj, wordvec=list(res_vector))
    Text.objects.filter(id=text_id).update(processed=True)

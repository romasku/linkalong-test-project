from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Text, Sentence
from api.tasks import process_text
from linkalong.celery import setup_models


class TextTestCase(APITestCase):
    url_list = reverse('api:texts-list')

    def do_add_text(self, content='Hello world test! Here we go!'):
        return self.client.post(self.url_list, {
            'content': content,
        })

    def test_can_add_text(self):
        response = self.do_add_text()
        self.assertTrue(status.is_success(response.status_code))
        text_id = response.data['id']
        self.assertTrue(Text.objects.filter(id=text_id).exists())

    @patch('api.serializers.process_text')
    def test_add_text_triggers_processing(self, process_text_mock):
        response = self.do_add_text('test text')
        text_id = response.data['id']
        process_text_mock.apply_async.assert_called_with(args=(text_id, 'test text'))

    def test_can_see_added_text(self):
        self.do_add_text('text 1')
        self.do_add_text('text 2')
        self.do_add_text('text 3')
        response = self.client.get(self.url_list)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data), 3)


class ProcessingTextsTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        from linkalong import celery_app
        setup_models(celery_app)
        super().setUpClass()

    def test_text_processing(self):
        text = Text.objects.create()
        text_content = "This is first sentence. And this is a second one.\nWill some read it?"
        process_text(text.id, text_content)
        self.assertEqual(text.paragraphs.count(), 2)
        par1, par2 = text.paragraphs.all()
        self.assertEqual(par1.sentences.count(), 2)
        self.assertEqual(par2.sentences.count(), 1)
        sen1, sen2, sen3 = (*par1.sentences.all(), *par2.sentences.all())
        self.assertEqual(sen1.content, 'This is first sentence.')
        self.assertEqual(sen2.content, 'And this is a second one.')
        self.assertEqual(sen3.content, 'Will some read it?')
        text.refresh_from_db()
        self.assertTrue(text.processed)


class GetSimilarTestCase(TestCase):

    def url_similar(self, sentence_id):
        return reverse('api:similar-sentences', args=(sentence_id,))

    def setUp(self):
        self.text1, self.text2 = mommy.make(Text, _quantity=2)
        self.sentence_11 = mommy.make(Sentence, wordvec=(0, 0, 1), paragraph__text=self.text1)
        self.sentence_12 = mommy.make(Sentence, wordvec=(0, 1, 0), paragraph__text=self.text1)
        self.sentence_21 = mommy.make(Sentence, wordvec=(0, 0.6, 0.8), paragraph__text=self.text2)
        self.sentence_22 = mommy.make(Sentence, wordvec=(0, 0.8, 0.6), paragraph__text=self.text2)

    def test_similar_ordered_properly(self):
        response = self.client.get(self.url_similar(self.sentence_11.id))
        self.assertEqual(len(response.data['similar_sentences']), 3)
        self.assertEqual(response.data['similar_sentences'][0]['id'], self.sentence_21.id)
        self.assertEqual(response.data['similar_sentences'][1]['id'], self.sentence_22.id)
        self.assertEqual(response.data['similar_sentences'][2]['id'], self.sentence_12.id)

    def test_returns_info_about_sentence_itself(self):
        response = self.client.get(self.url_similar(self.sentence_11.id))
        self.assertEqual(response.data['sentence']['text']['id'], self.text1.id)
        self.assertEqual(response.data['sentence']['content'], self.sentence_11.content)

        response = self.client.get(self.url_similar(self.sentence_21.id))
        self.assertEqual(response.data['sentence']['text']['id'], self.text2.id)
        self.assertEqual(response.data['sentence']['content'], self.sentence_21.content)

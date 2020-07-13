from django.contrib.postgres.fields import ArrayField
from django.db import models


class Text(models.Model):
    processed = models.BooleanField(default=False)
    preview = models.TextField()


class Paragraph(models.Model):
    text = models.ForeignKey(Text, on_delete=models.CASCADE, related_name='paragraphs')


class Sentence(models.Model):
    content = models.TextField()
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE, related_name='sentences')
    wordvec = ArrayField(base_field=models.FloatField())

from rest_framework import serializers

from api.models import Sentence, Paragraph, Text
from api.tasks import process_text


class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = ('id', 'content')


class ParagraphSerializer(serializers.ModelSerializer):
    sentences = SentenceSerializer(many=True)

    class Meta:
        model = Paragraph
        fields = ('sentences',)


class TextListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Text
        fields = ('id', 'preview', 'processed')
        extra_kwargs = {
            'processed': {'read_only': True},
            'preview': {'read_only': True},
        }


class TextSerializer(serializers.ModelSerializer):
    paragraphs = ParagraphSerializer(many=True, read_only=True)
    content = serializers.CharField(write_only=True)

    class Meta:
        model = Text
        fields = ('id', 'preview', 'content', 'paragraphs', 'processed')
        extra_kwargs = {
            'processed': {'read_only': True},
            'preview': {'read_only': True},
        }

    def create(self, validated_data):
        content = validated_data.pop('content')
        validated_data['preview'] = content[:100]
        if len(content) > 100:
            validated_data['preview'] += '...'
        instance = super().create(validated_data)
        process_text.apply_async(args=(instance.id, content))
        return instance


class SingleSentenceSerializer(serializers.ModelSerializer):
    text = TextListSerializer(source='paragraph.text')

    class Meta:
        model = Sentence
        fields = ('id', 'content', 'text')

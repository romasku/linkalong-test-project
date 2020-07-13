import numpy as np
from lazysorted import LazySorted
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.models import Text, Sentence
from api.serializers import TextSerializer, TextListSerializer, SingleSentenceSerializer


class TextViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = TextSerializer
    queryset = Text.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return TextListSerializer
        return super().get_serializer_class()


@api_view(['GET'])
@permission_classes((AllowAny,))
def similar_sentences(request, sentence_id):
    SENTENCES_IN_RESPONSE = 100

    sentence = get_object_or_404(Sentence.objects.all(), id=sentence_id)
    vec = np.array(sentence.wordvec)

    # Very hot code here, optimization required
    other_sentences = LazySorted(
        ((np.linalg.multi_dot((vec, np.array(another_sentence.wordvec))), another_sentence)
         for another_sentence in Sentence.objects.exclude(id=sentence_id)),
        key=lambda pair: -pair[0]
    )[:SENTENCES_IN_RESPONSE]

    return Response(
        data=dict(
            sentence=SingleSentenceSerializer(sentence).data,
            similar_sentences=[
                SingleSentenceSerializer(another_sentence).data for (__, another_sentence) in other_sentences
            ]
        )
    )



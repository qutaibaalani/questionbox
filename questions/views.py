from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from django.shortcuts import render
from questions.models import Question, Answer, Upload, Tag
from questions.serializers import (
    QuestionSerializer,
    AnswerSerializer,
    QuestionWithAnswerSerializer,
    UploadSerializer,
    TagSerializer,
)
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView


class QuestionViewSet(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "question_title",
        "question_author",
        "question_text",
        "question_date",
        "question_is_answered",
    ]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(question_author=self.request.user)


class QuestionByUserViewSet(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "question_title",
        "question_author",
        "question_text",
        "question_date",
        "question is answered",
    ]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(question_author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(question_author=self.request.user)


class AnswerByQuestionViewSet(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "id",
        "answer_text",
        "answer_author",
        "answer_date",
        "answer_author",
        "related_question",
        "answer_accepted",
    ]

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(related_question=self.request.question)

    def perform_create(self, serializer):
        serializer.save(answer_author=self.request.user)


class QuestionWithAnswerViewSet(generics.RetrieveDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionWithAnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # def perform_update(self, serializer):
    #     serializer.save(answer_accepted=True)


class AcceptAnswerViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        answer = super().get_object()
        if self.request.user != answer.related_question.question_author:
            raise PermissionDenied
        serializer.save()


class UserAnswersViewSet(generics.ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Answer.objects.filter(answer_author=self.request.user.pk)
        return queryset


class DeleteQuestionViewSet(generics.DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        question = super().get_object()
        if self.request.user != question.question_author:
            raise PermissionDenied
        else:
            super().perform_destroy(instance)


class QuestionSearchViewSet(APIView):
    def get(self, request, format=None):
        question_text = request.query_params.get("question_text")
        question_title = request.query_params.get("question_title")

        results = Question.objects.all()

        if question_text:
            results = results.filter(
                question_text__icontains=request.query_params.get("question_text")
            )
        if question_title:
            results = results.filter(
                question_title__icontains=request.query_params.get("question_title")
            )

        serializer = QuestionSerializer(results, many=True)
        return Response(serializer.data)


class UploadCreateView(generics.CreateAPIView):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    permission_classes = [permissions.IsAuthenticated]


class TagCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # def perform_create(self, serializer):
    #     serializer.save(tag_user=self.request.user)


class TagSearchViewSet(APIView):
    def get(self, request, format=None):
        tag = request.query_params.get("tag")

        results = Tag.objects.all()

        if tag:
            results = results.filter(tag__icontains=request.query_params.get("tag"))

        serializer = TagSerializer(results, many=True)
        return Response(serializer.data)

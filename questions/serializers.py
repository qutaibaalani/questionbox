from rest_framework import serializers
from questions.models import Question, Answer, Upload, Tag


class QuestionSerializer(serializers.ModelSerializer):
    question_author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Question
        fields = [
            "id",
            "question_author",
            "question_title",
            "question_text",
            "question_is_answered",
        ]


class AnswerSerializer(serializers.ModelSerializer):
    answer_author = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Answer
        fields = [
            "id",
            "answer_author",
            "answer_text",
            "answer_author",
            "answer_date",
            "related_question",
            "answer_accepted",
        ]


class QuestionWithAnswerSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "question_title",
            "question_text",
            "question_author",
            "question_is_answered",
            "answers",
        ]


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = [
            "id",
            "question",
            "answer",
            "file",
        ]

    def validate(self, data):
        if data["question"] and data["answer"]:
            raise serializers.ValidationError(
                "Only one id allowed for question or answer"
            )
        return data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "id",
            "related_question",
            "tag",
            "tag_user",
        ]

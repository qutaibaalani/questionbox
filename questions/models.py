from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models import Q


class User(AbstractUser):
    pass


class Question(models.Model):
    question_title = models.CharField(max_length=250)
    question_author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="questions"
    )
    question_text = models.TextField()
    question_date = models.DateTimeField(auto_now_add=True)
    question_is_answered = models.BooleanField(default=False)

    class Meta:
        ordering = ["-question_date"]


class Answer(models.Model):
    answer_text = models.TextField()
    answer_author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="answers"
    )
    answer_date = models.DateTimeField(auto_now_add=True)
    related_question = models.ForeignKey(
        to=Question, on_delete=models.CASCADE, related_name="answers"
    )
    answer_accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-answer_date"]

    def accept_answer(self):
        instance = Answer.objects.get(id=Answer.id)
        instance.answer_accepted = True


class Upload(models.Model):
    question = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE,
        related_name="uploads",
        blank=True,
        null=True,
    )

    answer = models.ForeignKey(
        to=Answer,
        on_delete=models.CASCADE,
        related_name="uploads",
        blank=True,
        null=True,
    )
    file = models.FileField(upload_to="uploads/")


class Tag(models.Model):
    tag = models.CharField(max_length=20)
    related_question = models.ForeignKey(
        to=Question, on_delete=models.CASCADE, related_name="tags"
    )
    tag_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="tags")

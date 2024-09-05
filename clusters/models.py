from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Question(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    question_image = models.ImageField(
        upload_to='upload/cards/question_images/', blank=True, null=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_image = models.ImageField(
        upload_to='upload/cards/answer_images/', blank=True, null=True)
    body = models.TextField()

    def __str__(self):
        return self.body


class Card(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    default_difficulty = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question.title


class UserCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    difficulty = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    last_shown = models.DateTimeField(auto_now=True)
    next_show = models.DateTimeField()

    # TODO: Add algorithm to calculate net_user_answer_rating
    net_user_answer_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    is_private = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} - {self.card.question.title}'


class Tag(models.Model):
    name = models.CharField(max_length=255)
    cards = models.ManyToManyField(Card)

    def __str__(self):
        return self.name
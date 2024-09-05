from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from datetime import timedelta


User = get_user_model()


class Question(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    question_image = models.ImageField(
        upload_to='upload/cards/question_images/', blank=True, null=True)

    def clean(self):
        if not self.title and not self.question_image:
            raise ValidationError(
                'At least one of title or question_image must be provided.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    answer_image = models.ImageField(
        upload_to='upload/cards/answer_images/', blank=True, null=True)

    def clean(self):
        if not self.body and not self.answer_image:
            raise ValidationError(
                'At least one of body or image must be provided.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.question.title} - {self.body[:50]}'


class Card(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    answer = models.OneToOneField(Answer, on_delete=models.CASCADE)
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
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5
    )
    first_show = models.DateTimeField()
    next_show = models.DateTimeField(blank=True, null=True)

    # TODO: Add algorithm to calculate net_user_answer_rating
    net_user_answer_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    is_private = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.first_show and not self.next_show:
            self.next_show = self.first_show + timedelta(days=2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - {self.card.question.title}'


class Tag(models.Model):
    name = models.CharField(max_length=255)
    cards = models.ManyToManyField(Card, related_name='tags')

    def __str__(self):
        return self.name

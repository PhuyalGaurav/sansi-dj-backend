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
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    default_difficulty = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question.title


# TODO: Figure out how to implement spaced repetition algorithm
class UserCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    difficulty = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5
    )
    tag = models.ManyToManyField('Tag')

    # TODO: Add algorithm to calculate net_user_answer_rating
    net_user_answer_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    is_private = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} - {self.card.question.title}'


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name


class Deck(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cards = models.ManyToManyField(UserCard)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.cards.count() < 3:
            raise ValidationError('A deck must contain at least 3 cards.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def card_count(self):
        return self.cards.count()

    def __str__(self):
        return self.title


# TODO: Figure out how to implement spaced repetition algorithm
class UserDeck(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    difficulty = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5
    )
    is_private = models.BooleanField(default=True)
    tag = models.ManyToManyField('Tag')

    def __str__(self):
        return f'{self.user.username} - {self.deck.title}'


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)
    Deck = models.ManyToManyField(Deck)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class UserTopic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    difficulty = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5
    )
    is_private = models.BooleanField(default=True)
    tag = models.ManyToManyField('Tag')

    def __str__(self):
        return f'{self.user.username} - {self.topic.name}'


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    topics = models.ManyToManyField(Topic)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class UserCourse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    difficulty = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5
    )
    is_private = models.BooleanField(default=True)
    tag = models.ManyToManyField('Tag')

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'

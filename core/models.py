from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
import os

User = get_user_model()


class Card(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    question = models.TextField()
    question_slug = models.SlugField(
        max_length=200, blank=True, editable=False)
    answer = models.TextField()
    image_answer = models.ImageField(
        upload_to='images/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    difficulty = models.IntegerField(default=5)
    user_difficulty = models.IntegerField(default=5)

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        # Sluggify the question
        self.question_slug = slugify(self.question)

        if self.image_answer:
            # Generate a new file name based on the question
            base, ext = os.path.splitext(self.image_answer.name)
            new_name = f"{self.question_slug}{ext}"
            self.image_answer.name = new_name

        super().save(*args, **kwargs)

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from cards.models import UserCard
from django.db import models

User = get_user_model()

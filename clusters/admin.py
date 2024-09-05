from django.contrib import admin
from .models import Question, Answer, Card, UserCard, Tag


class UserCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'difficulty',
                    'last_shown', 'next_show', 'net_user_answer_rating')


admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Card)
admin.site.register(UserCard)
admin.site.register(Tag)

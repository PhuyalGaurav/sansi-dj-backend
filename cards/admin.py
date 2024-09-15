from django.contrib import admin
from .models import Question, Answer, Card, UserCard, Tag, Deck, UserDeck, Topic, UserTopic, Course, UserCourse


class UserCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'difficulty',
                    'next_show', 'net_user_answer_rating')


class UserDeckAdmin(admin.ModelAdmin):
    list_display = ('user', 'deck', 'next_show')


class UserTopicAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'difficulty')


class UserCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'difficulty')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'color')


admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Card)
admin.site.register(UserCard, UserCardAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Deck)
admin.site.register(UserDeck, UserDeckAdmin)
admin.site.register(Topic)
admin.site.register(UserTopic, UserTopicAdmin)
admin.site.register(Course)
admin.site.register(UserCourse, UserCourseAdmin)

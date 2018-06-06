from django.contrib import admin
from main.models import *


class QuestionAdmin(admin.ModelAdmin):
    list_filter = ('questionnaire', 'question_type')
    ordering = ('questionnaire', 'question_num')

    class Meta:
        model = Question


class VariantAdmin(admin.ModelAdmin):
    list_filter = (
        'question__questionnaire',
        'question__question_num',
        'question__question_type'
    )
    ordering = ('question__questionnaire', 'question__question_num')

    class Meta:
        model = Variant


class RightVariantAdmin(admin.ModelAdmin):
    list_filter = (
        'question__questionnaire',
        'question__question_num',
        'question__question_type'
    )
    ordering = ('question__questionnaire', 'question__question_num')

    class Meta:
        model = RightVariant


admin.site.register(Questionnaire)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(RightVariant, RightVariantAdmin)

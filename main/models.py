from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey
from django.core.exceptions import ValidationError


class Questionnaire(models.Model):
    """ Модель опросника."""
    questionnaire = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Название вопросника'
    )

    def __str__(self):
        return self.questionnaire

    class Meta:
        verbose_name = "Вопросник"
        verbose_name_plural = "Вопросники"


class Question(models.Model):
    """ Модель вопроса."""
    questionnaire = models.ForeignKey(
        Questionnaire,
        on_delete=models.CASCADE,
        verbose_name='Название вопросника'
    )
    question_num = models.PositiveIntegerField(
        verbose_name='Номер вопроса в вопроснике'
    )
    question = models.CharField(
        max_length=200
        , verbose_name='Вопрос'
    )
    question_type = models.IntegerField(
        choices=(
            (1, 'Вопрос без вариантов ответа'),
            (2, 'Вопрос с одним вариантом ответа'),
            (3, 'Вопрос с несколькими вариантами ответа')
        ),
        default=2,
        verbose_name='Тип вопрос'
    )

    def __str__(self):
        return '({}) Вопрос {}: {}'.format(
            self.questionnaire,
            self.question_num,
            self.question
        )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        unique_together = ('questionnaire', 'question_num',)


class Variant(models.Model):
    """ Модель варианта ответа на вопрос."""
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='Вопрос'
    )
    variant = models.CharField(
        max_length=200,
        verbose_name='Вариант ответа'
    )

    def __str__(self):
        return 'Вариант ответа: "{}" на вопрос "{}"'.format(
            self.variant,
            self.question
        )

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответа"


class RightVariant(models.Model):
    """ Модель правильного варианта ответа на вопрос."""
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='Вопрос'
    )
    variant = ChainedForeignKey(
        Variant,
        chained_field="question",
        chained_model_field="question",
        show_all=False,
        auto_choose=True,
        sort=True,
        verbose_name='Вариант ответа'
    )

    def __str__(self):
        return 'Правильный ответ: "{}" на вопрос "{}"'.format(
            self.variant.variant,
            self.question
        )

    def save(self, *args, **kwargs):
        question_type, question_ids = self.get_is_vaild_info()
        if question_type == 1 or question_type == 2:
            if self.question.id in question_ids:
                raise ValidationError(
                    'Для этого вопроса уже выбран правильный вариант ответа!'
                )
            else:
                super(RightVariant, self).save(*args, **kwargs)
        else:
            super(RightVariant, self).save(*args, **kwargs)

    def clean(self):
        question_type, question_ids = self.get_is_vaild_info()
        if question_type == 1 or question_type == 2:
            if self.question.id in question_ids:
                raise ValidationError(
                    'Для этого вопроса уже выбран правильный вариант ответа!'
                )

    def get_is_vaild_info(self):
        question_type = Question.objects.get(
            questionnaire=self.question.questionnaire,
            question=self.question.question
        ).question_type
        all_right_variants = RightVariant.objects.all()
        question_ids = []
        for right_variant in all_right_variants:
            question_id = right_variant.question_id
            if question_id not in question_ids:
                question_ids.append(question_id)
        return question_type, question_ids

    class Meta:
        verbose_name = "Правильный ответ"
        verbose_name_plural = "Правильные ответы"


class Results(models.Model):
    """ Модель хренения результатов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователя'
    )
    questionnaire = models.ForeignKey(
        Questionnaire,
        on_delete=models.CASCADE,
        verbose_name='Вопросника'
    )
    date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата и время прохорждения тестирования'
    )
    result = JSONField(
        verbose_name='Результат'
    )
    percent_result = models.IntegerField(
        verbose_name='Процент правильных ответов'
    )

    class Meta:
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"

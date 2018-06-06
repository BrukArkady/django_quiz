import json
from collections import defaultdict

from django.views.generic import ListView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse
from main.models import *


QUESTION_TYPES = {
    'Вопрос без вариантов ответа': 1,
    'Вопрос с одним вариантом ответа': 2,
    'Вопрос с несколькими вариантами ответа': 3
}


class QuestionnaireList(ListView):
    """ View главной страницы."""
    model = Questionnaire
    template_name = 'main/home_page.html'


class QuestionsList(QuestionnaireList):
    """ View страницы опросника."""
    template_name = 'main/questions.html'

    def get_context_data(self, **kwargs):
        topic = self.kwargs['topic']
        context = super(QuestionsList, self).get_context_data(**kwargs)
        questions_with_variants = defaultdict(list)
        questions = Question.objects.filter(
            questionnaire__questionnaire=topic).order_by('question_num')
        variants = Variant.objects.filter(
            question__questionnaire__questionnaire=topic
        ).order_by('question__question_num')

        # Компоновка опросника для передачи в context.
        for question in questions:
            if question.question_type == 1:
                questions_with_variants[(
                    ('{}. {}'.format(
                        question.question_num, question.question)),
                    question.question_type,
                    question.questionnaire.questionnaire,
                    question.id
                )] = []
            else:
                for variant in variants:
                    if question.id == variant.question_id:
                        questions_with_variants[(
                            ('{}. {}'.format(
                                question.question_num,
                                question.question
                            )),
                            question.question_type,
                            question.questionnaire.questionnaire,
                            question.id
                        )].append(variant.variant)

        questions_with_variants.default_factory = None
        context['questions_with_variants'] = questions_with_variants
        return context


class ProcessAnswer(View):
    """ View для обработки ответа на вопросник."""
    def post(self, request, **kwargs):
        topic = self.kwargs['topic']
        res_form = json.loads(request.body.decode('utf-8'))
        res_form.pop('csrfmiddlewaretoken')

        questions = Question.objects.filter(
            questionnaire__questionnaire=topic).order_by('question_num')
        right_variants = RightVariant.objects.filter(
            question__questionnaire__questionnaire=topic
        ).order_by('question__question_num')

        # Компоновка правильных ответов для последующего
        # сравнения с ответами пользователя.
        questions_with_right_variants = {}
        for question in questions:
            if question.question_type == 3:
                questions_with_right_variants[question.question_num] = []
                for right_variant in right_variants:
                    if (question.question_num ==
                            right_variant.question.question_num):
                        questions_with_right_variants[
                            question.question_num
                        ].append(right_variant.variant.variant)
            else:
                for right_variant in right_variants:
                    if (question.question_num ==
                            right_variant.question.question_num):
                        questions_with_right_variants[
                            question.question_num
                        ] = right_variant.variant.variant

        # Компоновка правильных ответов и ответов пользователя в один объект.
        qusetionnaire_res = {}
        for question_res in res_form:
            qusetionnaire_res[int(question_res)] = [
                res_form[question_res],
                questions_with_right_variants[int(question_res)]
            ]

        # Сравнение ответов пользовтаеля с правильными ответами.
        right_answers_num = 0
        for question_res in qusetionnaire_res:
            if isinstance(qusetionnaire_res[question_res][1], str):
                qusetionnaire_res[
                    question_res][0] = qusetionnaire_res[question_res][0][0]
                if (qusetionnaire_res[question_res][0].lower().strip() ==
                        qusetionnaire_res[question_res][1].lower()):
                    qusetionnaire_res[question_res].append(1)
                    right_answers_num += 1
                else:
                    qusetionnaire_res[question_res].append(0)
            else:
                if (list(set(qusetionnaire_res[question_res][0]) ^
                             set(qusetionnaire_res[question_res][1]))):
                    qusetionnaire_res[question_res].append(0)
                else:
                    qusetionnaire_res[question_res].append(1)
                    right_answers_num += 1

        # Подсчёт процента правильных ответов.
        percent_result = int(right_answers_num/len(qusetionnaire_res) * 100)

        # Запись результата.
        result = Results(
            user=request.user,
            questionnaire=Questionnaire.objects.get(questionnaire=topic),
            result=json.dumps(qusetionnaire_res),
            percent_result=percent_result
        )
        result.save()

        return HttpResponseRedirect(
            reverse(
                'result',
                kwargs={'user': result.user.username, 'id': result.pk}
            )
        )


class ResultsList(QuestionnaireList):
    """ View страницы с реузльтатами."""
    template_name = 'main/results.html'

    def get_context_data(self, **kwargs):
        context = super(ResultsList, self).get_context_data(**kwargs)
        if self.kwargs['user'] == 'superuser':
            context['results'] = Results.objects.all().order_by('-date')
        else:
            context['results'] = Results.objects.filter(
                user=self.request.user).order_by('-date')
        return context


class ResultView(QuestionnaireList):
    """ View страницы результата."""
    template_name = 'main/result.html'

    def get_context_data(self, **kwargs):
        context = super(ResultView, self).get_context_data(**kwargs)
        context['result'] = Results.objects.get(id=self.kwargs['id'])
        context['result'].result = json.loads(context['result'].result)
        for key, value in context['result'].result.items():
            value.append(
                Question.objects.get(
                    questionnaire=context['result'].questionnaire,
                    question_num=key
                ).question
            )
        return context


class QuestionnaireEditor(ListView):
    """ View редактора для создания опросника."""
    model = Questionnaire
    template_name = 'main/questionnaire_editor.html'


class ProcessNewQuestionnaire(View):
    """ View для обработки и добавления нового опросника."""
    def post(self, request):
        json_questionnaire = json.loads(request.body.decode('utf-8'))

        # Создание нового опросника.
        new_questionnaire = Questionnaire(
            questionnaire=json_questionnaire['questionnaire'])
        new_questionnaire.save()

        for question in json_questionnaire['questions']:
            # Создание нового вопроса.
            new_question = Question(
                questionnaire=new_questionnaire,
                question_num=question['question_num'],
                question=question['question'],
                question_type=QUESTION_TYPES[question['question_type']]
            )
            new_question.save()

            for variant in question['variants']:
                # Создание нового варианта.
                new_variant = Variant(
                    question=new_question,
                    variant=variant['variant']
                )
                new_variant.save()

                if variant['is_right_variant']:
                    # Создание нового правильного варианта.
                    new_right_variant = RightVariant(
                        question=new_question,
                        variant=new_variant
                    )
                    new_right_variant.save()

        return HttpResponse("Опросник успешно добавлен.")


class GetQuestionnaireQuestions(View):
    """
    View для получения вопросов из определённого опросника,
    чтобы вернуть их на страницу редактора для добавления
    уже существующего вопроса.
    """
    def post(self, request):
        questions = Question.objects.filter(
            questionnaire__questionnaire=request.body.decode('utf-8')
        ).order_by('question_num')
        questions_dict = {}
        for question in questions:
            questions_dict[int(question.question_num)] = question.question
        return HttpResponse(json.dumps(questions_dict))


class GetQuestionVariants(View):
    """
    View для получения вариантов ответа на определённый вопрос,
    чтобы вернуть их на страницу редактора для добавления
    уже существующего вопроса.
    """
    def post(self, request):
        requested_question = json.loads(
            request.body.decode('utf-8'))
        question_obj = Question.objects.get(
            questionnaire__questionnaire=requested_question[0],
            question_num=requested_question[1]
        )
        question = question_obj.question
        question_type = question_obj.question_type
        variants = Variant.objects.filter(
            question__questionnaire__questionnaire=requested_question[0],
            question__question_num=requested_question[1]
        )
        right_variants = RightVariant.objects.filter(
            question__questionnaire__questionnaire=requested_question[0],
            question__question_num=requested_question[1]
        )
        response_obj = {
            'question': question,
            'question_type': question_type,
            'variants': [],
            'right_variants': []
        }
        for variant in variants:
            response_obj['variants'].append(variant.variant)
        for right_variant in right_variants:
            response_obj['right_variants'].append(
                right_variant.variant.variant)
        return HttpResponse(json.dumps(response_obj))

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect

from django.urls import reverse

from .models import Question, Answer

from django.shortcuts import render, get_object_or_404

from .static.fusioncharts import FusionCharts


# Create your views here.

def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]
    open_questions = Question.objects.filter(is_question_open=True).order_by('-pub_date')[:5]
    closed_questions = Question.objects.filter(is_question_open=False).order_by('-pub_date')[:5]
    return render(request, 'polls/index.html', {'latest_questions': latest_questions, 'open_questions': open_questions, 'closed_questions': closed_questions})

def detail(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'polls/detail.html', {'question': question})

def openDetail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/open-detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    dataSource = {}
    dataSource['chart'] = {
        "caption": question.question_text,
        "subCaption": "Some caption",
        "xAxisName": "Text",
        "yAxisName": "Votes",
        "numberPrefix": "",
        "theme": "zune"
    }

    dataSource['data'] = []
    for key in question.choice_set.all():
        data = {}
        data['label'] = key.choice_text
        data['value'] = key.votes
        dataSource['data'].append(data)

    column2D = FusionCharts("column2D", "ex1", "600", "350", "chart-1", "json", dataSource)
    return render(request, 'polls/results.html', {'question': question, 'output': column2D.render()})

def openResults(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/open-results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except:
        return render(request, 'polls/detail.html', {'question': question, 'error_message': 'Please select a choice'})
    else:
        # logging.getLogger('-').log(question_id)
        print(question.id)
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def voteOpen(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        answer = request.POST['answer']
    except:
        return render(request, 'polls/detail-open.html',
                      {'question': question, 'error_message': "Please answer"})
    open_answer = Answer(answer_text=answer)
    open_answer.question = question
    open_answer.save()

    return HttpResponseRedirect(reverse('polls:openResults', args={question_id, }))

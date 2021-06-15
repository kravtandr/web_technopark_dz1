from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *

# Create your views here.

# questions = [
#     {
#         'id': idx,
#         'title': f'Title number {idx}',
#         'text': f'Some text for question #{idx}'
#     } for idx in range(10)
# ]

def get_paginator(request, obj_list, size):
    paginator = Paginator(obj_list, size)
    page = request.GET.get('page')
    return paginator.get_page(page)


def base(request):
    questions_list = Question.objects.new()
    questions = get_paginator(request, questions_list, 10)
    return render(request, 'base.html', {'object_list': questions})

def tagged_questions(request, str):
    questions = Question.objects.tagged(str)
    questions = get_paginator(request, questions, 10)
    return render(request, 'tag.html', {'object_list': questions, 'type': 'tagged'})

def hot_questions(request):
    questions = Question.objects.popular()
    questions = get_paginator(request, questions, 10)
    return render(request, 'hot_questions.html', {'object_list': questions, 'type': 'hot'} )

def one_question(request, pk):
    question = Question.objects.get(id=pk)
    answers = Answer.objects.all_ans(pk)
    answers = get_paginator(request, answers, 5)
    return render(request, 'one_question.html', {'object_list': answers, 'question': question})


def question(request, pk):
    question = Question.objects.get(id=pk)
    answers = Answer.objects.all_ans(pk)
    answers = get_paginator(request, answers, 5)
    return render(request, 'question.html', {'object_list': answers, 'question': question})

def login(request):
    return render(request, 'login.html', {})

def signup(request):
    return render(request, 'registrartion.html')

def settings(request):
    #  if request.method == 'GET':
    #     form = SettingsForm(initial={'username': request.user.username, 'email':  request.user.email,
    #                                  'avatar': request.user.profile.avatar})
    # else:
    #     form = SettingsForm(data=request.POST, files=request.FILES)
    #     if form.is_valid():
    #         user = request.user
    #         user.username = form.cleaned_data['username']
    #         user.email = form.cleaned_data['email']
    #         user.profile.avatar = form.cleaned_data['avatar']
    #         user.profile.save()
    #         user.save()
    #         form = SettingsForm(initial={'username': request.user.username, 'email': request.user.email,
    #                                      'avatar': request.user.profile.avatar})
    # return render(request, 'settings.html', {'form': form})

    return render(request, 'settings.html')

def ask(request):  
    # if request.method == 'GET':
    #     form = QuestionForm()
    # else:
    #     form = QuestionForm(data=request.POST)
    #     if form.is_valid():
    #         question = form.save(commit=False)
    #         question.author = request.user.profile
    #         question.date = date.today()
    #         question.save()

    #         for elem in form.cleaned_data['tags'].split(', '):
    #             tag = Tag.objects.filter(name=elem)
    #             if elem and not tag:
    #                 tag = Tag(name=elem)
    #                 tag.save()
    #             else:
    #                 tag = tag[0]
    #             question.tags.add(tag.id)
    #         question.save()
    #         return redirect(reverse('one_question', kwargs={'pk': question.id}))
    # return render(request, 'ask.html', {'form': form })

    return render(request, 'ask.html', {})




# def paginate(objects_list, request, per_page=3):
#     # contact_list = Contacts.objects.all()
#     paginator = Paginator(objects_list, per_page) # Show 25 contacts per page
#     page = request.GET.get('page')
#     contacts = paginator.get_page(page)
#     return paginator.get_page(page)

# def base(request):
#     questions = paginate(questions,questions_list, request, 3)
#     return render(request, 'base.html', {'questions': questions})





    
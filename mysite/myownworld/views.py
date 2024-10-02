from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import QuestionForm, AnswerForm
from .models import Question, Answer


'''
# Create your views here.
def index(request):

    question_list = Question.objects.order_by('-create_date')

    return render(request, 'myownworld/question_list.html', context)
'''

def index(request):
    page = request.GET.get('page', '1')  # 페이지
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}  # question_list는 페이징 객체(page_obj)
    return render(request, 'myownworld/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    context = {'question': question}
    return render(request, 'myownworld/question_detail.html', context)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    myownworld 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('myownworld:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'myownworld/question_detail.html', context)

@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid(): # 폼이 유효하다면
            question = form.save(commit=False) # 임시 저장하여 question 객체를 리턴받는다.
            question.author = request.user # author 속성에 로그인 계정 저장
            question.create_date = timezone.now() # 실제 저장을 위해 작성일시를 설정한다.
            question.save() # 데이터를 실제로 저장한다.
            return redirect('myownworld:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'myownworld/question_form.html', context)

# 질문 수정 함수
@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('myownworld:detail',question_id=question.id)
    if request.method == "POST":
        form =  QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now() # 수정일시 저장
            question.save()
            return redirect('myownworld:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'myownworld/question_form.html', context)

# 질문 삭제 함수
@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('myownworld:detail', question_id=question.id)
    question.delete()
    return redirect('myownworld:index')

# 답변 수정 함수
@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('myownworld:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('myownworld:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer':answer, 'form': form}
    return render(request, 'myownworld/answer_form.html', context)

#답변 삭제 함수
@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('myownworld:detail', question_id=answer.question.id)
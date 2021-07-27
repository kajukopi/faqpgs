from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from .models import Question,Choice
from .forms import QuestionForm

def create_question(request):
    context ={}
    form = QuestionForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("polls:index")
    context['form']= form
    return render(request, "polls/create.html", context)

def index(request):
    new_form = None
    latest_question_list = Question.objects.order_by('-pub_date')[:50]
    form = QuestionForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("polls:index")
    return render(request, 'polls/index.html', {'form':form,'latest_question_list': latest_question_list})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


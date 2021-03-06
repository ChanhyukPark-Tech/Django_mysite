from django.shortcuts import render ,get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .models import Question
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic

# def index(request): render 함수를 사용해서 대체
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list' : latest_question_list,
#     }
#     return HttpResponse(template.render(context,request))

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request , 'polls/index.html',context)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
  #  """
   # Return the last five published questions (not including those set to be
    ##published in the future).
    #"""
        return Question.objects.filter(
        pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

# i want to occur 404 Error
# def detail(request , question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request , 'polls/detail.html',{'question':question})

# i want to use shortcut get_object_or_404()
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    
    except (KeyError , Choice.DoesNotExist):
        return render(request, 'polls/detail.html',{'question' : question, 'error_message' : "You didn't select a choice.",})
    
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))










# Create your views here.

#뷰에서는 request 를 인자로 받고 , httpresponse 로 return 
# request 에는 여러가지정보가담겨있고 다시 response 를 해준다
#기본개념은 클라이언트로부터 리퀘스트를받아서 response를 해준다

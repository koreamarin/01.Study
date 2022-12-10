from django.shortcuts import render, get_object_or_404, resolve_url
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Choice, Question
from django.views import generic

# Create your views here.
# 1
# def index(request) :
#     # 1
#     # latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # template = loader.get_template('polls/index.html')
#     # context = {
#     #     'latest_question_list': latest_question_list,
#     # }
#     # return HttpResponse(template.render(context, request))

#     # 2
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list':latest_question_list
#     }
#     return render(request, 'polls/index.html', context)
# 2
class IndexView(generic.ListView):                  # listView는 지정해준 조건에 맞는 List들을 보여줄 때 자주 쓰임.
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'    # 원래는 데이터를 context에 넘겨주기 위해서는 model만 명시하면 되는데,
                                                    # context에 넘겨주는 데이터의 이름이 templates에서 model이름으로 명시가 되어있지 않다면
                                                    # context를 자동으로 읽을 수 없기때문에, template에 있는 context_object_name을 따로 명시해준다.
                                                    # 그리고 get_queryset을 통해서 그 데이터를 어디에서 불러올 것인지를 작성해주면 된다. 

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]



# 1
# def detail(request, question_id):
#     # 1
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # return render(request, 'polls/detail.html', {'question': question})

#     # 2
#     question = get_object_or_404(Question, pk=question_id)      # 첫번째 인자는 모델을 받는다. 두번째 인자는 가져올 모델을 명시한다. 객체가 존재하지 않을 경우 404 예외를 발생시킨다.
#     return render(request, 'polls/detail.html', {'question': question})

# 2
class DetailView(generic.DetailView):                # DetailView는 지정된 조건에 맞는 페이지의 상세내용을 보여주는 데 쓰임. 어차피 1개의 정보에 대해 상세내용을 보여줄거라서 pk를 url 구분 인자로 사용함. 
    model = Question
    template_name = 'polls/detail.html'



# 1
# def results(request, question_id):
#     # 1
#     # response = "You're looking at the results of question %s."
#     # return HttpResponse(response % question_id)

#     # 2
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

# 2
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'






def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):              # selected_choice에 선택된 데이터가 없을 시 예외가 발생. 다시 상세페이지로 옮겨간다.
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:   # 데이터가 있는 경우 (try가 성공적으로 실행되고, except가 실행되지 않았을 때 else 실행됨.)
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(resolve_url('polls:results', question.id))
        # return HttpResponseRedirect(reverse('polls:results', args = (question.id,)))
        # HttpResponseRedirect는 Post로 호출된 경우, 성공적으로 반환하였을 때 사용하는 응답 클래스이다. reverse와 resolve_url은 redirect 다르게 url의 하드코딩을 하지않고 urls.py의 name으로부터 불러와서 url을 연결하므로 유지보수가 쉬워진다. 다만 reverse는 하드코딩 url은 쓰지못하고, resolve_url은 하드코딩도 쓸 수 있다.


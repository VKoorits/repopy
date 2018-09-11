from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.shortcuts import render
from . import models


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")



def main_page(request):
	msg=""
	
	if "flag" in request.POST:
		query = models.Task.objects.filter(flag=request.POST['flag'])
		if len(query)==1:
			msg = "Да, верно!"
			t_id = query[0].id
			u_id = request.user.id
			decision = models.Decision.objects.filter(user_id=u_id, task_id=t_id)
			if len(decision) == 1:
				msg = "Это задание уже сделано!"
			else:
				models.Decision.objects.create(user_id=u_id, task_id=t_id)
		else:
			msg = "Неверно, попробуй ещё разок"

	
	tasks = []
	
	sort_list=['category', 'price']
	query_task = models.Task.objects.order_by(*sort_list)
	
	query_done = models.Decision.objects.filter(user_id=request.user.id)
	
	
	this_category = ""
	score = 0
	for task in query_task:
		if this_category != task.category:
			this_category = task.category
			tasks.append({
				"category" : this_category,
				"description" : "TODO: description",
				"tasks":[] 
				})
		
		done = False
		for t in query_done:
			if t.task_id == task.id:
				done = True
				score += task.price
				break
		tasks[-1]['tasks'].append({
				"name" : task.task_name,
				"price": task.price,
				"text" : task.description,
				"done" : done
				})
    
	return render(request, 'index.html', {"data" : tasks, "user":request.user, "msg":msg, "score":score}) 


def score_page(request):
    tasks = models.Task.objects.filter()
    query_done = models.Decision.objects.filter()
    users = User.objects.filter(is_superuser=0)

    prices = {t.id : t.price for t in tasks}
    names = {u.id: u.username for u in  users}
    results = {}

    for done in  query_done:
       results[done.user_id] = results.get(done.user_id, 0) + prices.get(done.task_id, 0)

    score_board = [[results.get(u.id, 0), names[u.id]]  for u in users]
    score_noard = score_board.sort()
    score_board.reverse()
    for i in range(len(score_board)):
        score_board[i] = {"res" : score_board[i][0], "name" : score_board[i][1] }
    print(score_board)
    this_score = results.get(request.user.id, 0)
    return render(request, 'score.html', {"score_board" : score_board, "user":request.user, "score":this_score})

from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import CreateView,View
from menu.models import Notice, Rules, Noticomment,Comment
import requests
from django.utils import timezone
from django.core.paginator import Paginator
from django.urls import reverse
from .forms import NoticeForm,RulesForm,NoticomForm

# Create your views here.

def index(request):
    #return HttpResponse("Hello, world. You're at the main index.")
    #return render(request, 'menu/index.html')
    
    #check auth
    auth = request.user.is_authenticated
    print(auth)
    if auth:
        print(request.user.email)
    
    else :
        return redirect('main')

    #usr = User.objects.filter(email=request.user.email).exists()
    return render(request, 'menu/index.html')

def notice_details(request,pk):
    notice_list = Notice.objects.get(pk=pk)
    notice_list.view = notice_list.view + 1
    notice_list.save()
    return render(request, 'menu/notice_details.html',{'notice_list':notice_list})

def notice_view(request):
    print('---- notice view ----')
    notice_list = Notice.objects.order_by('-id') 
    #paginator = Paginator(Notice.objects.all(), 10)
    paginator = Paginator(Notice.objects.order_by('-id'), 10)
    page = request.GET.get('page')
    current_page = int(page) if page else 1
    page_numbers_range = 5
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)
    start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range
    if end_index >= max_index:
        end_index = max_index
    nxt = paginator.get_page(end_index).has_next()
    my_range = paginator.page_range[start_index:end_index]

    tmp = {}
    tmp['pre']=paginator.get_page(start_index+1)
    tmp['nxt']=nxt
    print('----end----')

    return render(request, 'menu/notice_list.html', {'user':request.user.is_superuser,'my_range':my_range,'tmp':tmp,'notice_list' :notice_list, 'page_obj': page_obj})

'''
class NoticeList(ListView):
    model = Notice
    paginate_by = 20

    def get_queryset(self):
        notice_list = Notice.objects.order_by('-id') 
        return notice_list
'''
def rules(request):
    return render(request, 'menu/rules.html')

def talk(request):
    return render(request, 'menu/talk.html')

def diary(request):
    return render(request, 'menu/diary.html')

def woe(request):
    return render(request, 'menu/woe.html')


def noticewrite(request):
    print('----try to get write page----')
    if request.user.is_superuser :
        return render(request, 'menu/notice_write.html')
    else :
        return redirect('/menu/notice')

#class postcreate():

def postcreate(request):
    print('-----try to write-----')
    #check auth
    if request.user.is_superuser :
        form = NoticeForm(request.POST)
        if form.is_valid():
            noti = form.save(commit=False)
            noti.create_at = timezone.datetime.now()
            noti.writer = request.user
            noti.save()
            print('success to write')
        
    '''
    this is using model not form
    notice_board = Notice()
    notice_board.title = request.GET['title']
    notice_board.contents = request.GET['contents']
    notice_board.create_at = timezone.datetime.now()
    notice_board.writer = request.user

    notice_board.save()
    '''

    return redirect('/menu/notice')

class Rulesview(ListView):
    print('---- rules view ----')

    def get(self, request):
        Rules_list = Rules.objects.order_by('-id') 
        #paginator = Paginator(Notice.objects.all(), 10)
        paginator = Paginator(Rules.objects.order_by('-id'), 10)
        page = request.GET.get('page')
        current_page = int(page) if page else 1
        page_numbers_range = 5
        page_obj = paginator.get_page(page)
        max_index = len(paginator.page_range)
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        nxt = paginator.get_page(end_index).has_next()
        my_range = paginator.page_range[start_index:end_index]

        tmp = {}
        tmp['pre']=paginator.get_page(start_index+1)
        tmp['nxt']=nxt
        print('----end----')

        return render(request, 'menu/rules_list.html', {'user':request.user.is_superuser,'my_range':my_range,'tmp':tmp,'notice_list' :Rules_list, 'page_obj': page_obj})

class Ruleswrite(CreateView):
    # example
    # r = Ruleswrite(model=..,fields=..)
    # r.save()

    print('----try to get write page----')

    def check_auth(self):
        print(self.request.user.is_superuser)
        if not self.request.user.is_superuser :
            return False
        else :
            return True

    def form_valid(self, form):
        form.instance.writer = self.request.user
        form.instance.create_at = timezone.datetime.now()
        form.save()
        return super(Ruleswrite, self).form_valid(form)

class Test(Ruleswrite):
    model = Rules
    form_class = RulesForm
    template_name = "menu/ruleswrite.html"

    '''
    def post(self,request):
        print('post')
        if not super(Test,self).check_auth():
            return redirect('/menu/rules')
    '''
    def form_valid(self,form):
        print('try to save')
        if not super(Test,self).check_auth():
            return redirect('/menu/rules')
        else : 
            return super(Test, self).form_valid(form)

    def get_success_url(self):
        return reverse('rules', )


class Testt(Ruleswrite):
    print('-----try to write-----')
    form_class = RulesForm()
    template_name = "rulescreate.html"

    def form_valid():
        obj = form.save(commit=False)
        obj.create_at = timezone.datetime.now()
        obj.writer = request.user
        obj.save()
        print('success to write')
    #super().check_save(form)


def rules(request) :
    return render(request, '/menu/rules/index.html')

def ruleswrite(request) :
    return render(request, '/menu/rules/index.html')

def rulescreate(request) :
    return render(request, '/menu/rules/index.html')

def rules_details(request,pk) :
    rules_list = get_object_or_404(Rules, pk=pk)
    #rules_list = Rules.objects.get(pk=pk)
    rules_list.view = rules_list.view + 1
    rules_list.save()
    return render(request, 'menu/rules_details.html',{'rules_list':rules_list})

def comment(request,pk):
    print('-----try to comment-----')
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = NoticomForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = NoticomForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

#class Comment(CreateView):

class Noticomm(View):

    def post(self,request,pk):
        print('post method')
        form = NoticomForm(request.POST)
        if form.is_valid():
            print('form is valid')
            noti = form.save(commit=False)
            noti.post = get_object_or_404(Notice, pk=pk)
            noti.create_at = timezone.datetime.now()
            noti.writer = request.user
            noti.save()
            print('success to save')
        
        url = '/menu/notice/details/{}'.format(pk)
        #n = Notice.objects.get(pk=pk)
        #doc = n.noticomment_set.all()
        
        return redirect(url, args=[pk])
        #return render(request, 'menu/notice_details.html', {'pk':pk,'object':doc, "comments":n, "comment_form":form})
        #return redirect(url, kwargs={'form':'123'})

    def get(self, request):
        print('get method')
        form = NoticomForm(request.POST)

        return render(request, 'menu/notice_details.html', {'form':form})

    '''
    def form_valid(self, form):
        form.instance.writer = self.request.user
        form.instance.create_at = timezone.datetime.now()
        form.instance.post = get_object_or_404(Post, pk=self.request.POST['noti'])
        form.save()
    
    def get_success_url(self):
        return reverse('notice/details/', {'comm': model})
    '''

class Notirecomm(View):

    def post(self,request,pk):
        print('post method')
        form = NoticomForm(request.POST)
        if form.is_valid():
            print('form is valid')
            print(request.POST)
            noti = form.save(commit=False)
            noti.post = get_object_or_404(Notice, pk=request.POST['post_id'])
            noti.parent = get_object_or_404(Noticomment, pk=pk)
            noti.create_at = timezone.datetime.now()
            noti.writer = request.user
            noti.save()

            print('success to save')
        
        url = '/menu/notice/details/{}'.format(request.POST['post_id'])
        #n = Notice.objects.get(pk=pk)
        #doc = n.noticomment_set.all()
        
        return redirect(url, args=[request.POST['post_id']])
        #return render(request, 'menu/notice_details.html', {'pk':pk,'object':doc, "comments":n, "comment_form":form})
        #return redirect(url, kwargs={'form':'123'})

    def get(self, request):
        print('get method')
        form = NoticomForm(request.POST)

        return render(request, 'menu/notice_details.html', {'form':form})
from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from .models import Registration
from django.views import View
import requests
from django.conf import settings
import re
import bcrypt
from .forms import UserForm
from django.contrib.auth.models import User

#this is for sending email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Create your views here.

def index(request):
    #return HttpResponse("Hello, world. You're at the signup index.")
    return render(request, 'signup/index.html')

def signform(request) :
    #return HttpResponse("Hello, world. You're at the signup form.")
    return render(request, 'signup/signform.html',{'site_key': settings.RECAPTCHA_SITE_KEY})

def findaccount(request) :
    latest_question_list = User.objects.all()
    template = loader.get_template('signup/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
    #output = ', '.join([q.id_text for q in latest_question_list])
    #return HttpResponse(output)
    #return HttpResponse("you are looking for you account")

def main(request):
    #return HttpResponse("Hi %s" % id_text)
    if not request.method == 'POST':
        return redirect('/')

    data = request.POST
    name = data.get('name')
    secret_key = settings.RECAPTCHA_SECRET_KEY

    # captcha verification
    data = {
        'response': data.get('g-recaptcha-response'),
        'secret': secret_key
    }
    resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result_json = resp.json()

    print(result_json)

    if not result_json.get('success'):
        return render(request, 'signup/test.html', {'is_robot': True})
    # end captcha verification

    return render(request, 'main/index.html', {'name': name})

def create(request):
    print("---------here create---------")
    print(request.POST)

    userdata = request.POST

    # check recaptcha first
    secret_key = settings.RECAPTCHA_SECRET_KEY

    # captcha verification
    data = {
        'response': userdata.get('g-recaptcha-response'),
        'secret': secret_key
    }
    resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result_json = resp.json()

    print(result_json)

    if not result_json.get('success'):
        return render(request, 'signup/test.html', {'is_robot': True})
    # end captcha verification

    username = userdata.get('username')
    userpw = userdata.get('password')
    userpw2 = userdata.get('password2')
    useremail = userdata.get('email')

    #nick check
    result = { 'result' : '0'}
    if len(username) < 1 :
        #no blank
        result = {
            'result' : '1'
        }
        return JsonResponse(result)
    
    if any(sym in username for sym in "{}[]/?.,;:|)*~`!^-_+<>@#$%&\=('\""):
        #no special char
        result = {
            'result' : '2'
        }
        return JsonResponse(result)

    if bool(re.search(r"\s", username)) :
        #no whitespace
        result = {
            'result' : '3'
        }
        return JsonResponse(result)

    #email check
    if len(useremail) < 1 :
        #no blank
        result = {
            'result' : '11'
        }
        return JsonResponse(result)

    if bool(re.search(r"\s", useremail)) :
        #no whitespace
        result = {
            'result' : '12'
        }
        return JsonResponse(result)

    if not useremail.find('@') :
        #wrong format
        result = {
            'result' : '13'
        }
        return JsonResponse(result)

    #pw check
    if userpw != userpw2 :
        #differ
        result = {
            'result' : '21'
        }
        return JsonResponse(result)

    if len(userpw) < 1:
        #no blank
        result = {
            'result' : '22'
        }
        return JsonResponse(result)

    if result['result'] != '0' :
        text = 'input has something wrong :( result : {}'.format(result)
        print(text)
    #done input check

    # useremail, , userpass, userpass2
    # email_str, nickid, pass_str
    # encoding email & cryp password

    # check overlap again & insert
    print(request.user)
    user_form = UserForm(request.POST)
    if user_form.is_valid() :
        print('get here')
        usrname = user_form.cleaned_data['username']
        email = user_form.cleaned_data['email']
        password = user_form.cleaned_data['password']
        if User.objects.filter(username=usrname).exists() == False :
            if User.objects.filter(email=email).exists() == False :
                user = User.objects.create_user(username=usrname,email=email, password=password)
                regi = Registration(is_auth=False,user=user)
                regi.save()
                #user.save()
        '''
        if User.objects.filter(username=usrname).exists() == False :
            if User.objects.filter(email=email).exists() == False :
                
                #user_form.save()
                # no way: new_user = User.objects.create_user(user_form.cleaned_data)
                user = User.objects.create_user(username=usrname, email=email, password=password,is_active=False)
                regi = Registration(is_auth=False,user=user)
                regi.save()

            else :
                result = {'result' : '30'}
        else :
            result = {'result' : '40'}
        '''
    if result['result'] != '0' :
        text = 'already exists :( result : {}'.format(result)
        print(text)
        return JsonResponse(result)

    '''
    this is filter way

    try:
        if not Registration.objects.filter(nickid=).exists() :
            if not Registration.objects.filter(email_str=useremail).exists() :
                cryppw = userpw.encode('utf-8')
                cryppw = bcrypt.hashpw(cryppw, bcrypt.gensalt())
                password_crypt = cryppw.decode('utf-8')

                crypem = useremail.encode('utf-8')
                crypem = bcrypt.hashpw(crypem, bcrypt.gensalt())
                email_crypt = crypem.decode('utf-8')
                txt = "encrypted password : {}\nencrypted email : {}".format(password_crypt,email_crypt)
                print(txt)
                
                usr = Registration(email_str=email_crypt,nickid=,pass_str=password_crypt,is_active=False, is_auth=False)
                usr.save()

            else :
                result = {'result' : '30'}
        else :
            result = {'result' : '40'}

    except Exception as e:
        print("no way!")
        print(e)
    
    if result['result'] != '0' :
        text = 'already exists :( result : {}'.format(result)
        print(text)
        return JsonResponse(result)
    '''

    # email send
    current_site = get_current_site(request)
    domain = current_site.domain
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk)).encode().decode()
    token = account_activation_token.make_token(user)
    txt = "domain : {}, mail to : {}".format(domain,useremail)
    print(txt)
    sendmsg = render_to_string('signup/auth_email.html',{
                'domain': domain,
                'uid': uidb64,
                'token': token,
    })

    mail_title = "[회원가입] 이메일 인증을 완료해주세요."
    mail_to = useremail
    email = EmailMessage(mail_title, sendmsg, to=[mail_to])
    email.send()
    
    response = {'status': result['result'], 'url':'main'} 
    
    return JsonResponse(response)

def activate(request,uid,token):
    uid = force_text(urlsafe_base64_decode(uid))
    # usr = User.objects.get(pk=uid) can get error about no matching query
    if User.objects.filter(pk=uid).exists() :
        usr = User.objects.get(pk=uid)
        if account_activation_token.check_token(usr, token):
            usr.is_active = True
            usr.save()
            print('+++++++++Done activation+++++++++')

            return redirect('main')

    return HttpResponse('비정상적인 접근입니다.')

def tmp(request):

    print("here tmp")
    print(request.POST)

    userdata = request.POST

    # check input len, special char, space


    if 'username' in userdata :
        username = userdata.get('username')

        try:
            result = {
            'result' : 'success',
            'data' : "exist" if User.objects.filter(username=username).exists() else "not exist"
        }

        except Exception as e:
            print("no way!")
            print(e)
            result = {'result' : 'success',
            'data': "not exist"}

            return JsonResponse(result)
    
        '''
        try:
            nick = User.objects.get(username=)

    
        except Exception as e:
            print("no way!")
            print(e)
            #nick = None

            result = {'result':'fail'}

            return JsonResponse(result)
    
        result = {
            'result' : 'success',
            'data' : "not exist" if nick is None else "exist"
        }
        '''

    elif 'email' in userdata:
        useremail = userdata.get('email')
        print(useremail)

        try:
            result = {
                'result' : 'success',
                'data' : "exist" if User.objects.filter(email=useremail).exists() else "not exist"

            }            

        except Exception as e:
            print("no way!")
            print(e)

            result = {'result' : 'success',
            'data': "not exist"}

            return JsonResponse(result)

        '''
        try:
            email = User.objects.get(email=useremail)

        except Exception as e:
            print("no way!")
            print(e)
            #email = None

            result = {'result':'fail'}

            return JsonResponse(result)
        
        result = {
            'result' : 'success',
            'data' : "not exist" if email is None else "exist"
        }
        '''

    print(result)
    #context = {'emailaddr':useremail}
    #print(len())
    #user = Useracc.object.get()

    return JsonResponse(result)
    #return render(request, 'signup/test.html')

'''
class CreateView(View):
    def get(self, request, *args, **kwargs):
        print("get")

    def post(self, request):
        print("post")
'''
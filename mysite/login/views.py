from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import requests, re, bcrypt
from django.contrib.auth import authenticate, get_user,login
from signup.models import Registration
from django.template.loader import render_to_string
from .my_auth import SettingsBackend
from django.contrib.auth.models import User


# Create your views here.

def trylogin(request):
    #return HttpResponse("Hello, world. You're at the login index.")

    print("---------here login---------")
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
        return render(request, 'login/index.html')
    # end captcha verification

    useremail = userdata['email']
    userpw = userdata['password']

    # user input check
    # email check
    result = {
        'status' :'1',
        'result' : '0'
    }
    if len(useremail) < 1 :
        #no blank
        result = {
            'status' :'1',
            'result' : '11'
        }

    if bool(re.search(r"\s", useremail)) :
        #no whitespace
        result = {
            'status' :'1',
            'result' : '12'
        }
        return JsonResponse(result)

    if not useremail.find('@') :
        #wrong format
        result = {
            'status' :'1',
            'result' : '13'
        }
        return JsonResponse(result)

    #pw check
    if len(userpw) < 1:
        #no blank
        result = {
            'status' :'1',
            'result' : '21'
        }
        return JsonResponse(result)

    if result['result'] != '0' :
        text = 'input has something wrong :( result : {}'.format(result)
        print(text)
    #done input check

    #chk user
    try:
        '''
        crypem = useremail.encode('utf-8')
        crypem = bcrypt.hashpw(crypem, bcrypt.gensalt())
        email_crypt = crypem.decode('utf-8')

        cryppw = userdata['password'].encode('utf-8')
        cryppw = bcrypt.hashpw(cryppw, bcrypt.gensalt())
        pw_crypt = cryppw.decode('utf-8')
        '''

        #email check
        if User.objects.filter(email=useremail).exists() :
            print('hi user')
            usr = SettingsBackend.authenticate(request, email=useremail, password=userpw)
            #usr = authenticate(email=useremail, password=userpw)

        else :
            print('no such useremail')
            result = {
                'status' : '4'
            }
            return JsonResponse(result)

        if usr is not None:
            login(request, usr) #is necessary but for username login
            if usr.is_active == True :
                print('this is active user')
                 
                if usr.registration.is_auth == True :
                    print('this is auth user')
                    result = {
                        'status' :'0',
                        'url':'menu'
                    }
                    # doesnt work :( return render_to_string('login/index.html')
                    return JsonResponse(result)

                else :
                    result = {
                            'status' : '3',
                            'url' : 'login/auth'
                    }
                    return JsonResponse(result)
                
            else :
                print('not active user')
                result = {
                    'status' :'2',
                }
                return JsonResponse(result)

        return HttpResponse('fail to auth')
        
    except Exception as e:
        print("no way!")
        print(e)

    result = {
        'status' : '-1'
    }
    return JsonResponse(result)

def auth(request):
    #return HttpResponse("Hello, world. You're at the auth index.")
    print(request.user)
    print(request.session.session_key)
    return render(request, 'login/index.html',{'username':request.user.get_username()})

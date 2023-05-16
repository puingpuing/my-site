window.onload = function () 
{
    email = document.getElementById('email');
    password = document.getElementById('password');
}

function getCookie(name) 
{
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') 
    {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) 
        {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) 
            {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function inputchk()
{
    result = true;

    $.getScript("/static/index.js",function(){
        //blank check first
        if(chkblank(email) == false)
        {
            document.getElementById('alert_email').innerText = "please enter your email address";
            result = false;
        }
        else 
        {
            tmp(email)
            document.getElementById('alert_email').innerText = "";

            //white space check
            if(chkspace(email) == false)
            {
                document.getElementById('alert_email').innerText = "no space character allowed";
                result = false;
            }
            else{
                tmp(email);
                document.getElementById('alert_email').innerText = "";

                //email format
                if(email.value.indexOf("@")==-1)
                {
                    document.getElementById('alert_email').innerText = "this is not a valid format";
                    alert_blank(email);
                    result = false;
                }
            }
        }

        if(chkblank(password) == false)
        {
            document.getElementById('alert_password').innerText = "please enter your password";
            result = false;
        }
        else
        {
            tmp(password);
            document.getElementById('alert_password').innerText = "";

            //white space check
            if(chkspace(password) == false)
            {
                document.getElementById('alert_password').innerText = "no space character allowed";
                result = false;
            }
            else{
                tmp(password);
                document.getElementById('alert_password').innerText = "";
            }
        }
    });

    return result;
}

function resultchk(res)
{
    $.getScript("/static/index.js",function(){
        if(res == '11')
        {
            //email blank
            document.getElementById('alert_email').innerText = "please enter your email address";
            alert_blank(usermail);            
        }
        else if(res == '12')
        {
            //email whitespace
            document.getElementById('alert_email').innerText = "no space character allowed";
            alert_blank(usermail);
        }
        else if(res == '13')
        {
            //email format
            document.getElementById('alert_email').innerText = "this is not a valid format";
            alert_blank(usermail);            
        }
        else if(res == '21')
        {
            //pw blank
            document.getElementById('alert_password').innerText = "please enter your password";
            alert_blank(password);            
        }
    });
}
function login()
{
    
    if(inputchk() == true)
    {
        var csrftoken = getCookie('csrftoken');

        data = {'email': email.value, 
        'password':password.value,
        'csrfmiddlewaretoken' : csrftoken ,
        'g-recaptcha-response' : document.getElementById('g-recaptcha-response').value}

        $.ajax({ 
            url:'login',
            type:"POST",
            data : data
            ,
            success:function(data)
            {
                console.log(data);
                if(data.status == "0"){
                    window.location.href = data.url;
                }
                else if(data.status == "1")
                {
                    resultchk(data.result);
                }
                else if(data.status == "2")
                {
                    alert('you can login after mail auth');
                }
                else if(data.status == "3")
                {
                    alert('gogo');
                    window.location.href = data.url;
                }
                else if(data.status == "4")
                {
                    alert('no such email');
                }
                else{
                    alert('retry again');
                    window.location.href='/';
                }
                //console.log(data);
            }
        })
    }
}

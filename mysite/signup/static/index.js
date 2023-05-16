window.onload = function () 
{
    nickdupBool = false;
    maildupBool = false;

    frm = document.register_form;
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

function confirm2() 
{
    // check password length, email format 
    // check overlap

    //alert(dupBool);
    //alert(maildupBool);
    if (nickdupBool && maildupBool)
    {
        var resemail;
        var resnick;
        var respw;
    
        if(resemail = checkemail())
        {
            tmp(frm.email);
        }
    
        if(respw = checkpw())
        {
            tmp(frm.password);
            tmp(frm.password2);
        }
    
        if(resnick = checknick())
        {
            tmp(frm.username);
        }
    
        if(resemail && resnick && respw)
        {
            //submit!
            alert("회원가입 완료!");
            //frm.action = '/signup/create';
            //frm.submit();
            tmp(frm.password);
            tmp(frm.password2);
            tmp(frm.username);
            tmp(frm.email);

            var csrftoken = getCookie('csrftoken');
            //var queryString = $("form[name=register_form]").serialize()
            //var queryString = $('regi').serialize();
            //console.log(queryString)

            $.ajax({ 
                url:'create',
                type:"POST",
                data : {
                    'email' : $("#email").val(),
                    'username' : $("#username").val(),
                    'password' : $("#password").val(),
                    'password2' : $("#password2").val(),
                    'csrfmiddlewaretoken' : csrftoken,
                    'g-recaptcha-response' : $("input[name=g-recaptcha-response]").val()
                }
                ,
                success:function(data)
                { 
                    if(data.result == '1')
                    {
                        //nick blank
                        alert_blank(frm.username);
                        document.getElementById('alert_username').innerText = "please enter your nickname";

                    }
                    else if(data.result == '2')
                    {
                        //nick special char
                        alert_blank(frm.username);
                        document.getElementById('alert_username').innerText = "no special character allowed";

                    }
                    else if(data.result == '3')
                    {
                        //nick whitespace
                        alert_blank(frm.username);
                        document.getElementById('alert_username').innerText = "no space character allowed";
                    }
                    else if(data.result== '11')
                    {
                        //email blank
                        alert_blank(frm.email);
                        document.getElementById('alert_email').innerText = "please enter your email address";
                    }
                    else if(data.result== '12')
                    {
                        //email space
                        alert_blank(frm.email);
                        document.getElementById('alert_email').innerText = "no space character allowed";
                        
                    }
                    else if(data.result== '13')
                    {
                        //email wrong format
                        alert_blank(frm.email);
                        document.getElementById('alert_email').innerText = "this is not a valid format";
                    }
                    else if(data.result== '21')
                    {
                        //pw differ
                        alert_blank(frm.password2);
                        document.getElementById('alert_password2').innerText = "password does not match";
                        
                    }
                    else if(data.result== '22')
                    {
                        //pw blank
                        alert_blank(frm.password);
                        alert_blank(frm.password2);
                        document.getElementById('alert_password').innerText = "please enter your password";
                        document.getElementById('alert_password2').innerText = "please enter your password";
                    }
                    else if(data.result == '30')
                    {
                        //email exists
                        alert_blank(frm.email);
                        document.getElementById('alert_email').innerText = "you already signup before";
                    }
                    else if(data.result == '40')
                    {
                        //nick exists
                        alert_blank(frm.username);
                        document.getElementById('alert_username').innerText = "this nickname already exists";
                    }
                    else if(data.status == '0'){
                        alert('gogo');
                        window.location.href = data.url;
                    }
                } 
            })

        }
    }
    else
    {
        // chk overlap first
        alert('중복체크 먼저 하세요!');
        return false;
    }
    /*
    var ps = document.getElementsByName('password').values;
    var ps2 = document.getElementsByName('password2').values;
    var em = document.getElementsByName('email').values;    
    var nick = document.getElementsByName('').values;
    */
}

function tmp(form)
{
    document.getElementById('alert_'+form.id).innerText = "";
    form.style.border="1px inset";
    form.style.borderColor="internal-light-dark";
}

function alert_blank(formname)
{
    formname.style.borderColor = '#FF0000';
    document.getElementById('alert_'+formname.id).style.color = '#FF0000';
}

function chkblank(form)
{
    if(form.value == "")
    {
        alert_blank(form);
    
        return false;
    }
}

function chkspeical(form)
{
    var special_pattern = /[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]/gi    
    
    if(special_pattern.test(form.value) == true)
    {
        alert_blank(form);

        return false;
    }
}

function chkspace(form)
{
    var blank_pattern = /[\s]/g;
    //form.load('')
    if(blank_pattern.test(form.value) == true)
    {
        //alert("space exists");
        alert_blank(form);

        return false;
    }
}
function checkemail() {

    if(chkblank(frm.email)==false)
    {
        //no blank
        document.getElementById('alert_email').innerText = "please enter your email address";
        
        return false;
    }

    if(frm.email.value.indexOf("@")==-1)
    {
        //no correct format
        document.getElementById('alert_email').innerText = "this is not a valid format";
        alert_blank(frm.email);

        return false;
    }

    if(chkspace(frm.email)==false)
    {
        //no space
        document.getElementById('alert_email').innerText = "no space character allowed";
    
        return false;
    }

    return true;
}

function checkpw() {
    if(chkblank(frm.password)==false)
    {
        //no blank
        document.getElementById('alert_password').innerText = "please enter your password";
    }
    else
    {

        if(chkspace(frm.password)== false)
        {
            //no space
            document.getElementById('alert_password').innerText = "no space character allowed";
        }
        else 
        {
            tmp(frm.password);
        }
    }

    if(chkblank(frm.password2)==false)
    {
        //no blank
        document.getElementById('alert_password2').innerText = "please enter your password";

        return false;
    }

    else{

        if(chkspace(frm.password2)==false)
        {
            //no space
            document.getElementById('alert_password2').innerText = "no space character allowed";
        
            return false;
        }

        else 
        {
            tmp(frm.password2);
        }
    }
    
    if(frm.password.value != frm.password2.value)
    {
        //differ 

        alert_blank(frm.password2);
        document.getElementById('alert_password2').innerText = "password does not match";

        return false;
    }
    
    if (frm.password.value.length < 10)
    {
        //length 

        alert_blank(frm.password);
        alert_blank(frm.password2);
        document.getElementById('alert_password').innerText = "passwords should be 10 characters long at least";
        document.getElementById('alert_password2').innerText = "passwords should be 10 characters long at least";

        return false;
    }

    return true;
}

function checknick() {
    if(chkblank(frm.username)==false)
    {
        //no blank

        document.getElementById('alert_username').innerText = "please enter your nickname";
        return false;
    }
    
    if(chkspeical(frm.username) == false)
    {
        //no special character
        document.getElementById('alert_username').innerText = "no special character allowed";

        return false;
    }

    if(chkspace(frm.username)==false)
    {
        //no space
        document.getElementById('alert_username').innerText = "no space character allowed";
    
        return false;
    }

    return true;
}

function dupchkemail() {
    if(checkemail())
    {
        tmp(frm.email);
    }
    else 
    {
        return false;
    }

    var csrftoken = getCookie('csrftoken');
    //const csrftoken = $(“[name=csrfmiddlewaretoken]”).val();

    $.ajax({ 
        url:'tmp/',
        type:"POST",
        data : 
        { 
            'email':$("#email").val(),
            'csrfmiddlewaretoken' : csrftoken
        }, 
        success:function(data)
        {             
            if(data.result == 'success')
            {
                if(data.data == 'not exist')
                {
                    tmp(frm.username)
                    document.getElementById('alert_email').innerText = "you can use this address";
                    document.getElementById('alert_email').style.color = '#000000';
                    maildupBool = true;
                }
                else
                {
                    alert_blank(frm.email)
                    document.getElementById('alert_email').innerText = "you already signup before";
                }
            }
            else
            {
                alert_blank(frm.email)
                document.getElementById('alert_email').innerText = "wrong format";
            }
            //$('#data_table').html(data)
        } 
    })
}

function dupchknick() 
{
    if(checknick())
    {
        tmp(frm.username);
    }
    else 
    {
        return false;
    }

    const csrftoken = getCookie('csrftoken');
    //const csrftoken = $(“[name=csrfmiddlewaretoken]”).val();

    $.ajax({ 
        url:'tmp/',
        type:"POST",
        data : 
        { 
            'username':$("#username").val(),
            'csrfmiddlewaretoken' : csrftoken
        }, 
        success:function(data)
        { 
            if(data.result == 'success')
            {
                if(data.data == 'not exist')
                {
                    tmp(frm.username)
                    document.getElementById('alert_username').innerText = "you can use this nickname";
                    document.getElementById('alert_username').style.color = '#000000';
                    nickdupBool = true;
                }
                else
                {
                    alert_blank(frm.username)
                    document.getElementById('alert_username').innerText = "this nickname already exists";
                }
            }
            else
            {
                alert_blank(frm.username)
                document.getElementById('alert_username').innerText = "wrong format";
            }
            //$('#data_table').html(data) 
        } 
    })
}
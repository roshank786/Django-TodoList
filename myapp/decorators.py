from django.contrib import messages
from django.shortcuts import redirect

def sign_required(fn):

    def wrapper(request,*args,**kwargs):

        if not request.user.is_authenticated:

            messages.error(request,"SignIn Required !!!")

            return redirect("signin")
        
        else:

            return fn(request,*args,**kwargs)
    return wrapper
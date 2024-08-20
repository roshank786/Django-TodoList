from django.shortcuts import render,redirect

from django.views import View

from myapp.forms import RegistrationForm,LoginForm,TaskForm

from django.contrib.auth import authenticate,login,logout

from django.contrib import messages

from myapp.models import Task

from myapp.decorators import sign_required

from django.utils.decorators import method_decorator




class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance = RegistrationForm()

        return render(request,"register.html",{"form":form_instance})
    

    def post(self,request,*args,**kwargs):

        form_instance = RegistrationForm(request.POST)

        if form_instance.is_valid:

            form_instance.save()

            print("Account created succesfully")

            messages.success(request,"Account created successfully")

            return redirect("signin")
        
        else:
            
            print("Failed to create account")

            messages.error(request,"Failed to create account")

            return render(request,"register.html",{"form":form_instance})
        


class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance = LoginForm()

        return render(request,"signin.html",{"form":form_instance})
    

    def post(self,request,*args,**kwargs):

        form_instance = LoginForm(request.POST)

        if form_instance.is_valid():
            
            user_object = authenticate(request,**form_instance.cleaned_data)

            if user_object:

                login(request,user_object)

                messages.success(request, "SignIn Successful !")

                return redirect("task-list")
            
            print("SignIn Failed !!!")
            
            messages.error(request, "Wrong Credentials !")

        return render(request,"signin.html",{"form":form_instance})
    

@method_decorator(sign_required,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")





@method_decorator(sign_required,name="dispatch")
class TaskCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance = TaskForm()

        return render(request,"task_add.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        if not request.user.is_authenticated:

            messages.error(request,"Invalid Session !!!")

            return redirect("signin")
        
        form_instance = TaskForm(request.POST)

        if form_instance.is_valid:

            form_instance.instance.user_object=request.user

            form_instance.save()

            return redirect("task-list")

        return render(request,"task_add.html",{"form":form_instance})
    

@method_decorator(sign_required,name="dispatch")
class TaskListView(View):

    def get(self,request,*args,**kwargs):

        qs = Task.objects.filter(user_object=request.user)

        return render(request,"task_list.html",{"list":qs})
    

@method_decorator(sign_required,name="dispatch")
class TaskEditView(View):

    def get(self,request,*args,**kwargs):

        id = kwargs.get("pk")

        task_object = Task.objects.get(id=id)

        form_instance = TaskForm(instance=task_object)

        return render(request,"task_edit.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        id = kwargs.get("pk")

        task_object = Task.objects.get(id=id)

        form_instance = TaskForm(request.POST,instance=task_object)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("task-list")
        
        else:
            return render(request,"task_edit.html",{"form":form_instance})
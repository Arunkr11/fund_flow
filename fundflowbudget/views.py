from django.shortcuts import render,redirect
from django.views.generic import View
from fundflowbudget.models import Transaction
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login

# Create your views here.

# url : localhost:8000/transactions/all/
class TransactionListView(View):
    def get(self, request, *args, **kwargs):
        qs=Transaction.objects.all()
        return render(request,'transactions_list.html',{'data':qs})
    
class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        exclude=('created_date',)
        # fields='__all__'
        # fields=['title','amount','type','category','user']
              
#  view for creating transactions
# url : localhost:8000/transaction/add/
# method get and post
class TransactionCreatedView(View):
    def get(self, request, *args, **kwargs):
        form=TransactionForm()
        return render(request,'transactions_add.html',{'form':form})
    
    def post(self, request, *args, **kwargs):
        form=TransactionForm(request.POST)
        if form.is_valid():
        #     data=form.changed_data
        #     Transaction.objects.create(**data)
        #     return redirect('transactions-list')
        # else:
        #     return render(request,'transactions_add.html',{'form':form})
            form.save()
            return redirect('transactions-list')
        else:
            return render(request,'transactions_add.html',{'form':form})
        
# transaction detail view        
# url : localhost:8000/transaction/{id}/
# method get

class TransactionDetailView(View):
    def get(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        qs=Transaction.objects.get(id=id)
        return render(request,"transactions_detail.html",{'data':qs})
        
        
# transaction delete View
# url : localhost:8000/transaction/{id}/remove/
# method get

class TransactionDeleteView(View):
    def get(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        Transaction.objects.filter(id=id).delete()
        return redirect('transactions-list')
    
# transaction update View
# url : localhost:8000/transaction/{id}/change/
# method get post

class TransactionUpdateView(View):
    def get(self,request,*args ,**kwargs):
        id=kwargs.get('pk')
        transaction_object=Transaction.objects.get(id=id)
        form=TransactionForm(instance=transaction_object)
        return render (request,'transaction_edit.html',{'form':form})
    
    def post(self,request,*args, **kwargs):
        id=kwargs.get('pk')
        transaction_object=Transaction.objects.get(id=id)
        form=TransactionForm(request.POST,instance=transaction_object)
        if form.is_valid():
            form.save()
            return redirect('transactions-list')
        else:
            return render(request,'transactions_add.html',{'form':form})
        
    
class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']
        
# signup
# url : localhost:8000/signup/
# method  get post

class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form=RegistrationForm()
        return render(request,'signup.html',{'form':form})
    
    def post(self, request, *args, **kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            # form.save()
            User.objects.create_user(**form.cleaned_data)
            print("Registration successful")
            return redirect('signin-view')
        else:
            print("Registration failed")
            return render(request,'signup.html',{'form':form})
            
# signin
# url : localhost:8000/signin/
# method get and post

class LoginForm(forms.Form):
    username= forms.CharField(max_length=225)
    password= forms.CharField(max_length=225)
    
class SignInView(View):
    def get(self, request, *args, **kwargs):
        form=LoginForm()
        return render(request,'login.html',{'form':form})
    
    def post(self, request, *args, **kwargs):
        form=LoginForm(request.POST)
        if  form.is_valid():
            u_name=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password')
            print(u_name,pwd)
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                print('is valid')
                login(request,user_object)
                return redirect('transactions-list')
        
        print('Invalid username or password')
        return render(request,'login.html',{'form':form})
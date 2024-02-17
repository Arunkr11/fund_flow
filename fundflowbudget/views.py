from django.shortcuts import render,redirect
from django.views.generic import View
from fundflowbudget.models import Transaction
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils import timezone
from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.decorators.cache import never_cache



def signin_requried(fn):
    def wrapper(request,*args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in")
            return redirect('signin-view')
        else:
            return fn(request, *args, **kwargs)
    return wrapper
decs=[signin_requried,never_cache]
# Create your views here.

# url : localhost:8000/transactions/all/
@method_decorator(decs,name='dispatch')
class TransactionListView(View):
    def get(self, request, *args, **kwargs):
        qs=Transaction.objects.filter(user_object=request.user)
        cur_month=timezone.now().month
        cur_year=timezone.now().year
        print(cur_month,cur_year)
        # expense_total=Transaction.objects.filter(
        #     user_object=request.user,
        #     type='expense',
        #     created_date__month=cur_month,
        #     created_date__year=cur_year
        # ).aggregate(Sum('amount'))
        # print(expense_total)
        # income_total=Transaction.objects.filter(
        #     user_object=request.user,
        #     type='income',
        #     created_date__month=cur_month,
        #     created_date__year=cur_year
        # ).aggregate(Sum('amount'))
        # print(income_total)
        data = Transaction.objects.filter(
            created_date__month=cur_month,
            created_date__year=cur_year,
            user_object=request.user
        ).values('type').annotate(type_sum=Sum('amount'))
        
        cat = Transaction.objects.filter(
            created_date__month=cur_month,
            created_date__year=cur_year,
            user_object=request.user
        ).values('category').annotate(cat_sum=Sum('amount'))
        
        print(cat)
        return render(request,'transactions_list.html',{'data':qs,'type_total':data,'cat_total':cat})
    
class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        exclude=('created_date','user_object')
        # fields='__all__'
        # fields=['title','amount','type','category','user']
        widgets={
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'amount' : forms.NumberInput(attrs={'class' : 'form-control'}),
            'type' : forms.Select(attrs={'class' : 'form-control form-select'}),
            'category' : forms.Select(attrs={'class': 'form-control form-select'})
    
        }
        
              
#  view for creating transactions
# url : localhost:8000/transaction/add/
# method get and post
@method_decorator(decs,name='dispatch')
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
            # form.instance.user_object=request.user
            # form.save()
            data=form.cleaned_data
            Transaction.objects.create(**data,user_object=request.user)
            messages.success(request,'Transaction added successfully')
            return redirect('transactions-list')
        else:
            messages.error(request,'failed to create transaction')
            return render(request,'transactions_add.html',{'form':form})
        
# transaction detail view        
# url : localhost:8000/transaction/{id}/
# method get
@method_decorator(decs,name='dispatch')
class TransactionDetailView(View):
    def get(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        qs=Transaction.objects.get(id=id)
        return render(request,"transactions_detail.html",{'data':qs})
        
        
# transaction delete View
# url : localhost:8000/transaction/{id}/remove/
# method get
@method_decorator(decs,name='dispatch')
class TransactionDeleteView(View):
    def get(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        Transaction.objects.filter(id=id).delete()
        messages.success(request,'transaction has been deleted')
        return redirect('transactions-list')
    
# transaction update View
# url : localhost:8000/transaction/{id}/change/
# method get post
@method_decorator(decs,name='dispatch')
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
            messages.success(request,'transaction updated successfully')
            return redirect('transactions-list')
        else:
            messages.error(request,'transaction updation failed')
            return render(request,'transactions_add.html',{'form':form})
        
    
class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']
        widgets={
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email' : forms.EmailInput(attrs={'class' : 'form-control'}),
            'password' : forms.PasswordInput(attrs={'class' : 'form-control'})
        }
        
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
    username= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password= forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
class SignInView(View):
    def get(self, request, *args, **kwargs):
        form=LoginForm()
        return render(request,'signin.html',{'form':form})
    
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
        return render(request,'signin.html',{'form':form})
@method_decorator(decs,name='dispatch')    
class SignOutView(View):
    def get(self, request, *args,**kwargs):
        logout(request)
        messages.success(request,'logout successfully')
        return redirect('signin-view')
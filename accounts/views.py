from django.shortcuts import render,redirect,HttpResponse
from .forms import Register
from django.contrib.auth import logout
from django.contrib  import messages
# Create your views here.
def register(request):
    form=Register(request.POST or None)
    if request.method=='POST':
    
        if form.is_valid():
            print(form.errors)
            user=form.save(commit=True)
            user.is_active=True
            user.save()
            messages.success(request,'Your account has been created successfully!')
            return redirect('accounts:login')
            
    return render(request,'accounts/register.html',{'form':form})        



def logout_view(request):
    
    logout(request)
    return render(request,'accounts/logout.html')
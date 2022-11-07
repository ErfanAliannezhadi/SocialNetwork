from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from . import forms
from .models import Follow, UserProfileModel
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class Registerview(View):
    form_class = forms.UserRegisterForm

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        form = self.form_class()
        return render(request,'accounts/register.html',{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(data['username'],data['email'],data['password'])
            user.first_name= data['firstname']
            user.last_name=data['lastname']
            user.profile.bio = data['bio']
            user.profile.birth_date = data['birth_date']
            user.profile.photo = data['photo']
            user.save()
            user.profile.save()
            messages.success(request,'you registered successfully','success')
            return redirect('home:home')
        return render(request,'accounts/register.html',{'form':form})


class Loginview(View):
    form_class = forms.UserLoginForm

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request,*args,*kwargs)

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        form = self.form_class()
        return render(request,'accounts/login.html',{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,username=data['username'],password=data['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'you logged in successfully','success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.warning(request,'your Username or Password is wrong','warning')
            return render(request,'accounts/login.html',{'form':form})


class Logoutview(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,'you logged out successfully','success')
        return redirect('home:home')


class Profileview(LoginRequiredMixin,View):
    def get(self, request, user_id, user_name):
        user = get_object_or_404(User, id=user_id, username=user_name)
        posts = user.posts.all()
        is_following = False
        follow = Follow.objects.filter(from_user=request.user,to_user=user)
        if follow.exists():
            is_following = True
        return render(request,'accounts/profile.html',{'user':user,'posts':posts,'is_following':is_following})


class Userpasswordresetview(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'


class Userpasswordresetdoneview(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class Userpasswordresetconfirmview(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class Userpasswordresetcompleteview(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class Userfollowview(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user = User.objects.get(id=user_id)
        follow = Follow.objects.filter(from_user=request.user,to_user=user)
        if user == request.user:
            messages.error(request,'you can\'t follow your self','danger')
        elif follow :
            messages.warning(request,'you had followed this user','danger')
        else:
            Follow.objects.create(from_user=request.user,to_user=user)
            messages.success(request,'you followed this user successfully','success')
        return redirect('accounts:user_profile', user.id,user.username)


class Userunfollowview(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user = User.objects.get(id=user_id)
        follow = Follow.objects.filter(from_user=request.user,to_user=user)
        if not follow.exists():
            messages.warning(request,'you didn\'t follow this user')
        else:
            follow.delete()
            messages.success(request,'you unfollowed this user successfully','success')
        return redirect('accounts:user_profile',user.id,user.username)


class EditProfileView(View):
    def get(self,request):
        initial = {'username':request.user.username,'email':request.user.email,'firstname':request.user.first_name,
                   'lastname':request.user.last_name,'bio':request.user.profile.bio,'birth_date':request.user.profile.birth_date,
                   'photo':request.user.profile.photo}
        form = forms.EditProfileForm(initial=initial)
        return render(request,'accounts/editprofile.html',{'form':form})

    def post(self,request):
        form = forms.EditProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            request.user.username = data['username']
            request.user.email = data['email']
            request.user.first_name = data['firstname']
            request.user.last_name = data['lastname']
            request.user.profile.bio = data['bio']
            request.user.profile.birth_date = data['birth_date']
            if data['photo']:
                request.user.profile.photo = data['photo']
            request.user.save()
            messages.success(request,'your profile edited successfully','success')
            return redirect('accounts:user_profile', request.user.id, request.user.username)
        return redirect('accounts:edit_profile')


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout 
from django.views import View

from app.forms import UserSignupForm, UserSignupProfileform, NewsForm
from app.models import Profile, News


class Index(View):
    def get(sef, request, *args, **kwargs):
        news = News.objects.all().order_by('timestamp').reverse().first()
        path_to_file = news.news_file.path
        file = open(path_to_file, 'r')
        news_text = file.readlines()
        file.close()
        args = {}
        args['news']=news
        args['title']=news_text[0]
        args['index_body']=news_text[1]
        args['body']=news_text[2]
        return render(request, 'index.html', {'args':args})

class SignUp(View):
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        user_form = UserSignupForm()
        profile_form = UserSignupProfileform()
        forms = {}
        forms['user_form'] = user_form
        forms['profile_form'] = profile_form
        return render(request, self.template_name, forms)


    def post(self, request, *args, **kwargs):
        user_form = UserSignupForm(request.POST)
        profile_form = UserSignupProfileform(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = User.objects.create_user(
                username=user_form.cleaned_data['username'],
                first_name=user_form.cleaned_data['first_name'],
                last_name=user_form.cleaned_data['last_name'],
                email=user_form.cleaned_data['email'],
                password=user_form.cleaned_data['password']
            )
            profile = Profile.objects.create(
                user=user,
                about_me=profile_form.cleaned_data['about_me'],
                img_file=profile_form.cleaned_data['img_file']
            )
            user.save()
            profile.save()
            return redirect('login')
        return redirect('signup')


class PostNews(View):
    template_name = 'posts/postnews.html'

    def get(self, request, *args, **kwargs):
        news_form = NewsForm()
        return render(request, self.template_name, { 'news_form':news_form })

    def post(self, request, *args, **kwargs):
        news_form = NewsForm(request.POST, request.FILES)
        author_id = User.objects.filter(id=request.user.id).first()
        if news_form.is_valid():
            news = News.objects.create(
                title=news_form.cleaned_data['title'],
                index_body=news_form.cleaned_data['index_body'],
                body=news_form.cleaned_data['body'],
                img_file=news_form.cleaned_data['img_file'],
                news_file=news_form.cleaned_data['news_file'],
                author_id=author_id
            )
            news.save()
            return redirect('index')
        print(news_form.errors)
        input()
        return render(request, self.template_name, { 'news_form':news_form })

class ShowProfile(View):

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=request.user).first()
        return render(request, 'registration/profile.html', { 'profile':profile })


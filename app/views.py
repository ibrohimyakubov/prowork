from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError

from .models import CustomUser, Startapper, Staff, IdeaStartapper, ApplicationStaff, SuccessProjects, CommentOfPost, \
    AboutUS, ContacktsProwork, AllUsersIdea
from app.forms import RegisterForm, IdeaStartapperForm, ApplicationDeveloperForm, ApplicationPractitionerForm, \
    UserUpdateForm, StartapperUpdateForm, CommentForm, AllUsersIdeaForm
from django.views import View


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            user.save()
            login(request, user)
            current_user = CustomUser.objects.get(email=request.user.email)
            if current_user.user_type == CustomUser.STARTAPPER:
                Startapper.objects.create(user=user).save()
                messages.success(request, 'Your account has been created')
                return redirect('home')
            if current_user.user_type == CustomUser.DEVELOPER:
                Staff.objects.create(user=user)
                messages.success(request, 'Your account has been created')
                return redirect('home')
            if current_user.user_type == CustomUser.PRACTITIONER:
                Staff.objects.create(user=user)
                messages.success(request, 'Your account has been created')
                return redirect('home')
        else:
            messages.warning(request, "Registration error!")
            return HttpResponseRedirect('/')
    form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, 'Error!')
            return redirect('login')
    return render(request, 'login.html')


def logout_(request):
    logout(request)
    return HttpResponseRedirect('/')


def all_users_idea(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form_as = AllUsersIdeaForm(request.POST, request.FILES)
        if form_as.is_valid():
            current_user = Staff.objects.get(user=request.user)
            data = AllUsersIdea()
            data.title = form_as.cleaned_data['title']
            data.description = form_as.cleaned_data['description']
            if request.FILES:
                data.file = request.FILES['file']
            else:
                data.file = form_as.cleaned_data['file']
            data.user = current_user
            data.save()
            messages.success(request, 'Successfully idea send!')
            return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)


@login_required(login_url='login')
def developer_home(request):
    try:
        developer = Staff.objects.get(user=request.user)
        idea_developer = ApplicationStaff.objects.filter(user=developer)
    except:
        messages.warning(request, 'you go to developer page')
        return redirect('home')

    if request.method == 'POST':
        form = ApplicationDeveloperForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = Staff.objects.get(user=request.user)
            data = ApplicationStaff()
            data.title = form.cleaned_data['title']
            data.description = form.cleaned_data['description']
            try:
                data.resume = request.FILES['resume']
            except MultiValueDictKeyError:
                messages.warning(request, 'resume where?')
                return redirect('developer_home')
            data.work_type = form.cleaned_data['work_type']
            data.user = current_user
            data.save()
            messages.success(request, 'You application successfully send')
            return redirect('developer_home')
        else:
            messages.warning(request, 'Application not send!')
            return redirect('developer_home')
    form = ApplicationDeveloperForm()

    context = {
        'developer': developer,
        'idea_developer': idea_developer,
        'form': form,
    }
    return render(request, 'users_page/developer_home.html', context)


@login_required(login_url='login')
def practitioner_home(request):
    try:
        practitioner = Staff.objects.get(user=request.user)
        application_practitioner = ApplicationStaff.objects.filter(user=practitioner)
        idea_practitioner = AllUsersIdea.objects.filter(user=practitioner)
    except:
        messages.warning(request, 'you go to developer page')
        return redirect('home')

    if request.method == 'POST':
        form = ApplicationPractitionerForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = Staff.objects.get(user=request.user)
            data = ApplicationStaff()
            data.title = form.cleaned_data['title']
            data.description = form.cleaned_data['description']
            data.resume = form.cleaned_data['resume']
            data.work_type = form.cleaned_data['work_type']
            data.user = current_user
            data.save()
            messages.success(request, 'Your application successfully send')
            return redirect('practitioner_home')
        else:
            messages.warning(request, 'You Application not send!')
            return redirect('practitioner_home')
    form = ApplicationPractitionerForm()
    context = {
        'practitioner': practitioner,
        'form': form,
        'application_practitioner': application_practitioner,
        'idea_practitioner': idea_practitioner,
    }
    return render(request, 'users_page/practitioner_home.html', context)


@login_required(login_url='login')
def staff_update(request):
    startapper = Staff.objects.get(user=request.user)
    form = StartapperUpdateForm(instance=startapper)
    if request.method == 'GET':
        return render(request, 'profile_update.html', {'form': form})
    else:
        form = StartapperUpdateForm(request.POST, request.FILES, instance=startapper)
        if form.is_valid():
            form.save()
        return redirect('startapper_home')


@login_required(login_url='login')
def startapper_home(request):
    try:
        startapper = Startapper.objects.get(user=request.user)
        idea_startapper = IdeaStartapper.objects.filter(user=startapper)
    except:
        messages.warning(request, 'you go to developer page')
        return redirect('home')

    if request.method == 'POST':
        form = IdeaStartapperForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            current_user = Startapper.objects.get(user=request.user)
            data = IdeaStartapper()
            data.title = form.cleaned_data['title']
            data.description = form.cleaned_data['description']
            if request.FILES:
                data.file = request.FILES['file']
            else:
                data.file = form.cleaned_data['file']
            # data.file = request.FILES['file'] or form.cleaned_data['file']
            data.user = current_user
            data.save()
            return redirect('startapper_home')
        else:
            messages.warning(request, 'Error idea!')
            return redirect('ideastartapper')
    form = IdeaStartapperForm()
    return render(request, 'users_page/startapper_home.html',
                  {'startapper': startapper, 'form': form, 'idea_startapper': idea_startapper})


@login_required(login_url='login')
def startapper_update_(request):
    startapper = Startapper.objects.get(user=request.user)
    form = StartapperUpdateForm(instance=startapper)
    if request.method == 'GET':
        return render(request, 'profile_update.html', {'form': form})
    else:
        form = StartapperUpdateForm(request.POST, request.FILES, instance=startapper)
        if form.is_valid():
            form.save()
        return redirect('startapper_home')


@login_required(login_url='/login')
def user_update(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'You profile successfully updated!')
            return HttpResponseRedirect(url)
    else:
        form = UserUpdateForm(instance=request.user)
        return render(request, 'user_update.html', {'form': form})


@login_required(login_url='/login')
def user_password(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your profile password successfully updated')
            return redirect(url)
        else:
            messages.error(request, 'Eror password')
            return redirect('user-password')
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'user_password.html', {'form': form})


class StartapperUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        startapper = Startapper.objects.get(user=self.request.user)
        form = StartapperUpdateForm(instance=startapper)
        context = {'form': form}
        return render(request, 'profile_update.html', context)

    def post(self, *args, **kwargs):
        form = StartapperUpdateForm(self.request.POST, self.request.FILES, instance=self.request.user.startapper)
        if form.is_valid():
            print(form)
            form.save()
            return redirect(reverse('startapper_home'))
        return redirect('home')


def success_projects(request):
    s_p = SuccessProjects.objects.all().order_by('-id')[:20]
    return render(request, 'success_projects.html', {'s_p': s_p})


def success_project_detail(request, pk):
    project = SuccessProjects.objects.get(pk=pk)
    comment = CommentOfPost.objects.filter(post_id=pk)
    return render(request, 'project_detail.html', {'project': project, 'comment': comment})


def comment_of_post(request, pk):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = CommentOfPost()
            data.comment = form.cleaned_data['comment']
            data.post_id = pk
            current_user = request.user
            data.owner_id = current_user.id
            data.save()
            messages.success(request, 'Your comment successfully send!')
            return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)


def about_us(request):
    about = AboutUS.objects.get(pk=1)
    return render(request, 'about_us.html', {'about': about})


def contact_prowork(request):
    contact = ContacktsProwork.objects.get(pk=1)
    return render(request, 'contacts_prowork.html', {'contact': contact})

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, FormView, RedirectView, DetailView, UpdateView
from .models import User, Profile
from .forms import UserRegistrationForm, ProfileForm, UserLoginForm
from django.template.loader import get_template



# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = 'accounts:login'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        return reverse(self.success_url)

    def get(self, request, *args, **kwargs):
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
        return render(request, 'accounts/register.html', {'user_form' : user_form, 'profile_form' : profile_form})

    def post(self, request, *args, **kwargs):
        if User.objects.filter(username=request.POST['username']).exists():
            messages.warning(request, "This username exists! Please retry another ...")
            return redirect('accounts:register')
        if User.objects.filter(email=request.POST['email']).exists():
            messages.warning(request, "This email exists")
            return redirect('accounts:register')

        user_form = UserRegistrationForm(request.POST or None, request.FILES or None)
        profile_form = ProfileForm(request.POST or None, request.FILES or None)

        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save()
            new_profile_user = Profile.objects.get(user_id=new_user.id)
            profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=new_profile_user)
            if profile_form.is_valid():
                profile_form.save()
            messages.success(request, "Successfully registered")
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(self.get_success_url())
        else:
            print(user_form.errors + profile_form.errors)
            return render(request, 'accounts/register.html', {'user_form' : user_form, 'profile_form' : profile_form})

class LoginView(FormView):
    form_class = UserLoginForm
    success_url = ''
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        return reverse(self.success_url)

    def get(self, request):
        return render(request, template_name='accounts/login.html')


    def post(self, request, *args, **kwargs):
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.warning(request, "This user doesn't exist")
                return redirect('accounts:login')
            if not user.check_password(password):
                messages.warning(request, "Password doesn't match")
                return redirect('accounts:login')
            if user.is_active is False:
                messages.warning(request, "This user is not Active")
                return redirect('accounts:login')
            return redirect(self.get_success_url())





class LogoutView(RedirectView):
    url = reverse_lazy('accounts:login')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You're logged out")
        return super(LogoutView, self).get(request, *args, **kwargs)





class ProfileView(DetailView):
    model = User
    template_name = 'accounts/profile.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.model.objects.select_related('profile').prefetch_related("post").get(id=self.kwargs.get(self.slug_url_kwarg))

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context =  self.get_context_data(object=self.object)
        return self.render_to_response(context)

class UpdateProfile(UpdateView):
    model = Profile
    template_name = 'accounts/edit_profile.html'
    context_object_name = 'form'
    object = None
    fields = '__all__'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        user_form = UserRegistrationForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user)
        context = self.get_context_data(**kwargs)
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        return self.render_to_response(context)



    def post(self, request, *args, **kwargs):
        pass























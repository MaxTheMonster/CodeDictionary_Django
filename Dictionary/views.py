from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views import generic
from django.template.context_processors import csrf
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from Dictionary import models
from Dictionary import forms


class EnsureCsrfCookieMixin(object):
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(EnsureCsrfCookieMixin, self).dispatch(*args, **kwargs)


class IndexView(EnsureCsrfCookieMixin, generic.TemplateView):
    template_name = "Dictionary/index.html"


class CreateWordView(LoginRequiredMixin, generic.CreateView):
    template_name = "Dictionary/submit.html"
    form_class = forms.CreateWordForm
    success_url = '/'
    #model = models.Word

    def form_valid(self, form):
        print("VALID")
        try:
            category_check = models.Category.objects.get(name=form.instance.category)
            form.instance.category = category_check
            print("Exists")

        except ObjectDoesNotExist:
            new_category = models.Category(name=form.instance.category)
            new_category.save()
            form.instance.category = new_category
            print("New") 
            
        form.instance.user = self.request.user
        return super(CreateWordView, self).form_valid(form)

    def form_invalid(self, form):
        print("invalid")
        return super(CreateWordView, self).form_valid(form)


class WordDetailView(generic.DetailView):
    model = models.Word
    template_name = "Dictionary/word_detail.html"

class SearchWordsView(generic.ListView):
    model = models.Word


class ProfileView(generic.DetailView):
    template_name = "users/profile.html"
    model = models.User
    slug_field = 'username'

class RegisterView(generic.CreateView):
    template_name = "users/register.html"
    form_class = forms.UserCreationForm
    success_url = "/login/"

    def form_valid(self, form):
        new_user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'],
                               )
        login(self.request, new_user)
        return HttpResponseRedirect("/dashboard/")


class LoginView(generic.FormView):
    template_name = "users/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("index")

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect("index")
        else:
            request.session.set_test_cookie()

            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())

        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)


class LogoutView(generic.RedirectView):
  url = "/"

  def get(self, request, *args, **kwargs):
    logout(request)
    return super(LogoutView, self).get(request, *args, **kwargs)

def search_words(request):
    if request.method == "POST":
        if request.POST["search_text"] == "":
            search_text = ""
        else:
            search_text = request.POST["search_text"]
    else:
        search_text = ''
    words = models.Word.objects.filter(name__contains=search_text)
    
    if not words.exists():
        error = "Hmmm... There aren't any words like that. Try submitting one if you recognise it."
        return render(request, "ajax_search.html", {"error": error})

    else:
        return render(request, "ajax_search.html", {"words": words})


# class SearchView():
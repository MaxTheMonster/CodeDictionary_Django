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
    success_url = reverse_lazy("index")
    #model = models.Word

    def form_valid(self, form):
        form.instance.user_creator = self.request.user

        return super(CreateWordView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.cleaned_data)
        print(form.instance)
        print(form.instance.name)
        print(form.instance.definition)

        return super(CreateWordView, self).form_invalid(form)

    # def post(self, request, *args, **kwargs):
    #     print("POSTTTT")

    #     data = request.POST
    #     print(data["category"])
    #     form = self.get_form()
        
    #     if form.is_valid():
    #         print("VALID")

    #         try:
    #             category_check = models.Category.objects.get(name=data["category"])
    #             print("Exists")

    #         except models.Category.DoesNotExist:
    #             print("Does Not Exist, creating")
    #             # new_category = models.Category(name=form.instance.category)
    #             new_category = models.Category.objects.create(name=data["category"])
    #             new_category.save()
    #             print("Created")
    #             print(new_category)

    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)


    # def form_valid(self, form):
    #     form.instance.user_creator = self.request.user
        

    #     return super(CreateWordView, self).form_valid(form)

    # def form_invalid(self, form):
    #     print("Invalid")
    #     form.instance.user_creator = self.request.user
       
            
    #     return super(CreateWordView, self).form_valid(form)


class WordDetailView(generic.DetailView):
    model = models.Word
    template_name = "Dictionary/word_detail.html"


class SearchWordsView(generic.ListView):
    model = models.Word


class CategoryView(generic.DetailView):
    template_name = "Dictionary/categories.html"
    model = models.Category
    slug_field = 'name'


class ProfileView(generic.DetailView):
    template_name = "users/profile.html"
    model = models.User
    slug_field = 'username'
    context_object_name = 'viewed_user'

    def dispatch(self, request, *args, **kwargs):
        self.current_user = models.User.objects.get(username=self.kwargs["slug"])
        self.user_words = models.Word.objects.filter(user=self.current_user).order_by("-published")
        return super(ProfileView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context["words"] = self.user_words
        return context

class RegisterView(generic.CreateView):
    template_name = "users/register.html"
    form_class = forms.UserCreationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'],
                               )
        #login(self.request, user)
        return super(RegisterView, self).form_valid(form)


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

def search_categories(request):
    if request.method == "POST":
        if request.POST["search_text"] == "":
            search_text = ""
        else:
            search_text = request.POST["search_text"]
    else:
        search_text = ''
    categories = models.Category.objects.filter(name__contains=search_text).values()

    print(categories)
    
    if not categories.exists():
        error = "This is a new tag, it will be created."
        return render(request, "Dictionary/category_search.html", {"error": error})

    else:
        return render(request, "Dictionary/category_search.html", {"categories": categories})
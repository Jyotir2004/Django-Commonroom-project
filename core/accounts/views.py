from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import RegistrationForm, UsernameOrEmailAuthenticationForm


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Your account is ready. Log in to enter Commonroom.')
        return redirect('login')
    return render(request, 'accounts/register.html', {'form': form})


class CommonroomLoginView(LoginView):
    authentication_form = UsernameOrEmailAuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


@login_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')

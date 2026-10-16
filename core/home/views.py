from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import CarForm
from .models import MemberStatus, WorkspaceInvite, car
from .utils import dashboard_context
# Create your views here.


@login_required
def home(request):
    context = dashboard_context(request.user)
    context['cars'] = car.objects.filter(
        Q(owner=request.user) | Q(owner__isnull=True)
    ).order_by('?')
    context['car_form'] = CarForm()
    return render(request, 'index.html', context)


@login_required
def overview(request):
    context = dashboard_context(request.user)
    context['cars'] = car.objects.filter(
        Q(owner=request.user) | Q(owner__isnull=True)
    ).order_by('?')
    return render(request, 'overview.html', context)


@login_required
def about(request):
    return render(request, 'about.html')


@login_required
def contact(request):
    return render(request, 'contact.html')


@login_required
def invite_person(request):
    if request.method != 'POST':
        return render(request, 'invite.html')

    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip().lower()
    role = request.POST.get('role', '').strip() or 'Team member'
    team = request.POST.get('team', '').strip() or 'Unassigned'
    errors = []

    if not name:
        errors.append('Enter a name.')
    try:
        validate_email(email)
    except ValidationError:
        errors.append('Enter a valid email address.')

    existing_people = dashboard_context(request.user)['people']
    if any(person['email'].lower() == email for person in existing_people):
        errors.append('Someone with this email is already in the directory.')

    if errors:
        return render(request, 'invite.html', {
            'errors': errors,
            'form_data': {'name': name, 'email': email, 'role': role, 'team': team},
        })

    WorkspaceInvite.objects.create(
        owner=request.user,
        name=name,
        email=email,
        role=role,
        team=team,
    )
    messages.success(request, f'Invitation for {name} was added to the directory.')
    return redirect('home')


@login_required
@require_POST
def delete_invite(request, invite_id):
    invite = get_object_or_404(WorkspaceInvite, pk=invite_id, owner=request.user)
    invite.delete()
    messages.success(request, 'The invited person was removed from the directory.')
    return redirect('home')


@login_required
@require_POST
def add_car(request):
    form = CarForm(request.POST)
    if form.is_valid():
        new_car = form.save(commit=False)
        new_car.owner = request.user
        new_car.save()
        messages.success(request, f'{new_car.car_name} was added.')
        return redirect('home')
    context = dashboard_context(request.user)
    context['cars'] = car.objects.filter(
        Q(owner=request.user) | Q(owner__isnull=True)
    ).order_by('?')
    context['car_form'] = form
    return render(request, 'index.html', context, status=400)


@login_required
@require_POST
def toggle_car(request, car_id):
    selected_car = get_object_or_404(car, pk=car_id, owner=request.user)
    selected_car.is_active = not selected_car.is_active
    selected_car.save(update_fields=['is_active'])
    return redirect('home')


@login_required
@require_POST
def toggle_member_status(request):
    status, _created = MemberStatus.objects.get_or_create(user=request.user)
    status.is_available = not status.is_available
    status.save(update_fields=['is_available'])
    messages.success(
        request,
        f'Your status is now {"active" if status.is_available else "inactive"}.',
    )
    return redirect('home')


@login_required
def success_page(_request):
    return HttpResponse('<h1>Success!page</h1>')
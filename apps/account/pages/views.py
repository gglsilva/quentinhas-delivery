from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..forms import UserRegistrationForm, UserEditForm, ProfileEditForm
# from actions.utils import create_action
from apps.account.models import Profile


# @login_required
# def dashboard(request):
#     template_name = 'account/dashboard.html'
#     return render(request, template_name, {'section':'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            # create_action(new_user, 'has created an account')
            return render(request,
                        'account/register_done.html',
                        {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                    'account/register.html',
                    {'user_form':user_form})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user,
                                data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        
    else:
        user_form = UserEditForm(
            instance=request.user
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile
        )
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form':profile_form})
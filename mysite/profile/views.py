from django.shortcuts import redirect, render

from .forms import UserForm, ProfileForm
from order.models import Order
from .models import Profile


def view_profile(request):
    user_detail = request.user
    return render(request, 'profile/profile_detail.html', {
        'user_detail': user_detail,
    })


def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile-detail')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile/profile_form.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def view_orders(request):
    # user_profile = Profile.objects.get(pk=profile_id)
    user_profile = Profile.objects.get(user=request.user)
    order_list = Order.objects.filter(user_orders=user_profile)
    return render(request, 'profile/profile_order.html', {
        'profile_order_list': order_list
    })

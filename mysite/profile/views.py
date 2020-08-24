from django.shortcuts import redirect, render
from django.views.generic import ListView

from order.models import Order
from .forms import UserForm, ProfileForm


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


class ProfileOrderList(ListView):
    model = Order
    template_name = "profile/profile_order.html"
    paginate_by = 9

    def get_queryset(self):
        if self.kwargs['filter'] != 'all':
            return Order.objects.filter(user_orders=self.request.user.profile,
                                        order_state=self.kwargs['filter']).order_by('date_created')
        else:
            return Order.objects.filter(user_orders=self.request.user.profile).order_by('date_created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_states'] = Order.OrderState
        context['active_tab'] = self.kwargs['filter'] + "-tab"
        return context

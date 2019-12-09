from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

from orders.models import Order


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт создан! '
            f'{username} теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):

    return render(request, 'users/profile.html')


@login_required
def change_phone_or_image(request):
    if request.method == 'POST':
        # u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid(): # and u_form.is_valid():
            # u_form.save()
            p_form.save()
            messages.success(request, f'Ваш аккаунт обновлен!')
            return redirect('users:profile')
    else:
        # u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        # 'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/change_phone_or_image.html', context)


@login_required
def page_ordered_goods(request):
    user_orders = Order.objects.filter(email=request.user.email,
                                       order_processed=True)
    orders = []
    for i in range(len(user_orders)):
        orders.append(get_object_or_404(Order, id=user_orders[i].id))
    # order = order.items.all()

    context = {
        'orders': orders
    }

    return render(request, 'users/page_ordered_goods.html', context)

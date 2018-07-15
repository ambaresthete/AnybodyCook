from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from .forms import AddressForm
from billing.models import BillingProfile
# Create your views here.

def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        "form" : form
    }
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_url = next_ or next_post or None
    if form.is_valid():
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=request.user, email=request.user.email)
        if billing_profile is not None:
            address_type = request.POST.get('address_type', 'shipping')
            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()
            request.session[address_type + "_address_id"] = instance.id
        else:
            print("error")
            return redirect("cart:checkout")      
        if is_safe_url(redirect_url, request.get_host()):
            return redirect(redirect_url)
        else:
            return redirect("cart:checkout")
    return redirect("cart:checkout")

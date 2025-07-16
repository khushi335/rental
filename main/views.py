from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Property, Inquiry, Favorite, Category, Review, ShiftHome, Contact, Report
from .forms import PropertyForm , ShiftHomeForm , FindMeRoomForm,InquiryForm,ReviewForm
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

CustomUser = get_user_model()
RATING_RANGE = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

def index(request):
    categories = Category.objects.all()
    selected_category_id = request.GET.get('category')
    if selected_category_id:
        properties = Property.objects.filter(category_id=selected_category_id, is_approved=True)
        selected_category = Category.objects.filter(id=selected_category_id).first()
    else:
        properties = Property.objects.filter(is_approved=True)
        selected_category = None
    paginator = Paginator(properties, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    hot_deals = Property.objects.filter(is_hot_deal=True, is_approved=True)
    return render(request, 'main/index.html', { 'categories': categories, 'hot_deals': hot_deals, 'page_obj': page_obj, 'selected_category': selected_category })

def index_landlord(request):
    categories = Category.objects.all()
    selected_category_id = request.GET.get('category')
    if selected_category_id:
        properties = Property.objects.filter(category_id=selected_category_id, is_approved=True)
        selected_category = Category.objects.filter(id=selected_category_id).first()
    else:
        properties = Property.objects.filter(is_approved=True)
        selected_category = None
    paginator = Paginator(properties, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    hot_deals = Property.objects.filter(is_hot_deal=True, is_approved=True)
    return render(request, 'main/index_landlord.html', { 'categories': categories, 'hot_deals': hot_deals, 'page_obj': page_obj, 'selected_category': selected_category })


@login_required(login_url='log_in')
def about_us(request):
    return render(request,"main/about_us.html")

@login_required(login_url='log_in')
def contact(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']

        # Save the message to database
        user = Contact(name=name, email=email, phone=phone, message=message)
        user.save()

        # From email
        from_email = settings.DEFAULT_FROM_EMAIL,

        # ✅ Email to the user (thank-you message)
        user_subject = 'Connect with us'
        user_message = "Thank you for your message/feedback. Your review means a lot."
        send_mail(user_subject, user_message, from_email, [email], fail_silently=False)

        # ✅ Email to all landlords
        landlord_subject = 'New Contact Submission'
        landlord_message = f"A user named {name} has submitted a message:\n\n{message}"
        landlord_emails = CustomUser.objects.filter(is_landlord=True).values_list('email', flat=True)
        send_mail(landlord_subject, landlord_message, from_email, landlord_emails, fail_silently=False)

        # ✅ Email to all admins (superusers)
        admin_subject = 'New Contact Submission (Admin Copy)'
        admin_message = f"A message was submitted by {name} ({email}):\nPhone: {phone}\n\n{message}"
        admin_emails = CustomUser.objects.filter(is_superuser=True).values_list('email', flat=True)
        send_mail(admin_subject, admin_message, from_email, admin_emails, fail_silently=False)

        # Show success message and redirect
        messages.success(request, 'Thank you for contacting us.')
        return redirect('contact')

    return render(request, 'main/contact.html')

@login_required(login_url='log_in')
def contact_landlord(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']

        # Save the message to database
        user = Contact(name=name, email=email, phone=phone, message=message)
        user.save()

        # From email
        from_email = settings.DEFAULT_FROM_EMAIL,

        # ✅ Email to the user (thank-you message)
        user_subject = 'Connect with us'
        user_message = "Thank you for your message/feedback. Your review means a lot."
        send_mail(user_subject, user_message, from_email, [email], fail_silently=False)

        # ✅ Email to all landlords
        landlord_subject = 'New Contact Submission'
        landlord_message = f"A user named {name} has submitted a message:\n\n{message}"
        landlord_emails = CustomUser.objects.filter(is_landlord=True).values_list('email', flat=True)
        send_mail(landlord_subject, landlord_message, from_email, landlord_emails, fail_silently=False)

        # ✅ Email to all admins (superusers)
        admin_subject = 'New Contact Submission (Admin Copy)'
        admin_message = f"A message was submitted by {name} ({email}):\nPhone: {phone}\n\n{message}"
        admin_emails = CustomUser.objects.filter(is_superuser=True).values_list('email', flat=True)
        send_mail(admin_subject, admin_message, from_email, admin_emails, fail_silently=False)

        # Show success message and redirect
        messages.success(request, 'Thank you for contacting us.')
        return redirect('contact')

    return render(request, 'main/contact_landlord.html')

@login_required(login_url='log_in')
def property_list_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    categories = Category.objects.all()

    if request.user.is_staff:
        properties = Property.objects.filter(category=category)
    else:
        properties = Property.objects.filter(
            category=category,
            is_approved=True
        )

    return render(request, 'main/property_list_by_category.html', {
        'properties': properties,
        'category': category,
        'categories': categories
    })

@login_required(login_url='log_in')
def find_me_room(request):
    if request.method == 'POST':
        form = FindMeRoomForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()

            # ✅ Email to Admin
            admin_subject = 'New Room Request Submitted'
            admin_message = f"""
New room request details:

Name: {instance.full_name}
Email: {instance.email}
Phone: {instance.phone}
Preferred Location: {instance.preferred_location}
Room Type: {instance.get_room_type_display()}
Price Range: Rs. {instance.price_min} - Rs. {instance.price_max}
Message: {instance.message or 'No message'}
Deposit Slip: {'Yes' if instance.deposit_slip else 'No'}

Submitted via Find Me Room page.
"""
            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False
            )

            # ✅ Email to User
            user_subject = 'We’ve Received Your Room Request'
            user_message = f"""
Hello {instance.full_name},

Thanks for filling out the Find Me Room form! 🎉

We’ll review your request and get back to you soon.

Here’s what you submitted:

Preferred Location: {instance.preferred_location}
Room Type: {instance.get_room_type_display()}
Price Range: Rs. {instance.price_min} – Rs. {instance.price_max}
Message: {instance.message or 'No additional message'}

We’ll contact you at {instance.phone} or {instance.email} once we match you with a suitable room.

- Rental Platform Team
"""
            send_mail(
                subject=user_subject,
                message=user_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=False
            )

            messages.success(request, "Your request has been submitted successfully!")
            return redirect('find_me_room')
    else:
        form = FindMeRoomForm()

    return render(request, 'main/find_me_room.html', {'form': form})

@login_required(login_url='log_in')
def property_list_landlord(request):
    """List properties with filtering, pagination, and favorites."""
    properties = Property.objects.all().order_by('-id').prefetch_related('reviews', 'category')

    location = request.GET.get('location')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if location:
        properties = properties.filter(location__icontains=location)
    if category:
        properties = properties.filter(category__name__iexact=category)
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)

    paginator = Paginator(properties, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    fav_ids = Favorite.objects.filter(user=request.user).values_list('property_id', flat=True)

    for prop in page_obj:
        prop.is_favorited = prop.id in fav_ids
        prop.user_review = prop.reviews.filter(user=request.user).first()

    return render(request, 'main/property_list_landlord.html', {
        'properties': page_obj,
        'location': location,
        'category': category,
    })


@login_required(login_url='log_in')
def shift_home(request):
    if request.method == 'POST':
        form = ShiftHomeForm(request.POST, request.FILES)
        if form.is_valid():
            shift_request = form.save(commit=False)
            shift_request.user = request.user
            shift_request.save()

            # ✅ Email to Admin
            admin_subject = "New Shift Request Submitted"
            admin_message = f"""
New shift request details:

User: {request.user.username} ({request.user.email})
From Location: {shift_request.from_location}
To Location: {shift_request.to_location}
Phone: {shift_request.phone}
Email: {shift_request.email}

Property Type: {shift_request.property_type}
Booking Date & Time: {shift_request.schedule_date} at {shift_request.schedule_time}
Message: {shift_request.message or 'No message'}
Deposit Slip Uploaded: {'Yes' if shift_request.deposit_slip else 'No'}

Submitted via Shift Home page.
"""
            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            # ✅ Email to User
            user_subject = "We've Received Your Shift Request"
            user_message = f"""
Hello {request.user.username},

Thank you for submitting your shift request from {shift_request.from_location} to {shift_request.to_location}.

Here are the details you submitted:

Property Type: {shift_request.property_type}
Booking Date & Time: {shift_request.schedule_date} at {shift_request.schedule_time}
Message: {shift_request.message or 'No additional message'}

We will review your request and get back to you shortly.

If you need to contact us, we will use the phone number {shift_request.phone} or email {shift_request.email}.

Best regards,
Rental Platform Team
"""
            send_mail(
                subject=user_subject,
                message=user_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[shift_request.email],
                fail_silently=False,
            )

            messages.success(request, "Your shift request has been submitted successfully.")
            return redirect('shift_success')
    else:
        form = ShiftHomeForm()

    # Organized form field groups for use in template
    item_fields = [
        'beds', 'cupboards', 'tvs', 'dining_tables', 'tea_tables', 'kitchen_racks',
        'sofas', 'chairs', 'shoe_racks', 'dressing_tables', 'table_lamps',
        'gas_cylinders', 'mattresses', 'refrigerator', 'heaters', 'table_fans',
        'flower_pots', 'computer_tables', 'cookware'
    ]

    main_info_fields = ['property_type', 'from_location', 'to_location', 'phone', 'email']
    location_fields = ['from_floor', 'to_floor']
    booking_time_fields = ['when', 'schedule_date', 'schedule_time']
    optional_upload_fields = ['deposit_slip', 'message']

    context = {
        'form': form,
        'item_fields': item_fields,
        'main_info_fields': main_info_fields,
        'location_fields': location_fields,
        'booking_time_fields': booking_time_fields,
        'optional_upload_fields': optional_upload_fields,
    }
    return render(request, 'main/shift_home.html', context)

@login_required(login_url='log_in')
def shift_success(request):
    return render(request, 'main/shift_success.html')

@login_required(login_url='log_in')
def property_list(request):
    properties = Property.objects.all().order_by('-id')\
        .prefetch_related('reviews', 'category')

    # Filter
    query = request.GET.get('q')
    location = request.GET.get('location')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if location:
        properties = properties.filter(location__icontains=location)
    if category:
        properties = properties.filter(category__name__iexact=category)
    if min_price:
        properties = properties.filter(price__gte=min_price)
    
    if max_price:
        properties = properties.filter(price__lte=max_price)

    # Pagination
    paginator = Paginator(properties, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    # Favorite properties
    fav_ids = Favorite.objects.filter(user=request.user).values_list('property_id', flat=True)

    for prop in page_obj:
        prop.is_favorited = prop.id in fav_ids
        prop.user_review = prop.reviews.filter(user=request.user).first()

    return render(request, 'main/property_list.html', {
        'properties': page_obj,
        'location': location,
        'category': category,
    })

@login_required(login_url='log_in')
def property_detail(request, property_id):
    prop = get_object_or_404(Property, id=property_id)
    reviews = prop.reviews.select_related('user').order_by('-created_at')
    user_review = reviews.filter(user=request.user).first()
    similar = Property.objects.filter(category=prop.category).exclude(id=prop.id)[:3]
    is_favorited = prop.favorited_by.filter(pk=request.user.pk).exists()
    inquiry_form = InquiryForm()

    # Handle inquiry submission
    if request.method == "POST" and 'inquiry_submit' in request.POST:
        inquiry_form = InquiryForm(request.POST)
        if inquiry_form.is_valid():
            inquiry = inquiry_form.save(commit=False)
            inquiry.property = prop
            inquiry.user = request.user
            inquiry.save()

            # Send email to Admin
            admin_subject = f"New Inquiry for: {prop.title} (ID: {prop.id})"
            admin_message = f"""
New Inquiry Submitted:

Property: {prop.title}
Property ID: {prop.id}
Property Link: https://127.0.0.1:8000/property/{prop.id}

User: {request.user.username}
Email: {inquiry.email}
Phone: {inquiry.phone if hasattr(inquiry, 'phone') else 'N/A'}
Message: {inquiry.message}

Submitted from: {prop.location}
"""
            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False
            )

            # Send email to User
            user_subject = "We've Received Your Inquiry"
            user_message = f"""
Hello {request.user.username},

Thank you for your interest in: {prop.title}.

We have received your inquiry and will get back to you soon.

Here's a copy of your message:
"{inquiry.message}"

We’ll contact you at {inquiry.email} if needed.

Best regards,
Rental Platform Team
"""
            send_mail(
                subject=user_subject,
                message=user_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[inquiry.email],
                fail_silently=False
            )

            messages.success(request, "Your inquiry has been sent successfully!")
            return redirect('property_detail', property_id=property_id)
        else:
            messages.error(request, "Please correct the errors in the inquiry form.")

    # Handle new review submission
    if request.method == "POST" and 'review_submit' in request.POST and not user_review:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.property = prop
            review.save()
            messages.success(request, "Your review was added.")
            return redirect('property_detail', property_id=property_id)
        else:
            messages.error(request, "Please correct the review form.")
    else:
        review_form = ReviewForm()

    context = {
        'property': prop,
        'reviews': reviews,
        'user_review': user_review,
        'similar_properties': similar,
        'is_favorited': is_favorited,
        'inquiry_form': inquiry_form,
        'review_form': review_form,
    }
    return render(request, 'main/property_detail.html', context)

@login_required(login_url='log_in')
def add_property(request):
    form = PropertyForm(request.POST or None, request.FILES or None)
    if request.method=='POST' and form.is_valid():
        prop = form.save(commit=False)
        prop.owner = request.user
        prop.save()
        messages.success(request, 'Property added successfully!')
        return redirect('landlord_dashboard')
    return render(request, 'main/add_property.html', {'form': form})

@login_required(login_url='log_in')
def edit_property(request, pk):
    prop = get_object_or_404(Property, pk=pk, owner=request.user)
    form = PropertyForm(request.POST or None, request.FILES or None, instance=prop)
    if request.method=='POST' and form.is_valid():
        form.save()
        return redirect('landlord_dashboard')
    return render(request, 'main/edit_property.html', {'form': form})

@login_required(login_url='log_in')
def delete_property(request, pk):
    prop = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method=='POST':
        prop.delete()
        return redirect('landlord_dashboard')
    return render(request, 'main/delete_property.html', {'property': prop})

@login_required(login_url='log_in')
def toggle_favorite(request, property_id):
    prop = get_object_or_404(Property, id=property_id)
    fav = Favorite.objects.filter(user=request.user, property=prop).first()
    if fav:
        fav.delete()
        messages.success(request, f'Removed "{prop.title}" from your favorites.')
    else:
        Favorite.objects.create(user=request.user, property=prop)
        messages.success(request, f'Added "{prop.title}" to your favorites.')
    return redirect(request.GET.get('next') or 'property_list')

# @login_required(login_url='log_in')
# def toggle_favorite(request, property_id):
#     prop = get_object_or_404(Property, id=property_id)
#     fav = Favorite.objects.filter(user=request.user, property=prop).first()
#     if fav:
#         fav.delete()
#         messages.success(request, f'Removed "{prop.title}" from your favorites.')
#     else:
#         Favorite.objects.create(user=request.user, property=prop)
#         messages.success(request, f'Added "{prop.title}" to your favorites.')

#     # Try to redirect to the exact same page the user was on
#     next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER') or 'property_list'
#     return redirect(next_url)

@login_required(login_url='log_in')
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('property')
    return render(request, 'main/favorite_list.html', {'favorites': favorites})

@login_required(login_url='log_in')
def landlord_dashboard(request):
    if getattr(request.user, 'is_landlord', False) is False:
        return redirect('tenant_dashboard')
    properties = Property.objects.filter(owner=request.user)
    inquiries = Inquiry.objects.filter(property__in=properties).order_by('created_at')
    return render(request, 'main/landlord_dashboard.html', {'properties': properties, 'inquiries': inquiries})

@login_required(login_url='log_in')
def tenant_dashboard(request):
    if getattr(request.user, 'is_landlord', True):
        return redirect('landlord_dashboard')
    inquiries = Inquiry.objects.filter(user=request.user).select_related('property').order_by('created_at')
    favorites = Favorite.objects.filter(user=request.user).select_related('property')
    return render(request, 'main/tenant_dashboard.html', {'inquiries': inquiries, 'favorites': favorites})

def tenant_shift_dashboard(request):
    shift_requests = ShiftHome.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tenant/tenant_shift_dashboard.html', {'shift_requests': shift_requests})

@login_required(login_url='log_in')
def add_or_update_review(request, property_id):
    prop = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if not (rating and comment):
            messages.error(request, "Please provide both a rating and a comment.")
            # Re-render property detail with error message
            reviews = prop.reviews.all().order_by('-created_at')
            user_review = reviews.filter(user=request.user).first()
            similar = Property.objects.filter(category=prop.category).exclude(id=prop.id)[:3]
            is_favorited = prop.favorited_by.filter(pk=request.user.pk).exists()
            return render(request, 'main/property_detail.html', {
                'property': prop,
                'reviews': reviews,
                'user_review': user_review,
                'similar_properties': similar,
                'is_favorited': is_favorited,
                'rating_range': RATING_RANGE,
            })
        else:
            review, created = Review.objects.update_or_create(
                property=prop,
                user=request.user,
                defaults={'rating': rating, 'comment': comment}
            )
            messages.success(request, "Review submitted successfully!" if created else "Review updated successfully!")
            return redirect('property_detail', property_id=property_id)

@login_required(login_url='log_in')
def delete_review(request, property_id):
    prop = get_object_or_404(Property, id=property_id)
    Review.objects.filter(property=prop, user=request.user).delete()
    messages.success(request, "Review deleted successfully.")
    return redirect('property_detail', property_id=property_id)

# @login_required(login_url='log_in')
# @require_POST
# def delete_review(request, property_id):
#     prop = get_object_or_404(Property, id=property_id)
#     review = prop.reviews.filter(user=request.user).first()
#     if review:
#         review.delete()
#         messages.success(request, "Your review was deleted.")
#     return redirect('property_detail', property_id=property_id)


@login_required(login_url='log_in')
def landlord_inquiries(request):
    if not request.user.is_landlord:
        return redirect('tenant_dashboard')
    
    inquiries = Inquiry.objects.filter(landlord=request.user).select_related('tenant', 'property').order_by('-created_at')
    return render(request, 'main/landlord_inquiries.html', {'inquiries': inquiries})

@login_required(login_url='log_in')
def user_reviews(request):
    reviews = Review.objects.filter(user=request.user).select_related('property').order_by('-created_at')
    return render(request, 'main/reviews.html', {'reviews': reviews})

def privacy_policy(request):
    return render(request, 'main/privacy_policy.html')

def terms_and_conditions(request):
    return render(request, 'main/terms_and_conditions.html')

@login_required(login_url='log_in')
def report_property(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)

    # Avoid duplicate reports from the same user
    if Report.objects.filter(user=request.user, property=property_obj).exists():
        messages.info(request, "You have already reported this property.")
    else:
        Report.objects.create(user=request.user, property=property_obj)

        # Send email notification to admin (update admin email accordingly)
        recipient_list = [email for _, email in getattr(settings, 'ADMINS', [])] or ['admin@example.com']
        send_mail(
            subject='New Property Report',
            message=f'User {request.user.username} reported property "{property_obj.title}" (ID: {property_obj.id}). Please review.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=True,
        )

        messages.success(request, "This property has been reported and will be reviewed soon.")

    next_url = request.POST.get('next') or redirect('property_detail', property_id=property_id)
    return redirect(next_url)

@login_required(login_url='log_in')  # Adjust login URL name as needed
def settings(request):
    # No special logic needed here for theme toggle, all handled client-side
    return render(request, 'main/settings.html')
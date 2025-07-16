from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Property, Inquiry, Favorite, Category, Review
from .forms import PropertyForm

# Create your views here.

def index(request):
    categories = Category.objects.all()
    selected_category_id = request.GET.get('category')
    
    if selected_category_id:
        properties = Property.objects.filter(category_id=selected_category_id, is_approved=True)
        selected_category = Category.objects.filter(id=selected_category_id).first()
    else:
        properties = Property.objects.filter(is_approved=True)
        selected_category = None

    paginator = Paginator(properties, 12)  # 24 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    hot_deals = Property.objects.filter(is_hot_deal=True, is_approved=True)

    return render(request, 'main/index.html', {
        'categories': categories,
        'hot_deals': hot_deals,
        'page_obj': page_obj,
        'selected_category': selected_category,
    })
# def index(request):
#     hot_deals = Property.objects.filter(is_hot_deal=True, is_approved=True)
#     categories = Category.objects.all()
#     return render(request, 'main/index.html', {'hot_deals': hot_deals, 'categories': categories})

def property_list_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    properties = Property.objects.filter(category=category, is_approved=True)
    categories = Category.objects.all()  # Optional, to show categories in sidebar
    return render(request, 'main/property_list_by_category.html', {
        'properties': properties,
        'category': category,
        'categories': categories,
    })

def find_me_room(request):
    return render(request,"main/find_me_room.html")

@login_required
def property_list(request):
    properties = Property.objects.all().order_by('-id')

    # Filtering by location and category if provided
    location = request.GET.get('location')
    category = request.GET.get('category')
    if location:
        properties = properties.filter(location__icontains=location)
    if category:
        properties = properties.filter(category__name__iexact=category)

    paginator = Paginator(properties, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Mark favorited properties dynamically
    if request.user.is_authenticated:
        favorites = set(Favorite.objects.filter(user=request.user).values_list('property_id', flat=True))
        for prop in page_obj:
            prop.is_favorited = prop.id in favorites
    else:
        for prop in page_obj:
            prop.is_favorited = False

    return render(request, 'main/property_list.html', {'properties': page_obj})

# @login_required
# def property_list(request):
#     properties = Property.objects.filter(is_approved=True).order_by('-created_at')

#     location = request.GET.get('location')
#     category = request.GET.get('category')
#     min_price = request.GET.get('min_price')
#     max_price = request.GET.get('max_price')

#     if location:
#         properties = properties.filter(location__icontains=location)
#     if category:
#         properties = properties.filter(category=category)
#     if min_price:
#         properties = properties.filter(price__gte=min_price)
#     if max_price:
#         properties = properties.filter(price__lte=max_price)

#     # Pagination
#     paginator = Paginator(properties, 10)  # Show 10 properties per page
#     page_number = request.GET.get('page')  # get page number from query params
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'page_obj': page_obj
#     }
#     return render(request, 'main/property_list.html', context)


@login_required
def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    reviews = Review.objects.filter(property=property)
    similar_properties = Property.objects.filter(category=property.category).exclude(pk=pk)[:3]

    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = property.favorited_by.filter(pk=request.user.pk).exists()

    return render(request, 'main/property_detail.html', {
        'property': property,
        'reviews': reviews,
        'similar_properties': similar_properties,
        'is_favorited': is_favorited
    })

# @login_required
# def add_property(request):
#     if request.method == 'POST':
#         form = PropertyForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Property added successfully!')
#             return redirect('landlord_dashboard')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = PropertyForm()
#     return render(request,'main/add_property.html',{'form': form})

@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user  
            property.save()
            messages.success(request, 'Property added successfully!')
            return redirect('landlord_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PropertyForm()
    return render(request, 'main/add_property.html', {'form': form})


@login_required
def edit_property(request, pk):
    property = get_object_or_404(Property, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            return redirect('landlord_dashboard')
    else:
        form = PropertyForm(instance=property)

    return render(request, 'main/edit_property.html', {'form': form})

@login_required
def delete_property(request, pk):
    property = get_object_or_404(Property, pk=pk, owner=request.user)

    if request.method == 'POST':
        property.delete()
        return redirect('landlord_dashboard')

    return render(request, 'main/delete_property.html', {'property': property})

@login_required
def toggle_favorite(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    # Try to get existing favorite
    favorite = Favorite.objects.filter(user=request.user, property=property).first()

    if favorite:
        # If favorite exists, delete it (unfavorite)
        favorite.delete()
        messages.success(request, f'Removed "{property.title}" from your favorites.')
    else:
        # Else create a new favorite
        Favorite.objects.create(user=request.user, property=property)
        messages.success(request, f'Added "{property.title}" to your favorites.')

    # Redirect back to the same page or property list if none provided
    next_url = request.GET.get('next') or 'property_list'
    return redirect(next_url)


@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('property')
    return render(request, 'main/favorite_list.html', {'favorites': favorites})

@login_required
def landlord_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_landlord:
        return redirect('tenant_dashboard')  # redirect tenants away from landlord dashboard

    properties = Property.objects.filter(owner=request.user)
    inquiries = Inquiry.objects.filter(property__in=properties).order_by('-timestamp')

    return render(request, 'main/landlord_dashboard.html', {
        'properties': properties,
        'inquiries': inquiries
    })

@login_required
def tenant_dashboard(request):
    if not request.user.is_authenticated or request.user.is_landlord:
        return redirect('landlord_dashboard')  # redirect landlords away from tenant dashboard

    inquiries = Inquiry.objects.filter(tenant=request.user).select_related('property').order_by('-timestamp')
    favorites = Favorite.objects.filter(user=request.user).select_related('property')

    return render(request, 'main/tenant_dashboard.html', {
        'inquiries': inquiries,
        'favorites': favorites,
    })

# @login_required
# def add_review(request, pk):
#     if request.method == 'POST':
#         property = get_object_or_404(Property, pk=pk)
#         rating = int(request.POST['rating'])
#         comment = request.POST['comment']
#         Review.objects.create(user=request.user, property=property, rating=rating, comment=comment)
#         return redirect('property_detail', pk=pk)

@login_required
def property_detail(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    reviews = property_obj.reviews.all().order_by('-created_at')
    user_review = None

    if request.user.is_authenticated:
        user_review = Review.objects.filter(property=property_obj, user=request.user).first()

    similar_properties = Property.objects.filter(
        category=property_obj.category
    ).exclude(id=property_obj.id)[:3]

    is_favorited = request.user.is_authenticated and request.user in property_obj.favorited_by.all()
    rating_range = [i * 0.5 for i in range(1, 11)]

    context = {
        'property': property_obj,
        'reviews': reviews,
        'user_review': user_review,
        'similar_properties': similar_properties,
        'is_favorited': is_favorited,
        'rating_range': rating_range,  
    }
    return render(request, 'main/property_detail.html', context)

@login_required
def add_or_update_review(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if not (rating and comment):
            messages.error(request, "Please provide both a rating and a comment.")
            return redirect('property_detail', property_id=property_id)

        review, created = Review.objects.update_or_create(
            property=property_obj,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )

        messages.success(request, "Review submitted successfully!" if created else "Review updated successfully!")
        return redirect('property_detail', property_id=property_id)

@login_required
def delete_review(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    review = Review.objects.filter(property=property_obj, user=request.user).first()

    if review:
        review.delete()
        messages.success(request, "Review deleted successfully.")

    return redirect('property_detail', property_id=property_id)

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating and comment:
            review.rating = rating
            review.comment = comment
            review.save()
            messages.success(request, "Review updated successfully!")
            return redirect('property_detail', property_id=review.property.id)
        else:
            messages.error(request, "Please fill out all fields.")

    return render(request, 'edit_review.html', {'review': review})
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import GovernmentScheme, SchemeApplication

@login_required
def schemes_list(request):
    """Display all government schemes with filtering"""
    schemes = GovernmentScheme.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        schemes = schemes.filter(
            Q(name__icontains=search_query) |
            Q(name_hi__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(benefits__icontains=search_query)
        )
    
    # Category filter
    category_filter = request.GET.get('category')
    if category_filter and category_filter != 'all':
        schemes = schemes.filter(category=category_filter)
    
    # Get categories for filter dropdown
    categories = GovernmentScheme.objects.values_list('category', flat=True).distinct()
    category_choices = dict(GovernmentScheme.CATEGORY_CHOICES)
    
    context = {
        'schemes': schemes,
        'search_query': search_query,
        'selected_category': category_filter,
        'categories': [(cat, category_choices.get(cat, cat)) for cat in categories],
        'category_choices': category_choices,
        'total_schemes': schemes.count(),
    }
    return render(request, 'schemes/list.html', context)

@login_required
def scheme_detail(request, scheme_id):
    scheme = get_object_or_404(GovernmentScheme, id=scheme_id)
    has_applied = SchemeApplication.objects.filter(
        farmer=request.user,
        scheme=scheme
    ).exists()
    
    if request.method == 'POST':
        if not has_applied:
            SchemeApplication.objects.create(
                farmer=request.user,
                scheme=scheme
            )
            return JsonResponse({'status': 'applied', 'message': 'Application submitted successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Already applied for this scheme'})
    
    context = {
        'scheme': scheme,
        'has_applied': has_applied
    }
    return render(request, 'schemes/detail.html', context)

@login_required
def my_applications(request):
    applications = SchemeApplication.objects.filter(farmer=request.user).order_by('-applied_date')
    return render(request, 'schemes/my_applications.html', {'applications': applications})
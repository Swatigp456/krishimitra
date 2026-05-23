from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from .models import ProductListing, BuyerRequest, Buyer, Interest, ChatMessage
from crops.models import Crop
import json

@login_required
def marketplace(request):
    """Main marketplace page - shows all listings and buyer requests"""
    crops = Crop.objects.all()
    
    # Get filter parameters
    crop_filter = request.GET.get('crop')
    type_filter = request.GET.get('type', 'listings')  # listings or requests
    
    # Get all active listings
    listings = ProductListing.objects.filter(status='available')
    if crop_filter:
        listings = listings.filter(crop_id=crop_filter)
    
    # Get buyer requests
    buyer_requests = BuyerRequest.objects.filter(is_active=True)
    if crop_filter:
        buyer_requests = buyer_requests.filter(crop_id=crop_filter)
    
    # Get farmer's own listings
    my_listings = ProductListing.objects.filter(farmer=request.user)
    
    # Get interests received for farmer's listings
    received_interests = Interest.objects.filter(
        listing__farmer=request.user,
        status='pending'
    ).select_related('listing', 'buyer')
    
    context = {
        'crops': crops,
        'listings': listings,
        'buyer_requests': buyer_requests,
        'my_listings': my_listings,
        'received_interests': received_interests,
        'crop_filter': crop_filter,
        'type_filter': type_filter,
    }
    return render(request, 'chat/marketplace.html', context)

@login_required
def post_listing(request):
    """Farmer posts a new product listing"""
    if request.method == 'POST':
        try:
            crop_id = request.POST.get('crop')
            quantity = request.POST.get('quantity')
            price = request.POST.get('price')
            location = request.POST.get('location')
            quality = request.POST.get('quality', 'Standard')
            description = request.POST.get('description', '')
            harvest_date = request.POST.get('harvest_date') or None
            
            listing = ProductListing.objects.create(
                farmer=request.user,
                crop_id=crop_id,
                quantity=quantity,
                price_per_quintal=price,
                location=location,
                quality=quality,
                description=description,
                harvest_date=harvest_date,
                status='available'
            )
            
            messages.success(request, f'✅ {listing.crop.name} listing posted successfully!')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return redirect('marketplace')

@login_required
def edit_listing(request, listing_id):
    """Edit an existing listing"""
    listing = get_object_or_404(ProductListing, id=listing_id, farmer=request.user)
    
    if request.method == 'POST':
        listing.quantity = request.POST.get('quantity', listing.quantity)
        listing.price_per_quintal = request.POST.get('price', listing.price_per_quintal)
        listing.location = request.POST.get('location', listing.location)
        listing.quality = request.POST.get('quality', listing.quality)
        listing.description = request.POST.get('description', listing.description)
        listing.save()
        messages.success(request, 'Listing updated successfully!')
        return redirect('marketplace')
    
    return JsonResponse({
        'id': listing.id,
        'quantity': str(listing.quantity),
        'price': str(listing.price_per_quintal),
        'location': listing.location,
        'quality': listing.quality,
        'description': listing.description,
    })

@login_required
def delete_listing(request, listing_id):
    """Delete a listing"""
    listing = get_object_or_404(ProductListing, id=listing_id, farmer=request.user)
    listing.delete()
    messages.success(request, 'Listing deleted successfully!')
    return redirect('marketplace')

@login_required
def show_interest(request, listing_id):
    """Buyer shows interest in a farmer's listing"""
    if request.method == 'POST':
        listing = get_object_or_404(ProductListing, id=listing_id)
        
        # Get or create buyer
        buyer, created = Buyer.objects.get_or_create(
            email=request.POST.get('email'),
            defaults={
                'name': request.POST.get('buyer_name'),
                'company': request.POST.get('company', ''),
                'phone': request.POST.get('phone'),
            }
        )
        
        # Create interest record
        interest = Interest.objects.create(
            listing=listing,
            buyer=buyer,
            offered_price=request.POST.get('offered_price') or None,
            quantity_requested=request.POST.get('quantity') or None,
            message=request.POST.get('message', ''),
            status='pending'
        )
        
        messages.success(request, f'Interest shown! The farmer will contact you soon.')
    
    return redirect('marketplace')

@login_required
def respond_to_interest(request, interest_id):
    """Farmer responds to buyer interest (accept/reject/negotiate)"""
    interest = get_object_or_404(Interest, id=interest_id, listing__farmer=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'accept':
            interest.status = 'accepted'
            interest.listing.status = 'pending'
            interest.listing.save()
            messages.success(request, 'Interest accepted! Contact buyer to complete sale.')
        
        elif action == 'reject':
            interest.status = 'rejected'
            messages.info(request, 'Interest rejected.')
        
        elif action == 'negotiate':
            interest.status = 'negotiating'
            # Add negotiation message
            ChatMessage.objects.create(
                interest=interest,
                sender_type='farmer',
                message=request.POST.get('counter_offer', 'Let\'s negotiate the price.')
            )
            messages.info(request, 'Negotiation started. Check chat for details.')
        
        interest.save()
    
    return redirect('marketplace')

@login_required
def chat_view(request, interest_id):
    """Chat between farmer and buyer"""
    interest = get_object_or_404(Interest, id=interest_id)
    
    # Check if user is authorized (either farmer or buyer)
    if request.user != interest.listing.farmer and request.user.email != interest.buyer.email:
        messages.error(request, 'Unauthorized access')
        return redirect('marketplace')
    
    # Mark messages as read
    if request.user == interest.listing.farmer:
        ChatMessage.objects.filter(interest=interest, sender_type='buyer', is_read=False).update(is_read=True)
    else:
        ChatMessage.objects.filter(interest=interest, sender_type='farmer', is_read=False).update(is_read=True)
    
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            sender_type = 'farmer' if request.user == interest.listing.farmer else 'buyer'
            ChatMessage.objects.create(
                interest=interest,
                sender_type=sender_type,
                message=message_text,
                is_read=False
            )
        
        return redirect('chat_view', interest_id=interest_id)
    
    messages_list = ChatMessage.objects.filter(interest=interest)
    
    context = {
        'interest': interest,
        'messages': messages_list,
        'is_farmer': request.user == interest.listing.farmer,
    }
    return render(request, 'chat/chat.html', context)

@login_required
def my_interests(request):
    """Show interests sent by farmer as buyer"""
    # For demo, show interests where farmer acted as buyer
    # For real implementation, you'd need farmer_buyer relationship
    interests = Interest.objects.filter(
        Q(listing__farmer=request.user) |  # Received interests
        Q(buyer__email=request.user.email)  # Sent interests
    ).select_related('listing', 'buyer')
    
    return render(request, 'chat/my_interests.html', {'interests': interests})

@login_required
def mark_listing_sold(request, listing_id):
    """Mark listing as sold"""
    listing = get_object_or_404(ProductListing, id=listing_id, farmer=request.user)
    listing.status = 'sold'
    listing.save()
    messages.success(request, 'Listing marked as sold!')
    return redirect('marketplace')
@login_required
def my_listings(request):
    """Show farmer's own listings"""
    listings = ProductListing.objects.filter(farmer=request.user).order_by('-created_at')
    return render(request, 'chat/my_listings.html', {'listings': listings})
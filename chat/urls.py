from django.urls import path
from . import views

urlpatterns = [
    path('marketplace/', views.marketplace, name='marketplace'),
    path('post-listing/', views.post_listing, name='post_listing'),
    path('edit-listing/<int:listing_id>/', views.edit_listing, name='edit_listing'),
    path('delete-listing/<int:listing_id>/', views.delete_listing, name='delete_listing'),
    path('show-interest/<int:listing_id>/', views.show_interest, name='show_interest'),
    path('respond-interest/<int:interest_id>/', views.respond_to_interest, name='respond_to_interest'),
    path('chat/<int:interest_id>/', views.chat_view, name='chat_view'),
    path('my-interests/', views.my_interests, name='my_interests'),
    path('my-listings/', views.my_listings, name='my_listings'),  # ADD THIS LINE
    path('mark-sold/<int:listing_id>/', views.mark_listing_sold, name='mark_sold'),
]
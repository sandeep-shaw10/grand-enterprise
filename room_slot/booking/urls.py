from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='index'),
    path('book',views.book,name='book'),
    path('contact-us',views.contact,name='contact-us'),
    path('book-now/<str:category>/<str:id>',views.book_now,name='book-now'),
    path('cancel-room/<str:id>',views.cancel_room,name='cancel-room'),
    path('delete-room/<str:id>',views.delete_room,name='delete-room'),
    path('room/confirm-now-booking',views.book_confirm,name="book_confirm"),
    path('apartment/confirm-now-booking',views.book_confirm1,name="book_confirm1")
]
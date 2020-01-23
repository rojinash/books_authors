from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('authors', views.add_author),
    path('process_book', views.process_book),
    path('process_author', views.process_author),
    path('books/<int:book_id>', views.book_details),
    path('authors/<int:author_id>', views.author_details),
    path('book_to_author/<int:author_id>', views.add_book_to_author),
    path('author_to_book/<int:book_id>', views.add_author_to_book),
    path('register', views.register),
    path('registration', views.registration),
    path('logout', views.logout),
    path('login', views.login),
]
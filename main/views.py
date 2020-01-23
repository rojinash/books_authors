from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
# Create your views here.
def index(request):
    if 'user_id' not in request.session:
        return redirect('/register')
    user_id = request.session['user_id']
    context = {
        'books' : Book.objects.all(),
        'user': User.objects.get(id = user_id)

    }
    return render(request, 'index.html', context)

def process_book(request):
    if request.method != 'POST':
        return redirect('/')
    form = request.POST
    Book.objects.create(title=form['title'], desc=form['desc'])
    return redirect('/')

def book_details(request, book_id):
    book = Book.objects.get(id=book_id)
    authors_without_book = []
    for author in Author.objects.all():
        if author not in book.authors.all():
            authors_without_book.append(author)
    context = {
        'book': book,
        'authors': authors_without_book
    }
    return render(request, 'book_details.html', context)

def add_author_to_book(request, book_id):
    this_book = Book.objects.get(id=book_id)
    this_author = Author.objects.get(id=request.POST['author_id'])

    this_author.books.add(this_book)
    return redirect('/books/'+str(book_id))


def add_author(request):
    context = {
        'authors': Author.objects.all()
    }
    return render(request, 'add_author.html', context)

def process_author(request):
    if request.method != 'POST':
        return redirect('/authors')
    form = request.POST
    Author.objects.create(first_name=form['first_name'], last_name=form['last_name'], notes=form['notes'])
    return redirect('/authors')

def author_details(request, author_id):
    author = Author.objects.get(id=author_id)
    books_not_associated = []
    for book in Book.objects.all():
        if book not in author.books.all():
            books_not_associated.append(book)
    context = {
        'author': author,
        'books': books_not_associated
    }
    return render(request, 'author_details.html', context)

def add_book_to_author(request, author_id):
    this_book = Book.objects.get(id=request.POST['book_id'])
    this_author = Author.objects.get(id=author_id)

    this_author.books.add(this_book)
    return redirect('/authors/'+str(author_id))

def register(request):
    return render(request, 'register.html')

def registration(request):
    form = request.POST
    err = User.objects.basic_validator(form)
    if len(err) > 0:
        for value in err.values():
            messages.error(request, value)
        return redirect('/register')
    hashedpw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(first_name = form['first_name'], last_name=form['last_name'], email=form['email'], password=hashedpw)

    request.session['user_id'] = user.id 
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/register')

def login(request):
    response = User.objects.login_validator(request.POST)
    if response['status'] == False:
        for error in response['err_log']:
            messages.error(request, error)
        return redirect('/register')
    else:
        request.session['user_id'] = response['user_id']
        # request.session['name'] = User.objects.get(id=response['user_id']).name
        return redirect('/')





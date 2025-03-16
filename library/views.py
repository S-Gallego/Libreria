from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Library, Book, User, Loan

# ------------------------
# Gestión de Bibliotecas
# ------------------------

@csrf_exempt
def library_list(request):
    if request.method == 'GET':
        libraries = list(Library.objects.values())
        return JsonResponse(libraries, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        library = Library.objects.create(name=data['name'])
        return JsonResponse({"id": library.id, "name": library.name}, status=201)

@csrf_exempt
def library_detail(request, id):
    try:
        library = Library.objects.get(id=id)
    except Library.DoesNotExist:
        return JsonResponse({"error": "Library not found"}, status=404)

    if request.method == 'GET':
        return JsonResponse({"id": library.id, "name": library.name})

# ------------------------
# Gestión de Libros
# ------------------------

@csrf_exempt
def book_list(request):
    if request.method == 'GET':
        books = list(Book.objects.values())
        return JsonResponse(books, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        try:
            library = Library.objects.get(id=data['library_id'])
            book = Book.objects.create(title=data['title'], author=data['author'], library=library)
            return JsonResponse({"id": book.id, "title": book.title, "author": book.author}, status=201)
        except Library.DoesNotExist:
            return JsonResponse({"error": "Library not found"}, status=404)

@csrf_exempt
def book_detail(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found"}, status=404)

    if request.method == 'GET':
        return JsonResponse({"id": book.id, "title": book.title, "author": book.author, "library": book.library.id})

    elif request.method == 'DELETE':
        book.delete()
        return JsonResponse({"message": "Book deleted successfully"}, status=204)

@csrf_exempt
def books_by_library(request, id):
    try:
        library = Library.objects.get(id=id)
        books = list(library.books.values())
        return JsonResponse(books, safe=False)
    except Library.DoesNotExist:
        return JsonResponse({"error": "Library not found"}, status=404)

# ------------------------
# Gestión de Usuarios
# ------------------------

@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = list(User.objects.values())
        return JsonResponse(users, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.create(name=data['name'], email=data['email'])
        return JsonResponse({"id": user.id, "name": user.name, "email": user.email}, status=201)

@csrf_exempt
def user_detail(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    if request.method == 'GET':
        return JsonResponse({"id": user.id, "name": user.name, "email": user.email})

# ------------------------
# Gestión de Préstamos
# ------------------------

@csrf_exempt
def loan_list(request):
    if request.method == 'GET':
        loans = list(Loan.objects.values())
        return JsonResponse(loans, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        try:
            user = User.objects.get(id=data['user_id'])
            book = Book.objects.get(id=data['book_id'])

            if book.is_borrowed:
                return JsonResponse({"error": "Book is already borrowed"}, status=400)

            loan = Loan.objects.create(user=user, book=book)
            return JsonResponse({"id": loan.id, "user": loan.user.id, "book": loan.book.id}, status=201)
        except (User.DoesNotExist, Book.DoesNotExist):
            return JsonResponse({"error": "User or Book not found"}, status=404)

@csrf_exempt
def loan_detail(request, id):
    try:
        loan = Loan.objects.get(id=id)
    except Loan.DoesNotExist:
        return JsonResponse({"error": "Loan not found"}, status=404)

    if request.method == 'PUT':
        data = json.loads(request.body)
        loan.return_date = data.get('return_date')
        loan.save()
        return JsonResponse({"message": "Loan updated successfully"})

@csrf_exempt
def user_loans(request, id):
    try:
        user = User.objects.get(id=id)
        loans = list(user.loans.values())
        return JsonResponse(loans, safe=False)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

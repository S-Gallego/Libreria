from django.db import models

class Library(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="books")
    is_borrowed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
        
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans")
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.return_date:
            self.book.is_borrowed = True
        else:
            self.book.is_borrowed = False
        self.book.save()
        super().save(*args, **kwargs)


from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Model for Student with basic fields
class Student(models.Model):
    isbn = models.CharField(max_length=40, default=None)  # ISBN for the book issued
    mail = models.CharField(max_length=40, default=None)  # Email of the student
    enrollment = models.CharField(max_length=40)  # Enrollment number of the student

# Model for additional student details, linked to the User model
class StudentExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to User model with a one-to-one relationship
    mail = models.CharField(max_length=40, default=None)  # Email of the student
    enrollment = models.CharField(max_length=40)  # Enrollment number of the student
    branch = models.CharField(max_length=40)  # Branch of the student

    # String representation of the student
    def __str__(self):
        return self.user.first_name + '[' + str(self.enrollment) + ']'

    # Property to get the student's name
    @property
    def get_name(self):
        return self.user.first_name

    # Property to get the user ID
    @property
    def getuserid(self):
        return self.user.id

# Model for Book with various attributes
class Book(models.Model):
    # Choices for book category
    catchoice = [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('biography', 'Biography'),
        ('history', 'History'),
    ]
    name = models.CharField(max_length=30)  # Name of the book
    isbn = models.PositiveIntegerField()  # ISBN of the book
    author = models.CharField(max_length=40)  # Author of the book
    category = models.CharField(max_length=30, choices=catchoice, default='education')  # Category of the book
    
    # String representation of the book
    def __str__(self):
        return self.name + '[' + str(self.isbn) + ']'

# Function to get the expiry date (15 days from today)
def get_expiry():
    return datetime.today() + timedelta(days=15)

# Model for IssuedBook to track issued books
class IssuedBook(models.Model):
    enrollment = models.CharField(max_length=30)  # Enrollment number of the student
    isbn = models.CharField(max_length=30)  # ISBN of the book
    issuedate = models.DateField(auto_now=True)  # Issue date (auto-set to current date)
    expirydate = models.DateField(default=get_expiry)  # Expiry date (15 days from issue)
    
    # Choices for status of the issued book
    statuschoice = [
        ('Issued', 'Issued'),
        ('Returned', 'Returned'),
    ]
    status = models.CharField(max_length=20, choices=statuschoice, default="Issued")  # Status of the book

    # String representation of the issued book
    def __str__(self):
        return self.enrollment

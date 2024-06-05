from django import forms
from django.contrib.auth.models import User
from . import models

# Form for Contact Us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)  # Name field with a max length of 30 characters
    Email = forms.EmailField()  # Email field
    Message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))  # Message field with a max length of 500 characters, using a textarea widget

# Form for Student user registration
class StudentUserForm(forms.ModelForm):
    class Meta:
        model = User  # Using the built-in User model
        fields = ['first_name', 'last_name', 'username', 'password']  # Fields to include in the form

# Form for additional student details
class StudentExtraForm(forms.ModelForm):
    class Meta:
        model = models.StudentExtra  # Using the StudentExtra model
        fields = ['mail', 'enrollment', 'branch']  # Fields to include in the form

# Form for adding a new book
class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book  # Using the Book model
        fields = ['name', 'isbn', 'author', 'category']  # Fields to include in the form

# Form for issuing a book
class IssuedBookForm(forms.Form):
    # ModelChoiceField for selecting a book, showing the book's name and ISBN
    isbn2 = forms.ModelChoiceField(queryset=models.Book.objects.all(), empty_label="Name and ISBN", to_field_name="isbn", label='Name and ISBN')
    
    # ModelChoiceField for selecting a student, showing the student's name and enrollment number
    enrollment2 = forms.ModelChoiceField(queryset=models.StudentExtra.objects.all(), empty_label="Name and Enrollment", to_field_name='enrollment', label='Name and Enrollment')

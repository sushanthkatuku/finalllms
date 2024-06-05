from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from . import forms, models
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta, date
from django.core.mail import send_mail
from librarymanagement.settings import EMAIL_HOST_USER

# View for the home page
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  # Redirect authenticated users
    return render(request, 'library/index.html')  # Render home page for unauthenticated users

# View for showing signup/login button for students
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  # Redirect authenticated users
    return render(request, 'library/studentclick.html')  # Render student click page

# View for showing signup/login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  # Redirect authenticated users
    return render(request, 'library/adminclick.html')  # Render admin click page

# View for student signup
def studentsignup_view(request):
    form1 = forms.StudentUserForm()  # Form for student user
    form2 = forms.StudentExtraForm()  # Form for additional student details
    mydict = {'form1': form1, 'form2': form2}
    
    if request.method == 'POST':
        email = request.POST.get('mail')  # Get email from POST data
        print("Email address is ", email)
        
        # Send registration confirmation email
        import smtplib
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login("helpinggpt@gmail.com", "xyie dyth ptog qfdc")
        smtp.sendmail("helpinggpt@gmail.com", [email], "You are Successfully Registered to our Service")
        smtp.quit()

        form1 = forms.StudentUserForm(request.POST)  # Populate form1 with POST data
        form2 = forms.StudentExtraForm(request.POST)  # Populate form2 with POST data
        if form1.is_valid() and form2.is_valid():
            user = form1.save()  # Save user form
            user.set_password(user.password)  # Set user password
            user.save()  # Save user with password

            f2 = form2.save(commit=False)
            f2.user = user
            user2 = f2.save()  # Save additional student details

            # Add user to 'STUDENT' group
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')  # Redirect to student login page
    return render(request, 'library/studentsignup.html', context=mydict)  # Render student signup page

# Check if user is admin
def is_admin(user):
    if user.is_superuser or user.is_staff:
        return True
    else:
        return False

# Check if user is a student
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

# View after login
def afterlogin_view(request):
    if is_admin(request.user):
        return render(request, 'library/adminafterlogin.html')  # Render admin after login page
    elif is_student(request.user):
        return render(request, 'library/studentafterlogin.html')  # Render student after login page

# View for adding a book (admin only)
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
    form = forms.BookForm()  # Empty book form
    if request.method == 'POST':
        form = forms.BookForm(request.POST)  # Form with POST data
        if form.is_valid():
            user = form.save()  # Save book form
            return render(request, 'library/bookadded.html')  # Render book added page
    return render(request, 'library/addbook.html', {'form': form})  # Render add book page

# View for viewing books (admin only)
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewbook_view(request):
    books = models.Book.objects.all()  # Get all books
    return render(request, 'library/viewbook.html', {'books': books})  # Render view book page

# View for issuing a book (admin only)
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    form = forms.IssuedBookForm()  # Empty issued book form
    if request.method == 'POST':
        form = forms.IssuedBookForm(request.POST)  # Form with POST data
        if form.is_valid():
            obj = models.IssuedBook()
            obj.enrollment = request.POST.get('enrollment2')  # Get enrollment from POST data
            obj.isbn = request.POST.get('isbn2')  # Get ISBN from POST data
            obj.save()  # Save issued book
            return render(request, 'library/bookissued.html')  # Render book issued page
    return render(request, 'library/issuebook.html', {'form': form})  # Render issue book page

# View for viewing issued books (admin only)
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks = models.IssuedBook.objects.all()  # Get all issued books
    li = []
    for ib in issuedbooks:
        issdate = str(ib.issuedate.day) + '-' + str(ib.issuedate.month) + '-' + str(ib.issuedate.year)  # Issue date
        expdate = str(ib.expirydate.day) + '-' + str(ib.expirydate.month) + '-' + str(ib.expirydate.year)  # Expiry date
        
        # Fine calculation
        days = (date.today() - ib.issuedate)
        print(date.today())
        d = days.days
        fine = 0
        if d > 15:
            day = d - 15
            fine = day * 10

        # Get book and student details
        books = list(models.Book.objects.filter(isbn=ib.isbn))
        students = list(models.StudentExtra.objects.filter(enrollment=ib.enrollment))
        i = 0
        for l in books:
            t = (students[i].get_name, students[i].enrollment, books[i].name, books[i].author, issdate, expdate, fine, ib.status)
            i = i + 1
            li.append(t)

    return render(request, 'library/viewissuedbook.html', {'li': li})  # Render view issued book page

# View for viewing students (admin only)
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students = models.StudentExtra.objects.all()  # Get all students
    return render(request, 'library/viewstudent.html', {'students': students})  # Render view student page

# View for deleting a book (admin only)
def deleteBook(request):
    bid = request.GET.get('bid')  # Get book ID from GET data
    models.Book.objects.filter(id=bid).delete()  # Delete book
    books = models.Book.objects.all()  # Get all books
    return render(request, 'library/viewbook.html', {'books': books})  # Render view book page

# View for updating a book (admin only)
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def updateBook(request):
    bid = request.GET.get('id')  # Get book ID from GET data
    name = request.GET.get('name')  # Get book name from GET data
    author = request.GET.get('author')  # Get book author from GET data
    category = request.GET.get('cat')  # Get book category from GET data
    book = models.Book.objects.filter(id=bid)

    book = get_object_or_404(book, id=bid)  # Get book or 404 if not found

    # Update the book attributes
    book.name = name
    book.author = author
    book.category = category

    # Save the changes to the database
    book.save()

    books = models.Book.objects.all()  # Get all books
    return render(request, 'library/viewbook.html', {'books': books})  # Render view book page

# View for editing a book (admin only)
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def editBook(request):
    bid = request.GET.get('bid')  # Get book ID from GET data
    book = models.Book.objects.filter(id=bid)
    bdata1 = {'id': book[0].id, 'name': book[0].name, 'author': book[0].author, 'category': book[0].category}
    return render(request, 'library/editBook.html', {'book': bdata1})  # Render edit book page

# View for students to see their issued books
@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student = models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook = models.IssuedBook.objects.filter(enrollment=student[0].enrollment)

    li1 = []
    li2 = []
    for ib in issuedbook:
        books = models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t = (request.user, student[0].enrollment, student[0].branch, book.name, book.author)
            li1.append(t)
        issdate = str(ib.issuedate.day) + '-' + str(ib.issuedate.month) + '-' + str(ib.issuedate.year)  # Issue date
        expdate = str(ib.expirydate.day) + '-' + str(ib.expirydate.month) + '-' + str(ib.expirydate.year)  # Expiry date
        
        # Fine calculation
        days = (date.today() - ib.issuedate)
        print(date.today())
        d = days.days
        fine = 0
        if d > 15:
            day = d - 15
            fine = day * 10
        t = (issdate, expdate, fine, ib.status, ib.id)
        li2.append(t)

    return render(request, 'library/viewissuedbookbystudent.html', {'li1': li1, {'li2': li2}})  # Render view issued book by student page

# View for returning a book
def returnbook(request, id):
    issued_book = models.IssuedBook.objects.get(pk=id)
    issued_book.status = "Returned"  # Update book status to 'Returned'
    issued_book.save()
    return redirect('viewissuedbookbystudent')  # Redirect to view issued book by student page

# View for the 'About Us' page
def aboutus_view(request):
    return render(request, 'library/aboutus.html')  # Render about us page

# View for the 'Contact Us' page
def contactus_view(request):
    sub = forms.ContactusForm()  # Empty contact us form
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)  # Form with POST data
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            # Send contact us email
            send_mail(str(name) + ' || ' + str(email), message, EMAIL_HOST_USER, ['wapka1503@gmail.com'], fail_silently=False)
            return render(request, 'library/contactussuccess.html')  # Render contact us success page
    return render(request, 'library/contactus.html', {'form': sub})  # Render contact us page

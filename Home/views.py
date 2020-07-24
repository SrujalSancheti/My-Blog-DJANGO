from django.shortcuts import render,redirect
from django.http import HttpResponse
from Home.models import Contact
from django.contrib import messages
from blog1.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# HTML Pages
def home(request):
    allPosts = Post.objects.all().order_by('-views')[:3]
    context = {'allPosts':allPosts}    
 
    context = {'allPosts':allPosts}
    return render(request,'home/home.html',context)

def about(request):
    messages.success(request,'This is about')
    return render(request,'home/about.html')

def contact(request):
   # messages.error(request, 'Welcome to Contact. Please fill details and add messsage and click submit button to contact us.')
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        desc = request.POST['desc']
        if len(name)<4 or len(email)<3 or len(phone)<10 or len(desc)<5:
            messages.error(request,"Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email,phone=phone,desc=desc)
            contact.save()
            messages.success(request,"Message is sent successfully. We will contact you soon.")
    return render(request,'home/contact.html')

def search(request):
    query =request.GET['query']
    if len(query)>50:
        allPosts = Post.objects.none()
    else:    
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent,allPostsAuthor)
    if allPosts.count() == 0:
        messages.warning(request,"No Search Results found. Please refine yout query")
    params = {'allPosts':allPosts,'query':query}
    return render(request,'home/search.html',params)

#Authentication API's
def handleSignUp(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2  = request.POST['pass2']
        
        # Check for erroeneous  inputs
        if len(username)>20:
            messages.error(request,"Username must be under 20 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request,"Username Should only contain letters and numbers")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request,"Passwords didn't match")
            return redirect('home')
        
        if len(pass1)<5:
            messages.error(request,"Lenght of password should be greater than 5")
            return redirect('home')
        
        # Create User
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"Account has been successfully created")
        return redirect('home')
    else:
        return HttpResponse("404 - Not Found")
    
def handlelogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        user = authenticate(username=loginusername,password=loginpass)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request,"Invalid Credentials, please try again")
            return redirect('home')
    return HttpResponse("404 - Not Found")
            
def handlelogout(request):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect('home')
    
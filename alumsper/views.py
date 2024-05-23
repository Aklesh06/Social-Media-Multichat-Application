from django.shortcuts import render ,get_object_or_404, redirect
from .models import Account, Post, Event, Comment ,EventComment
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .form import ImageForm,CommentForm,EventImageForm,EventCommentForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        email           =request.POST['email']
        username        =request.POST['name']
        gender          =request.POST['gender']
        phone           =request.POST['phone']
        batch           =request.POST['batch_year']
        password        =request.POST['password']
        re_password     =request.POST['re_password']
        job_profile     =request.POST['occupation']
        img_presence = False
        if 'image' in request.FILES:
            profile_image   =request.FILES['image']
            img_presence = True
        if password==re_password:
            if Account.objects.filter(email=email).exists():
                messages.info(request, "Email Already Exists")
                return redirect('register')
            elif Account.objects.filter(username=username).exists():
                messages.info(request, "UserName Already Exists")
                return redirect('register')
            else:
                if(img_presence):
                    user = Account.objects.create_user(username=username, email=email, gender=gender, password=password, batch=batch, job_profile=job_profile, profile_image=profile_image, phone=phone)
                else:
                     user = Account.objects.create_user(username=username, email=email, gender=gender, password=password, batch=batch, job_profile=job_profile, phone=phone)
                user.save()

                return redirect('login')
        else:
            messages.info(request, "Password Not Matched")
            return redirect('register')
    else:
        return render(request,"Registration.html")

def login(request):
    if request.method == 'POST':
        username    =request.POST['username']
        password    =request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.info(request,'Invalid Username/Password')
            return redirect('login')
    else:
        return render(request, 'Login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

def home(request):
    if request.user.is_anonymous:
        return redirect('login')
    users = Account.objects.all()
    all_post=Post.objects.all()
    all_post=all_post[::-1]
    return render(request,"alumn.html",{"all_post":all_post , "users":users})

def pass_reset_req(request):
    if request.method == "POST":
        pass_form = PasswordResetForm(request.POST)
        if pass_form.is_valid():
            mail = pass_form.cleaned_data['email']
            user_mail = Account.objects.filter(Q(email=mail))
            if(user_mail.exists()):
                for user in user_mail:
                    subject = "Password Request"
                    email_name = 'pass_message.txt'
                    parameters = {
                        'username':user.username,
                        'email':user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name':'Aluminispear',
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                        'token':default_token_generator.make_token(user),
                        'protocol':'http',        
                    }
                    email = render_to_string(email_name,parameters)
                    try:
                        send_mail(subject,email,"",[user.email], fail_silently = False)
                    except:
                        return HttpResponse("Invalid Header")
                    return redirect('password_reset_done')
    else:
        pass_form = PasswordResetForm()
    context = {
        'pass_form' : pass_form
    }
    return render(request,"password_reset.html",context)

def post(request,acc_id):
    account = get_object_or_404(Account, pk=acc_id)   
    if request.method == "POST":
        form=ImageForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.account = account
            post.save()
            obj=form.instance
            return render(request, "Post_Success.html" ,{"obj":obj})
    else:
        form=ImageForm()
    return render(request, "Post.html",{"form":form})

def comment(request,post_id,acc_id):
    post = get_object_or_404(Post, pk=post_id)
    account = get_object_or_404(Account, pk=acc_id)
    comments = post.comment_set.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.account = account
            comment.save()
            return redirect('comment', post_id=post_id, acc_id=acc_id)
    else:
        form = CommentForm()

    return render(request, 'comment.html', {'account': account, 'post': post, 'comments': comments, 'form': form})
    
def edit(request):
    if request.user.is_anonymous:
        return redirect('home')
    default_Profile_Image = '/media/profile_img/default_profile_pic.png'    
    return render(request, 'Profile_Edit.html' ,{'default_Image':default_Profile_Image})
    
    
def edit_profile(request):
    if(request.method == 'POST'):
        user_id         = request.POST['id']
        email           = request.POST['email']
        username        = request.POST['name']
        batch           = request.POST['batch_year']
        phone           = request.POST['phone']
        bio             = request.POST['bio']
        
        occ_presence = False
        first4 = int(batch[0:4]) 
        if(first4<=2019):
            job_profile = request.POST['occupation']
            occ_presence = True
        img_presence = False
        if 'image' in request.FILES:
            profile_image = request.FILES['image']
            img_presence = True
        user = Account.objects.get(pk=user_id)
        
        user.email = email
        user.username = username
        user.batch = batch
        user.phone = phone
        if bio:
            user.bio = bio
        if occ_presence:
            user.job_profile = job_profile
        if img_presence:
            user.profile_image = profile_image
        user.save()
        return redirect('edit_profile')
    else:
        return render(request, 'Profile_update_Successfull.html')

def event_page(request):
    if request.user.is_anonymous:
        return redirect('home')
    users = Account.objects.all()
    all_post=Event.objects.all()
    all_post=all_post[::-1]
    return render(request, 'Event.html',{"all_post":all_post , "users":users})

def event(request,acc_id):
    account = get_object_or_404(Account, pk=acc_id)   
    if request.method == "POST":
        form=EventImageForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.account = account
            event.save()
            obj=form.instance
            return render(request, "Event_successfull.html" ,{"obj":obj})
    else:
        form=ImageForm()
    return render(request, "Event_post.html",{"form":form})        

def eventcomment(request,event_id,acc_id):
    event = get_object_or_404(Event, pk=event_id)
    account = get_object_or_404(Account, pk=acc_id)
    comments = event.comments.all()
    
    if request.method == 'POST':
        form = EventCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.account = account
            comment.save()
            return redirect('eventcomment', event_id=event_id, acc_id=acc_id)
    else:
        form = CommentForm()

    return render(request, 'Event_comment.html', {'account': account, 'event': event, 'comments': comments, 'form': form})

def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('home')

def delete_eventpost(request, event_id):
    eventpost = get_object_or_404(Event, pk=event_id)
    eventpost.delete()
    return redirect('home')

def delete_comment(request, comm_id):
    comment = get_object_or_404(Comment, pk=comm_id)
    comment.delete()
    acc_id = comment.account_id
    post_id = comment.post_id
    
    return redirect('comment',post_id=post_id ,acc_id=acc_id)

def delete_eventcomment(request, eventcomm_id):
    comment = get_object_or_404(EventComment, pk=eventcomm_id)
    comment.delete()
    acc_id = comment.account_id
    event_id = comment.event_id
    
    return redirect('eventcomment',event_id=event_id ,acc_id=acc_id)
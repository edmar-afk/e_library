from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Classroom, Forum, Comments, Lesson,UserProfile
from django.db.models import Count
# Create your views here.


def homepage(request):
    return render(request, 'index.html')

def user_register(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
       
        email = request.POST['email']
        role = request.POST['role']
        password = request.POST['password1']
        repeat_password = request.POST['password2']
       
        if password != repeat_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('user_register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
            return redirect('user_register')

        else:
            # Create new user
            user = User.objects.create_user(first_name=fullname, username=email, email=email, password=password, last_name=role)
            user.save()
            
            user_profile = UserProfile.objects.create(user=user, status='Not Ban')
            user_profile.save()
            
            messages.success(request, 'You have been registered successfully.')
            return redirect('user_login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            
            if user.is_superuser:
                return redirect('teacher_forum') 
            
            elif user.is_staff:
                return redirect('student_dashboard')
            
            else:
                messages.error(request, "Please Wait for Admin to Accept your account")
                return redirect('user_login')
            
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect('user_login')
    return render(request, 'login.html')



def logout(request):
    auth.logout(request)
    messages.success(request, "Logged out Successfully!")
    return redirect('user_login')



def teacher_dashboard(request):
    classroom = Classroom.objects.filter(instructor=request.user).order_by('-id')
    if request.method == 'POST':
        class_name = request.POST['class_name']
        section = request.POST['section']
     
        new_class = Classroom.objects.create(class_name=class_name, section=section, instructor=request.user)
        new_class.save()
        messages.success(request, 'Classroom created')
        
    context = {
        'classroom':classroom,
    }
    return render(request, 'teacher/index.html', context)


def deleteClassroom(request, class_id):
    Classroom.objects.filter(id=class_id).delete()
    messages.success(request, 'Classroom Removed')
    return redirect('teacher_dashboard')


@login_required(login_url='/homepage')
def classroom(request, class_id):
    room = get_object_or_404(Classroom, id=class_id)
    classroom = Classroom.objects.filter(id=class_id)
    lessons = Lesson.objects.filter(classroom=room.id)
   
    context = {
        'classroom': classroom,
        'room': room,
        'lessons':lessons,
    }
    return render(request, 'teacher/classroom.html', context)


def teacher_forum(request):
    forum = Forum.objects.all().select_related('uploader', 'uploader__userprofile').order_by('-id')
    
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        file = request.FILES.get('file')  # Use get() to avoid KeyError
        
        new_forum = Forum.objects.create(title=title, description=description, uploader=request.user, file=file)
        new_forum.save()
        messages.success(request, 'Forum created')
        
        
    context = {
        'forum':forum,
    }
    return render(request, 'teacher/forum.html', context)

def deleteForum(request, forum_id):
    Forum.objects.filter(id=forum_id).delete()
    messages.success(request, 'Forum deleted')
    return redirect(request.META.get('HTTP_REFERER'))

def teacher_forumPost(request, forum_id):
    forum = Forum.objects.filter(id=forum_id).select_related('uploader', 'uploader__userprofile').get(id=forum_id)
    comments = Comments.objects.filter(post=forum_id).order_by('-id')
    comment_count = Comments.objects.filter(post=forum_id).count()
    
    if request.method == 'POST':
        comment = request.POST['comment']
    
        new_comment = Comments.objects.create(post=forum, commentors=request.user, comment=comment)
        new_comment.save()
    
    context = {
        'forum':forum,
        'comments':comments,
        'comment_count':comment_count,
    }
    return render(request, 'teacher/post.html', context) 



def teacher_lesson(request):
    lessons = Lesson.objects.all().order_by('-id')
    
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        file = request.FILES.get('file')  # Use get() to avoid KeyError
    
        new_lesson = Lesson.objects.create(title=title,description=description, lesson_file=file, teacher=request.user)
        new_lesson.save()
    
    context = {
      'lessons':lessons, 
    }
    return render(request, 'teacher/lesson.html', context) 

def deleteLesson(request, lesson_id):
    Lesson.objects.filter(id=lesson_id).delete()
    messages.success(request, 'Lesson deleted')
    return redirect(request.META.get('HTTP_REFERER'))


def student_dashboard(request):
    forum = Forum.objects.all().select_related('uploader', 'uploader__userprofile').order_by('-id')
    
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        file = request.FILES.get('file')  # Use get() to avoid KeyError
        
        new_forum = Forum.objects.create(title=title, description=description, uploader=request.user, file=file)
        new_forum.save()
        messages.success(request, 'Forum created')
        
        
    context = {
        'forum':forum,
    }
    return render(request, 'student/index.html', context)



def student_forumPost(request, forum_id):
    forum = Forum.objects.filter(id=forum_id).select_related('uploader', 'uploader__userprofile').get(id=forum_id)
    comments = Comments.objects.filter(post=forum_id).order_by('-id').select_related('commentors', 'commentors__userprofile')
    comment_count = Comments.objects.filter(post=forum_id).count()
    
    if request.method == 'POST':
        comment = request.POST['comment']
    
        new_comment = Comments.objects.create(post=forum, commentors=request.user, comment=comment)
        new_comment.save()
    
    context = {
        'forum':forum,
        'comments':comments,
        'comment_count':comment_count,
    }
    return render(request, 'student/post.html', context) 

def student_classroom(request):
    classroom = Classroom.objects.all().order_by('-id')
    
    context = {
        'classroom': classroom,
    }
    return render(request, 'student/classroom.html',context)


def student_room(request, class_id):
    room = get_object_or_404(Classroom, id=class_id)
    activities = Lesson.objects.filter(classroom=room.id)
    lesson = Lesson.objects.filter(classroom=room)
    
    
    context = {
        'room': room,
        'activities': activities,
        'lessons':lesson,
       
    }
    return render(request, 'student/room.html', context)



def student_lesson(request):
    lessons = Lesson.objects.all().order_by('-id')
  
    context = {
      'lessons':lessons, 
    }
    return render(request, 'student/lesson.html', context)



def mainLogin(request):
    return render(request, 'main/mainLogin.html')

def dashboard(request):
    student = User.objects.filter(last_name='Student').order_by('-id').select_related('userprofile')
    instructor = User.objects.filter(last_name='Teacher').order_by('-id')
    context = {
        'student': student,
        'instructor':instructor
       
    }
    return render(request, 'main/mainDashboard.html', context)

def approve_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_staff = True
    user.save()
    # You can redirect to a success page or to the same page
    return redirect('mainDashboard')

def disapprove_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_staff = False
    user.save()
    # You can redirect to a success page or to the same page
    return redirect('mainDashboard')


def approve_instructor(request, instructor_id):
    user = User.objects.get(pk=instructor_id)
    user.is_superuser = True
    user.save()
    # You can redirect to a success page or to the same page
    return redirect('mainDashboard')

def disapprove_instructor(request, instructor_id):
    user = User.objects.get(pk=instructor_id)
    user.is_superuser = False
    user.save()
    # You can redirect to a success page or to the same page
    return redirect('mainDashboard')


def deleteUser(request, user_id):
    User.objects.filter(id=user_id).delete()
    messages.success(request, 'User Removed')
    return redirect('/mainDashboard')


def about(request):
    return render(request, 'about.html')
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
from .models import Student,schedule,coursetaken
from django.contrib import messages
from django.urls import reverse
from datetime import datetime


# Student Registration View
def student_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        course_option = request.POST['course_option']
        date_of_joining = request.POST['date_of_joining']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']

        # Create User
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        Student.objects.create(user=user, phone_number=phone_number, course_option=course_option, date_of_joining=date_of_joining)

        messages.success(request, 'Student registered successfully.')
        return redirect('login')

    return render(request, 'student_register.html')

# Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'login.html')

# Admin Dashboard View
def admin_dashboard(request):
    if not request.user.is_staff:
        return HttpResponse("You are not authorized to view this page.")
    else:
         Schedule = schedule.objects.all() # Fetch all schedule entries
         print(Schedule)
         course=coursetaken.objects.all()
         print(course)
         course1=coursetaken.objects.all().values()
         print(course1)
         context = {
        'Schedule': Schedule,
        'course': course
    }
    
    return render(request, 'admin_dashboard.html',context)

# Student Dashboard View
def student_dashboard(request):
    if request.user.is_staff:
        return HttpResponse("You are not authorized to view this page.")
    else:
         Studen=schedule.objects.all() # Fetch all schedule entries
         print(Student)
      
    if request.method == "POST":
        batch_id=request.POST.get("batch_id")
        trainer=request.POST.get("trainer")
        course_name=request.POST.get("course_name")
        batch_date=request.POST.get("batch_date")
        start_time=request.POST.get("start_time")
        end_time=request.POST.get("end_time")
        date_str=batch_date
        date_obj = datetime.strptime(date_str, "%b. %d, %Y")
        # Format the date to YYYY-MM-DD
        formatted_date = date_obj.strftime("%Y-%m-%d")  
        time_str=start_time
        time_str = time_str.replace(".", "")
        time_obj = datetime.strptime(time_str, "%I:%M %p")
         # Now format the time to a 24-hour format
        formatted_time = time_obj.strftime("%H:%M:%S")
        time_stri=end_time
        time_stri = time_stri.replace(".", "")
        time_obj1 = datetime.strptime(time_stri, "%I:%M %p")
         # Now format the time to a 24-hour format
        formatted_time1 = time_obj1.strftime("%H:%M:%S")
        stud= request.user.username  # Get the logged-in username
        result = User.objects.get(username=stud)
        result1 = Student.objects.get(user_id=result.id)
        student_id=result1.user_id
        studentname=result.username
        phonenumber=result1.phone_number
        email=result.email
        if result1.course_option==course_name:
            coursetaken.objects.create(student_id=student_id,studentname=studentname,phone_number=phonenumber,email=email,batch_id=batch_id,trainer=trainer,course_name=course_name,batch_date=formatted_date,start_time=formatted_time,end_time=formatted_time1)
            return JsonResponse({"success": True})
        else:
            messages.error(request, 'Course does not match')
            return JsonResponse({"success": False})

    return render(request, 'student_dashboard.html',{'Schedule':Studen})
   


# Logout View
def user_logout(request):
    logout(request)
    return redirect('login')

#add schedule
def add_schedule(request):
    if request.method == 'POST':
        batch_id = request.POST['batchid']
        sir_name = request.POST['sirname']
        course_name = request.POST['course_name']
        batch_date= request.POST['batch_date']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        schedule.objects.create(batch_id=batch_id, trainer=sir_name, course_name=course_name, batch_date=batch_date,start_time=start_time,end_time=end_time)
        messages.success(request, 'Scheduled successfully.')
        return redirect('admin_dashboard')

    return render(request,'add_schedule.html')

def home(request):
    return render(request, 'home.html')

def edit_schedule(request, batch_id):
    # Fetch the specific schedule based on batch_id
    Schedule = get_object_or_404(schedule, batch_id=batch_id)
    
    if request.method == 'POST':
        # Update schedule details from form inputs
        Schedule.trainer = request.POST['sirname']
        Schedule.course_name = request.POST['course_name']
        Schedule.batch_date = request.POST['batch_date']
        Schedule.start_time = request.POST['start_time']
        Schedule.end_time = request.POST['end_time']
        Schedule.save()
        return redirect('admin_dashboard')
    
    # Render the edit form with the fetched schedule data
    return render(request, 'edit.html', {'Schedule': Schedule})
def delete_schedule(request,batch_id):
    Schedule = get_object_or_404(schedule, batch_id=batch_id)
    # Delete the schedule instance
    print(Schedule)
    Schedule.delete()
    return redirect('admin_dashboard')
    





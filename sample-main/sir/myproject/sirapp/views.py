from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ClgRegistration
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import StudentEvent, FacultyEvent, LectureEvent,LectureEventFeedback
from django.db.models import Count
import calendar
from .models import StudentEvent, StudentEventFeedback,ClgRequest,PrincipalRequest,Requestsir,FinalRequest
from django.http import JsonResponse
from .models import FacultyEventFeedback,OtherEvent, OtherEventFeedback,CalEvents
import csv
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa  # Importing the module for pdf creation
from django.core.mail import send_mail
from django.core.exceptions import MultipleObjectsReturned

def send_email(request,email,event_name,event_type):
    subject = "Your Request has been Accepted"
    message = "Your request has been accepted."
    from_email = "professorsaikumarml@gmail.com"  # Replace with your sender email
    recipient_list = [email]

    # Send the email using the send_mail function
    send_mail(subject, message, from_email, recipient_list)
    try:
        events = FinalRequest.objects.filter(email=email, program_topic=event_name)
        for event in events:
            event.acknowledgement = True
            event.save()
            if event_type == "Student Development Program":
                student_event = StudentEvent(
                    title=event_name,
                    date=event.date,
                    college=event.college_name,
                    location = event.college_name + "Telangana, India",

                    description="On " + str(event.date) + " conduted " + event_name
                )
                student_event.save()
            elif event_type == "Faculty Development Program":
                faculty_event = OtherEvent(
                    title=event_name,
                    date=event.date,
                    contact_person=event.name,
                    email=event.email,
                    cell=event.mobile,  # Use 'mobile' from the function parameter
                    description="On " + str(event.date) + " conduted " + event_name
                )
                faculty_event.save()



    except FinalRequest.DoesNotExist:
        pass
    except MultipleObjectsReturned:
        pass

    return render(request, "admin_calender.html")


def send_reject_email(request,email,event_name):
    subject = "Your Request has been Rejected"
    message = "Your request has been Rejected, Please kindly change date."
    from_email = "professorsaikumarml@gmail.com"  # Replace with your sender email
    recipient_list = [email]

    # Send the email using the send_mail function
    send_mail(subject, message, from_email, recipient_list)
    try:
        events = FinalRequest.objects.filter(email=email, program_topic = event_name)
        for event in events:
            event.acknowledgement = True
            event.save()


    except FinalRequest.DoesNotExist:
        pass
    except MultipleObjectsReturned:
        pass
    return render(request, "admin_calender.html")
def pdf_template(request):
    return render(request, "pdf_template")
def std_pdf(request):
    return render(request, "std_pdf")
def fac_pdf(request):
    return render(request, "fac_pdf")

class GeneratePDF(View):
    def get(self, request, event_title):
        # Get the feedback data for the specified event
        feedbacks = LectureEventFeedback.objects.filter(event__title=event_title)

        # Create a PDF template using Django's template system
        template = get_template('pdf_template.html')
        context = {'feedbacks': feedbacks, 'event_title': event_title}
        html = template.render(context)

        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{event_title}_feedback.pdf"'

        # Generate the PDF and write it to the response
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('PDF generation error')

        return response

class GenerateFacPDF(View):
    def get(self, request, event_title):
        # Get the feedback data for the specified event
        feedbacks = OtherEventFeedback.objects.filter(event__title=event_title)

        # Create a PDF template using Django's template system
        template = get_template('fac_pdf.html')
        context = {'feedbacks': feedbacks, 'event_title': event_title}
        html = template.render(context)

        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{event_title}_feedback.pdf"'

        # Generate the PDF and write it to the response
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('PDF generation error')

        return response

class GenerateStdPDF(View):
    def get(self, request, event_title):
        # Get the feedback data for the specified event
        feedbacks = StudentEventFeedback.objects.filter(event__title=event_title)

        # Create a PDF template using Django's template system
        template = get_template('std_pdf.html')
        context = {'feedbacks': feedbacks, 'event_title': event_title}
        html = template.render(context)

        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{event_title}_feedback.pdf"'

        # Generate the PDF and write it to the response
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('PDF generation error')

        return response

# Import any models or forms you may have here

# views.py
# from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def get_user_credentials():
    # Retrieve all UserRegistration objects from the database
    user_records = ClgRegistration.objects.all()

    # Create a dictionary to store email-password pairs
    user_credentials = {}

    # Populate the dictionary with email-password pairs from the database records
    for user_record in user_records:
        user_credentials[user_record.email] = user_record.password

    return user_credentials

def admin_login(request):
    if request.method == 'POST':
        user_type = request.POST['userType']
        email = request.POST['email']
        password = request.POST['password']

        # Check if the user exists and is of the selected type
        mydict = dict()
        mydict = get_user_credentials()
        print(mydict)
        try:

          if user_type == "admin" and email=="prof_saikumar@rediffmail.com" and password == "12345":
              return redirect('dashboard')
          elif password == mydict[email]:
              return redirect('user_home')
          else:
              error_message = 'Invalid email, password, or user type. Please try again.'
              return render(request, 'admin_login.html', {'error_message': error_message})
        except:

          error_message = 'Invalid email, password, or user type. Please try again.'
          return render(request, 'admin_login.html', {'error_message': error_message})

    return render(request, 'admin_login.html')

def index(request):
    return render(request, "home.html")

def admin_registration(request):
    if request.method == 'POST':
        email = request.POST['regEmail']
        password = request.POST['regPassword']
        confirm_password = request.POST['confirmPassword']
        college_name = request.POST['collegeName']
        name = request.POST['name']
        cell = request.POST['regContact']  # Update the field name here
        location = request.POST['regAddress']  # Update the field name here

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('admin_registration')

        if ClgRegistration.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('admin_registration')

        # Create a new user registration record with all fields
        user_registration = ClgRegistration(
            email=email,
            password=password,
            collegeName=college_name,
            name=name,
            cell=cell,
            location=location
        )
        user_registration.save()

        messages.success(request, "Registration successful. You can now log in.")
        return redirect('admin_login')  # Redirect to the login page after successful registration

    return render(request, "admin_registration.html")



def lectures_seminar(request):
    months_years = LectureEvent.objects.dates('date', 'month')

    # Create a dictionary to store events grouped by month and year
    events_by_month = {}
    for date in months_years:
        month = date.strftime('%B')
        year = date.year
        events = LectureEvent.objects.filter(date__month=date.month, date__year=year)
        events_by_month[(month, year)] = events

    return render(request, 'lectures_seminar.html', {'events_by_month': events_by_month})


def studentevents(request):
    months_years = StudentEvent.objects.dates('date', 'month')

    # Create a dictionary to store events grouped by month and year
    events_by_month = {}
    for date in months_years:
        month = date.strftime('%B')
        year = date.year
        events = StudentEvent.objects.filter(date__month=date.month, date__year=year, deleted=False)
        events_by_month[(month, year)] = events

    return render(request, 'studentevents.html', {'events_by_month': events_by_month})
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404

def deleteStdevents(request,event_title, event_date):

    events = get_list_or_404(StudentEvent, title=event_title, date=event_date)

    for event in events:
        event.deleted = True
        event.save()

    return render(request, 'admin_std_events.html')

def deleteFacevents(request,event_title, event_date):

    events = get_list_or_404(OtherEvent, title=event_title, date=event_date)

    for event in events:
        event.deleted = True
        event.save()

    return render(request, 'admin_fac_events.html')
def deleteLectures(request,event_title, event_date):

    events = get_list_or_404(LectureEvent, title=event_title, date=event_date)

    for event in events:
        event.deleted = True
        event.save()

    return render(request, 'admin_lectures.html')

from datetime import datetime


def filter_events(request):
    selected_month = request.GET.get('month')
    selected_date = None

    if selected_month:
        selected_date = datetime.strptime(selected_month, '%Y-%m')
        formatted_selected_date = selected_date.strftime('%b. %Y')

        faculty_events = OtherEvent.objects.filter(date__month=selected_date.month, date__year=selected_date.year, deleted=False)
        student_events = StudentEvent.objects.filter(date__month=selected_date.month, date__year=selected_date.year, deleted=False)
        lecture_events = LectureEvent.objects.filter(date__month=selected_date.month, date__year=selected_date.year, deleted=False)
    else:
        formatted_selected_date = None
        faculty_events = OtherEvent.objects.filter(deleted=False)
        student_events = StudentEvent.objects.filter(deleted=False)
        lecture_events = LectureEvent.objects.filter(deleted=False)

    return render(request, 'newsreport.html', {'selected_date': formatted_selected_date, 'faculty_events': faculty_events, 'student_events': student_events, 'lecture_events': lecture_events})

def liveevents(request):
    return render(request, "liveevents.html")

def requestform(request):
    return render(request, "requestform.html")

def registration(request):
    return render(request, 'admin_registration.html')

def dashboard(request):
    return render(request,"dashboard.html")

def user_home(request):
    return render(request,"user_home.html")

def facultyevents(request):
    # Get distinct months and years from the 'date' field of FacultyEvent model
    months_year = OtherEvent.objects.dates('date', 'month')

    # Create a dictionary to store events grouped by month and year
    events_by_month = {}
    for date in months_year:
        month = date.strftime('%B')
        year = date.year
        events = OtherEvent.objects.filter(date__month=date.month, date__year=year, deleted = False).order_by('-date')
        events_by_month[(month, year)] = events

    return render(request, 'facultyevents.html', {'events_by_month': events_by_month})
def admin_lectures(request):
    if request.method == 'POST':
        # Process and save the form data to the database
        title = request.POST['title']
        date = request.POST['date']
        location = request.POST['college']
        contact_person = request.POST['location']
        email = request.POST['email']
        cell = request.POST['cell']
        description = request.POST['description']

        # Save the data to the LectureEvent model
        lecture_event = LectureEvent(title=title, date=date, location=location, contact_person=contact_person, email=email, cell=cell, description=description)
        lecture_event.save()

        # Show a success message
        messages.success(request, "Lecture or seminar details added successfully.")

        # Redirect to the same page to display the success message
        return redirect('admin_lectures')
    lecture_events = LectureEvent.objects.filter(deleted = False)

    context = {
        'lecture_events': lecture_events,
    }

    return render(request, 'admin_lectures.html', context)




def admin_fac_events(request):
    if request.method == 'POST':
        # Process and save the form data to the database
        title = request.POST['title']
        date = request.POST['date']
        location = request.POST['college']
        contact_person = request.POST['location']
        email = request.POST['email']
        cell = request.POST['cell']
        description = request.POST['description']

        # Save the data to the FacultyEvent model
        faculty_event = OtherEvent(title=title, date=date, location=location, contact_person=contact_person, email=email, cell=cell, description=description)
        faculty_event.save()

        # Show a success message


        # Redirect to the same page to display the success message
    faculty_events = OtherEvent.objects.filter(deleted = False)

    context = {
        'faculty_events': faculty_events,
    }

    return render(request, 'admin_fac_events.html', context)

def admin_std_events(request):
    if request.method == 'POST':
        # Process and save the form data to the database
        title = request.POST['title']
        date = request.POST['date']
        college = request.POST['college']
        location = request.POST['location']
        description = request.POST['description']



        # Save the data to the StudentEvent model
        student_event = StudentEvent(title=title, date=date, college=college, location=location, description=description, deleted = False)
        student_event.save()


        # Show a success message


        # Redirect to the same page to display the success message
        # return redirect('admin_std_events')

    student_events = StudentEvent.objects.filter(deleted=False)
    context = {
        'student_events': student_events,
    }

    return render(request, 'admin_std_events.html', context)

def submit_feedback(request):
    if request.method == 'POST':
        event_title = request.POST.get('event_title')
        name = request.POST.get('name')
        email = request.POST.get('email')
        feedback_text = request.POST.get('feedback_text')

        # Get the event based on the title
        event = StudentEvent.objects.get(title=event_title)

        # Create and save the feedback
        feedback = StudentEventFeedback(event=event, name=name, email=email, feedback=feedback_text)
        feedback.save()

    return redirect('studentevents')
def submit_lecture_feedback(request):
    if request.method == 'POST':
        event_title = request.POST.get('event_title')
        name = request.POST.get('name')
        email = request.POST.get('email')
        feedback_text = request.POST.get('feedback_text')

        # Get the event based on the title
        event = LectureEvent.objects.get(title=event_title)

        # Create and save the feedback
        feedback = LectureEventFeedback(event=event, name=name, email=email, feedback=feedback_text)
        feedback.save()

    return redirect('lectures_seminar')
def submit_faculty_event_feedback(request):
    if request.method == 'POST':

        event_title = request.POST.get('event_title')
        name = request.POST.get('name')
        email = request.POST.get('email')
        feedback_text = request.POST.get('feedback_text')

        # Get the event based on the title
        event = OtherEvent.objects.get(title=event_title)

        # Create and save the feedback
        feedback = OtherEventFeedback(event=event, name=name, email=email, feedback=feedback_text)
        feedback.save()

        # Redirect to a thank you page or any other appropriate page

    return redirect('facultyevents')







def admin_calender(request):

    events = FinalRequest.objects.filter(acknowledgement=False)

    context = {
            'events' : events
        }
        # print(context)
    return render(request, "admin_calender.html",context)

def get_events(request):
    events = FinalRequest.objects.all()
    event_data = []

    for event in events:
        event_data.append({
            'title': event.program_topic,
            'start': event.start_time(),
            'end': event.end_time(),
            # Replace with the actual field name in your model
             # Replace with the actual field name in your model
        })

    return JsonResponse(event_data, safe=False)
def admin_settings(request):
    return render(request, "admin_settings.html")


def feedback_page(request, event_title):
    # Assuming that event_title corresponds to the event's title in LectureEvent model
    feedbacks = LectureEventFeedback.objects.filter(event__title=event_title)
    context = {'feedbacks': feedbacks,'event_title':event_title}
    return render(request, 'feedback_page.html', context)


def std_feedbacks(request, event_title):
    feedbacks = StudentEventFeedback.objects.filter(event__title=event_title)
    context = {'feedbacks':feedbacks,'event_title':event_title}
    return render(request,'std_feedbacks.html',context)



def fac_feedbacks(request, event_title):
    feedbacks = OtherEventFeedback.objects.filter(event__title=event_title)
    context = {'feedbacks':feedbacks,'event_title':event_title}
    return render(request,'fac_feedbacks.html',context)


def std_login(request):
    months_years = StudentEvent.objects.dates('date', 'month')

    # Create a dictionary to store events grouped by month and year
    events_by_month = {}
    for date in months_years:
        month = date.strftime('%B')
        year = date.year
        events = StudentEvent.objects.filter(date__month=date.month, date__year=year)
        events_by_month[(month, year)] = events

    return render(request, 'std_login.html', {'events_by_month': events_by_month})

def fac_login(request):
    months_year = OtherEvent.objects.dates('date', 'month')

    # Create a dictionary to store events grouped by month and year
    events_by_month = {}
    for date in months_year:
        month = date.strftime('%B')
        year = date.year
        events = OtherEvent.objects.filter(date__month=date.month, date__year=year).order_by('-date')
        events_by_month[(month, year)] = events

    return render(request, 'fac_login.html', {'events_by_month': events_by_month})

def lec_login(request):
    months_years = LectureEvent.objects.dates('date', 'month')

    # Create a dictionary to store events grouped by month and year
    events_by_month = {}
    for date in months_years:
        month = date.strftime('%B')
        year = date.year
        events = LectureEvent.objects.filter(date__month=date.month, date__year=year)
        events_by_month[(month, year)] = events

    return render(request, 'lec_login.html', {'events_by_month': events_by_month})

def submit_request(request):
    if request.method == 'POST':
        # print(request.POST)
        college_name = request.POST.get('college_name')
        number_of_days = request.POST.get('number_of_days')
        date = request.POST.get('date')
        mode_of_event = request.POST.get('mode_of_event')
        program_type = request.POST.get('program_type')
        program_topic = request.POST.get('program_topic')
        program_duration = request.POST.get('program_duration')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        course = request.POST.get('course')
        year = request.POST.get('year')
        branch = request.POST.get('branch')
        semester = request.POST.get('semester')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        terms_and_conditions = request.POST.get('terms_and_conditions') == 'on'
        event = {
            'title': program_topic,
            'start': f'{date}T{start_time}',
            'end': f'{date}T{end_time}',
            # Add other event properties here
        }

        # Create a new Request instance and save it to the database
        request_instance = FinalRequest(
            college_name=college_name,
            number_of_days=number_of_days,
            date=date,
            mode_of_event=mode_of_event,
            program_type=program_type,
            program_topic=program_topic,
            program_duration=program_duration,
            start_time=start_time,
            end_time=end_time,
            course=course,
            year=year,
            branch=branch,
            semester=semester,
            name=name,
            mobile=mobile,
            email=email,
            terms_and_conditions=terms_and_conditions
        )
        request_instance.save()


    events = FinalRequest.objects.all()
    event_data = []

    for event in events:
        event_data.append({
            'title': event.program_topic,
            'start': event.start_time,
            'end': event.end_time,
            # Add other event properties here
        })

    return render(request, 'requestform.html',{'event_data': event_data})



def cal(request):
    all_events = CalEvents.objects.all()
    context = {
        "events":all_events,
    }
    return render(request,'cal.html',context)
def all_events(request):
    cal_events = CalEvents.objects.all()
    student_events = StudentEvent.objects.filter(deleted = False)
    faculty_events = OtherEvent.objects.filter(deleted = False)

    events = []

    # Add CalEvents to the events list
    for cal_event in cal_events:
        events.append({
            'title': cal_event.name,
            'id': cal_event.id,
            'start': cal_event.start.strftime("%Y-%m-%d %H:%M:%S"),
            'end': cal_event.end.strftime("%Y-%m-%d %H:%M:%S"),
        })

    # Add StudentEvents to the events list with college names as titles
    for student_event in student_events:
        events.append({
            'title':"SSDP at "+ student_event.college,
            'start': student_event.date.strftime("%Y-%m-%d"),
            'end': student_event.date.strftime("%Y-%m-%d"),
        })
    for faculty_event in faculty_events:
        events.append({
            'title':"FDP at " + faculty_event.location,
            'start':faculty_event.date.strftime("%Y-%m-%d"),
            'end':faculty_event.date.strftime("%Y-%m-%d"),

        })


    return JsonResponse(events, safe=False)


def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = CalEvents(name=str(title), start=start, end=end)
    event.save()
    data = {}
    return JsonResponse(data)

def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = CalEvents.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)

def remove(request):
    id = request.GET.get("id", None)
    event = CalEvents.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)
def usercal(request):
    return render(request, "usercal.html")



def newsreport(request):
    return render(request, "newsreport.html")

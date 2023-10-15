from django.db import models
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class ClgRegistration(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    collegeName = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    cell = models.CharField(max_length=20)
    location = models.CharField(max_length= 255)

    def __str__(self):
        return self.email


class StudentEvent(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    college = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class FacultyEvent(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    cell = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.title
class LectureEvent(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    cell = models.CharField(max_length=20)
    description = models.TextField()
    deleted = models.BooleanField(default=False)


    def __str__(self):
        return self.title

class LectureEventFeedback(models.Model):
    event = models.ForeignKey(LectureEvent, on_delete=models.CASCADE, related_name='feedback')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    feedback = models.TextField()

    def __str__(self):
        return f"Feedback for {self.event.title} on {self.event.date}"

class FacultyEventFeedback(models.Model):
    event = models.ForeignKey(FacultyEvent, on_delete=models.CASCADE, related_name='feedback')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    feedback_text = models.TextField()

    def __str__(self):
        return f"Feedback for {self.event.title} on {self.event.date}"


class StudentEventFeedback(models.Model):
    event = models.ForeignKey(StudentEvent, on_delete=models.CASCADE, related_name='feedback')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    feedback = models.TextField()

    def __str__(self):
        return f"Feedback for {self.event.title} on {self.event.date}"

class OtherEvent(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    cell = models.CharField(max_length=20)
    description = models.TextField()
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class OtherEventFeedback(models.Model):
    event = models.ForeignKey(OtherEvent, on_delete=models.CASCADE, related_name='feedback')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    feedback = models.TextField()

    def __str__(self):
        return f"Feedback for {self.event.title} on {self.event.date}"

class ClgRequest(models.Model):
    date = models.DateField()
    program_type = models.CharField(max_length=255)
    program_topic = models.CharField(max_length=255, blank=True, null=True)
    program_duration = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    participants_type = models.ManyToManyField('ClgParticipantType')
    course = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    semester = models.CharField(max_length=255)
    mobile = models.CharField(max_length=10)
    email = models.EmailField()
    acknowledgement = models.BooleanField(default=False)
    terms_and_conditions = models.BooleanField()

    def __str__(self):
        return f"Request for {self.date} - {self.program_type}"

class ClgParticipantType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PrincipalRequest(models.Model):
    college_name = models.CharField(max_length=200)
    day = models.CharField(max_length=200)
    date = models.DateField()
    mode = models.CharField(max_length=100, choices=[('Offline', 'Offline'), ('Online', 'Online')])
    participants = models.IntegerField()
    contact_name = models.CharField(max_length=200)
    institution = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    email = models.EmailField()
    program_type = models.CharField(max_length=100, choices=[('Faculty Development Program', 'Faculty Development Program'), ('Student Development Program', 'Student Development Program')])
    topic_guest = models.CharField(max_length=100, null=True, blank=True)
    duration_guest = models.CharField(max_length=100, null=True, blank=True)
    from_time_guest = models.CharField(max_length=100, null=True, blank=True)
    to_time_guest = models.CharField(max_length=100, null=True, blank=True)
    participant_type_guest = models.CharField(max_length=100, choices=[('Students', 'Students'), ('Faculty', 'Faculty')], null=True, blank=True)
    course_guest = models.CharField(max_length=200, null=True, blank=True)
    year = models.CharField(max_length=100, null=True, blank=True)
    branch = models.CharField(max_length=100, null=True, blank=True)
    semester = models.CharField(max_length=100, null=True, blank=True)
    topic_faculty = models.CharField(max_length=100, null=True, blank=True)
    duration_faculty = models.CharField(max_length=100, null=True, blank=True)
    from_time_faculty = models.CharField(max_length=100, null=True, blank=True)
    to_time_faculty = models.CharField(max_length=100, null=True, blank=True)
    topic_student = models.CharField(max_length=100, null=True, blank=True)
    duration_student = models.CharField(max_length=100, null=True, blank=True)
    course = models.CharField(max_length=200, null=True, blank=True)
    student_year = models.CharField(max_length=100, null=True, blank=True)
    student_branch = models.CharField(max_length=100, null=True, blank=True)
    student_semester = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'Request by {self.contact_name} from {self.college_name}'




class College(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Requestsir(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    date = models.DateField()
    number_of_days = models.IntegerField()
    mode_of_event = models.CharField(max_length=255, choices=[("Full day", "Offline"), ("Half day", "Online")])
    program_type = models.CharField(max_length=255, choices=[
        ("Guest Lecture", "Guest Lecture"),
        ("Faculty Development Program", "Faculty Development Program"),
        ("Student Development Program", "Student Development Program")
    ])
    program_topic = models.CharField(max_length=255)
    program_duration = models.CharField(max_length=255, choices=[("Full day", "Full day"), ("Half day", "Half day")])
    start_time = models.TimeField()
    end_time = models.TimeField()
    course = models.CharField(max_length=255, choices=[
        ("B Tech", "B Tech"),
        ("B Pharmacy", "B Pharmacy"),
        ("MBA", "MBA"),
        ("BBA", "BBA"),
        ("B Com", "B Com"),
        ("BA", "BA"),
        ("B Sc", "B Sc")
    ])
    year = models.CharField(max_length=255, choices=[
        ("1st Year", "1st Year"),
        ("2nd Year", "2nd Year"),
        ("3rd Year", "3rd Year"),
        ("4th Year", "4th Year")
    ])
    branch = models.CharField(max_length=255, choices=[
        ("Computer Science", "Computer Science"),
        ("Electrical Engineering", "Electrical Engineering"),
        ("Electronics and Communication Engineering", "Electronics and Communication Engineering"),
        ("Mechanical Engineering", "Mechanical Engineering"),
        ("Civil Engineering", "Civil Engineering"),
        ("Pharmacy", "Pharmacy"),
        ("MBA", "MBA"),
        ("BBA", "BBA"),
        ("Commerce", "Commerce"),
        ("Arts", "Arts"),
        ("Science", "Science")
    ])
    semester = models.CharField(max_length=255, choices=[
        ("1", "1"),
        ("2", "2")
    ])
    name = models.CharField(max_length=128)
    mobile = models.CharField(max_length=10)
    email = models.EmailField()
    terms_and_conditions = models.BooleanField()

    def __str__(self):
        return f"Request for {self.date} - {self.program_type}"


class FinalRequest(models.Model):
    college_name = models.CharField(max_length=255, verbose_name='College Name')
    number_of_days = models.IntegerField(verbose_name='Number of Days')
    date = models.DateField(verbose_name='Date')
    mode_of_event = models.CharField(max_length=255, verbose_name='Mode of Event')
    program_type = models.CharField(max_length=255, verbose_name='Program Type')
    program_topic = models.CharField(max_length=255, verbose_name='Program Topic')
    program_duration = models.CharField(max_length=255, verbose_name='Program Duration')
    start_time = models.TimeField(verbose_name='Start Time')
    end_time = models.TimeField(verbose_name='End Time')
    course = models.CharField(max_length=255, verbose_name='Course')
    year = models.CharField(max_length=255, verbose_name='Year')
    branch = models.CharField(max_length=255, verbose_name='Branch')
    semester = models.IntegerField(verbose_name='Semester')
    name = models.CharField(max_length=128, verbose_name='Contact Person Name')
    mobile = models.CharField(max_length=10, verbose_name='Mobile/WhatsApp Number')
    email = models.EmailField(verbose_name='Email')
    terms_and_conditions = models.BooleanField(verbose_name='Agree to Terms and Conditions')
    acknowledgement = models.BooleanField(default=False, verbose_name='Acknowledgement')

    def __str__(self):
        return f"Request from {self.college_name}"






class CalEvents(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)

    class Meta:
        db_table = "tblevents"

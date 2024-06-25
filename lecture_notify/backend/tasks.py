from datetime import datetime, timedelta, time
import pytz
from django.utils import timezone
from twilio.rest import Client
from backend.models import Lecture, Student
from celery import shared_task

# Twilio credentials
account_sid = 'AC19124da78b12cbcea185bcdf20542b80'
auth_token = '6f42f0638b536754f1655a4d29ca8fd7'
twilio_number = '+14155238886'

@shared_task
def send_whatsapp_notification_to_students():
    # Time zone setup for Nigeria
    nigeria_tz = pytz.timezone('Africa/Lagos')

    # Current time in Nigeria
    now_nigeria = timezone.now().astimezone(nigeria_tz)
    print(f"Current Nigerian time: {now_nigeria}")

    lecture_time = time(3, 35)  # Adjust this to match the lecture time you want to check
    print(f"Lecture time: {lecture_time}")

    # Find lectures scheduled at the specified time
    lectures = Lecture.objects.filter(time=lecture_time)

    if not lectures:
        print("No lectures scheduled at 3:35 AM.")
        return

    for lecture in lectures:
        # Calculate the notification time (1 minute before the lecture)
        lecture_datetime = datetime.combine(lecture.date, lecture.time)
        lecture_datetime_nigeria = nigeria_tz.localize(lecture_datetime)
        notification_time = lecture_datetime_nigeria - timedelta(minutes=1)

        # Check if it's time to send the notification
        if now_nigeria >= notification_time and now_nigeria < lecture_datetime_nigeria:
            print(f"Sending notification for lecture: {lecture.name} at {lecture_datetime_nigeria}")

            # Get students in the same department as the lecture
            students = Student.objects.filter(department=lecture.department)
            client = Client(account_sid, auth_token)

            for student in students:
                try:
                    message = client.messages.create(
                        body=f"Reminder: You have a lecture '{lecture.name}' for the course '{lecture.course}' at {lecture_datetime_nigeria}. Venue: {lecture.venue}",
                        from_=f'whatsapp:{twilio_number}',
                        to=f'whatsapp:{student.phone_number}'
                    )
                    print(f"Message sent successfully to {student.name}: {message.sid}")
                except Exception as e:
                    print(f"Failed to send message to {student.name}: {e}")
        else:
            print(f"Not yet time to send notification for lecture: {lecture.name}")

# Call the function to send notifications (only for manual testing, not for production use with Celery)
# send_whatsapp_notification_to_students()



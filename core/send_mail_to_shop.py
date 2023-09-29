# send email using django EmailMultiAlternatives
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_emails(recepient, order, total_cost, buyer_name, order_id):
    # send email using django EmailMultiAlternatives
    subject = 'Welcome to African Food Store'
    content_dict = {
                    'recepient': recepient, 
                    'order': order, 
                    'total_cost': total_cost, 
                    'buyer_name': buyer_name,
                    'order_id': order_id
                    }
    html_content = render_to_string('emails/receipt_mail.html', content_dict)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [recepient]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
    # return render(request, 'email.html')
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings


def home(request):
    return render(request, 'home.html')

def ethnic_wear(request):
    return render(request, 'ethnic_wear.html')

def office_wear(request):
    return render(request, 'office_wear.html')

def tops_tunics(request):
    return render(request, 'tops_tunics.html')

def collections(request):
    return render(request, 'collections.html')

def contact(request):
    if request.method == 'POST':
        # Form data get karein
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Basic validation
        if not all([name, email, subject, message]):
            messages.error(request, 'Please fill all the fields.')
            return render(request, 'contact.html')
        
        try:
            # Email to admin
            email_subject = f"New Contact Form: {subject}"
            email_message = f"""
            Name: {name}
            Email: {email}
            Subject: {subject}
            
            Message:
            {message}
            
            Sent from Tulsattva website contact form.
            """
            
            send_mail(
                email_subject,
                email_message,
                email,  # From email
                [settings.DEFAULT_FROM_EMAIL],  # To email (admin)
                fail_silently=False,
            )
            
            # Optional: Confirmation email to user
            user_subject = "Thank you for contacting Tulsattva"
            user_message = f"""
            Dear {name},
            
            Thank you for contacting Tulsattva! We have received your message and will get back to you within 24 hours.
            
            Your Message:
            {message}
            
            Best regards,
            Tulsattva Team
            """
            
            send_mail(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Thank you for your message! We will contact you soon.')
            return redirect('contact')
            
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again.')
    
    return render(request, 'contact.html')

def wishlist(request):
    return render(request, 'wishlist.html')

def cart(request):
    return render(request, 'cart.html')

def profile(request):
    return render(request, 'profile.html')

def lookbook(request):  # Add this function
    return render(request, 'lookbook.html')

def faq(request):
    return render(request, 'faq.html')

def returns(request):
    return render(request, 'returns.html')

def shipping(request):
    return render(request, 'shipping.html')

def size_guide(request):
    return render(request, 'size_guide.html')

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')


def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)
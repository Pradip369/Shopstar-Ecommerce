from django.apps import apps
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.core.mail import send_mail

from email_change.forms import EmailChangeForm
from email_change.utils import generate_key
from django.template.loader import render_to_string

from django.contrib.auth import get_user_model
User = get_user_model()

@login_required
def email_change_view(request, extra_context={},
                      success_url='email_verification_sent',
                      template_name='email_change/email_change_form.html',
                      email_message_template_name='email_change/emails/verification_email_message.html',
                      email_subject_template_name='email_change/emails/verification_email_subject.html',
                      form_class=EmailChangeForm):
    
    if request.method == 'POST':
        
        form = form_class(username=request.user.username,
                          data=request.POST,
                          files=request.FILES)
    
        if form.is_valid():
            
            user_email = User.objects.values_list('email',flat=True)
            email = form.cleaned_data.get('email')
        
            if email in user_email:
                return render(request,'email_change/sem_match_email.html')
            
            EmailChangeRequest = apps.get_model('email_change',
                                                 'EmailChangeRequest')

            email = form.cleaned_data.get('email')
            verification_key = generate_key(request.user, email)

            site_name = getattr(settings, 'SITE_NAME',
                                'Please define settings.SITE_NAME')
            domain = getattr(settings, 'SITE_URL', None)

            if domain is None:
                Site = apps.get_model('sites', 'Site')
                current_site = Site.objects.get_current()
                site_name = current_site.name
                domain = current_site.domain

            protocol = 'http'
            if request.is_secure():
                protocol = 'https'

            qs = EmailChangeRequest.objects.filter(user=request.user)
            qs.delete()

            EmailChangeRequest.objects.create(
                user=request.user,
                verification_key=verification_key,
                email=email
            )

            # Prepare context
            c = {
                'email': email,
                'site_domain': domain,
                'site_name': site_name,
                'support_email': settings.SUPPORT_EMAIL,
                'user': request.user,
                'verification_key': verification_key,
                'protocol': protocol,
            }
            c.update(extra_context)

            # Send success email
            subject = render_to_string(email_subject_template_name, c).strip()
            message = render_to_string(email_message_template_name, c)

            send_mail(subject, message, None, [email])

            # Redirect
            return redirect(success_url)

    else:
        form = form_class(username=request.user.username)

  
    extra_context['form'] = form

    return render(request, template_name, extra_context)


@login_required
def email_verify_view(request, verification_key, extra_context={},
                      success_url='email_change_complete',
                      template_name='email_change/email_verify.html'):
    """
    """
    EmailChangeRequest = apps.get_model('email_change', 'EmailChangeRequest')
    try:
        ecr = EmailChangeRequest.objects.get(
            user=request.user, verification_key=verification_key)
    except EmailChangeRequest.DoesNotExist:
        # Return failure response
        return render(request, template_name, extra_context)
    else:
        # Check if the email change request has expired
        if ecr.has_expired():
            ecr.delete()
            # Return failure response
            return render(request, template_name, extra_context)

        # Success. Replace the user's email with the new email
        request.user.email = ecr.email
        request.user.save()
        # Delete the email change request
        ecr.delete()

        # Redirect to success URL
        return redirect(success_url)
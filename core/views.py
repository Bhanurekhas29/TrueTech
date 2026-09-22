import re

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.conf import settings

PHONE_PATTERN = re.compile(r"^[0-9+\-\s()]{7,20}$")

from .models import (
    ContactSection,
    FAQSection,
    FooterSection,
    HeroSection,
    OfficesSection,
    OurProcessSection,
    ProcessSection,
    ServiceShowcase,
    SiteHeader,
    WhatWeDoSection,
    WhoWeAreSection,
    WhySection,
    ContactSubmission,
)


def home(request):
    if request.method == "POST":
        return _handle_contact_submission(request)

    context = {
        "header": SiteHeader.load(),
        "hero": HeroSection.load(),
        "services": ServiceShowcase.objects.filter(is_active=True),
        "who_we_are": WhoWeAreSection.load(),
        "why": WhySection.load(),
        "process": ProcessSection.load(),
        "our_process": OurProcessSection.load(),
        "what_we_do": WhatWeDoSection.load(),
        "offices": OfficesSection.load(),
        "faq": FAQSection.load(),
        "contact": ContactSection.load(),
        "footer": FooterSection.load(),
    }
    return render(request, "core/home.html", context)


def _handle_contact_submission(request):
    full_name = request.POST.get("full_name", "").strip()
    company = request.POST.get("company", "").strip()
    email = request.POST.get("email", "").strip()
    phone = request.POST.get("phone", "").strip()
    service_interested = request.POST.get("service_interested", "").strip()
    requirement = request.POST.get("requirement", "").strip()

    errors = []
    if not full_name:
        errors.append("Please enter your full name.")
    if not company:
        errors.append("Please enter your company name.")
    if not email:
        errors.append("Please enter your email address.")
    else:
        try:
            validate_email(email)
        except ValidationError:
            errors.append("Please enter a valid email address.")
    if phone and not PHONE_PATTERN.match(phone):
        errors.append("Please enter a valid phone number (digits only, with optional +, spaces, hyphens or brackets).")

    if not errors:
        submission = ContactSubmission.objects.create(
            full_name=full_name,
            company=company,
            email=email,
            phone=phone,
            service_interested=service_interested,
            requirement=requirement,
        )
        _notify_new_enquiry(submission)
        messages.success(request, "Thanks — we've received your enquiry and will be in touch shortly.")
    else:
        for error in errors:
            messages.error(request, error)

    return redirect("/#contact")


def _notify_new_enquiry(submission):
    if not settings.EMAIL_HOST_USER:
        return

    plain_text = (
        f"New website enquiry from {submission.full_name} ({submission.company})\n\n"
        f"Name: {submission.full_name}\n"
        f"Company: {submission.company}\n"
        f"Email: {submission.email}\n"
        f"Phone: {submission.phone or '-'}\n"
        f"Service: {submission.service_interested or '-'}\n\n"
        f"Requirement:\n{submission.requirement or '-'}"
    )
    html_body = render_to_string("core/emails/new_enquiry.html", {"submission": submission})

    email = EmailMultiAlternatives(
        subject=f"New enquiry from {submission.full_name} ({submission.company})",
        body=plain_text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.EMAIL_HOST_USER],
        reply_to=[submission.email],
    )
    email.attach_alternative(html_body, "text/html")
    email.send(fail_silently=True)

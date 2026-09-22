from django.db import models


class SingletonModel(models.Model):
    """Base for models that should only ever have one row (one site-wide section)."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteHeader(SingletonModel):
    brand_name = models.CharField(max_length=100, default="TrueTechs")
    tagline = models.CharField(max_length=150, blank=True, help_text="e.g. IT · AUTOMATION · BPO")
    logo = models.ImageField(upload_to="header/", blank=True, null=True)
    cta_text = models.CharField(max_length=50, blank=True, help_text="e.g. Get a quote")
    cta_link = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Header & Navigation"
        verbose_name_plural = "Header & Navigation"

    def __str__(self):
        return "Header & Navigation"


class NavMenuItem(models.Model):
    header = models.ForeignKey(SiteHeader, related_name="nav_items", on_delete=models.CASCADE)
    label = models.CharField(max_length=50)
    link = models.CharField(max_length=255, help_text="URL or path, e.g. /services or #services")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.label


class HeroSection(SingletonModel):
    eyebrow = models.CharField(max_length=100, blank=True, help_text="e.g. IT INFRASTRUCTURE SUPPORT")
    heading_main = models.CharField(max_length=150, help_text="e.g. Keep your systems running")
    heading_highlight = models.CharField(max_length=150, blank=True, help_text="Accent-coloured second line, e.g. day and night.")
    subtext = models.TextField(blank=True)
    background_image = models.ImageField(upload_to="hero/", blank=True, null=True)

    primary_cta_text = models.CharField(max_length=50, blank=True, help_text="e.g. Get a quote")
    primary_cta_link = models.CharField(max_length=255, blank=True)
    secondary_cta_text = models.CharField(max_length=50, blank=True, help_text="e.g. View services")
    secondary_cta_link = models.CharField(max_length=255, blank=True)

    stat_value = models.CharField(max_length=20, blank=True, help_text="e.g. 99.97%")
    stat_caption = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def __str__(self):
        return "Hero Section"


class HeroFeature(models.Model):
    hero = models.ForeignKey(HeroSection, related_name="features", on_delete=models.CASCADE)
    icon = models.CharField(max_length=50, help_text="Material icon name, e.g. bolt, cloud, backup, desktop_windows")
    label = models.CharField(max_length=50, help_text="e.g. 24/7 NOC")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.label


class ServiceShowcase(models.Model):
    IMAGE_LEFT = "left"
    IMAGE_RIGHT = "right"
    IMAGE_POSITION_CHOICES = [(IMAGE_LEFT, "Left"), (IMAGE_RIGHT, "Right")]

    eyebrow = models.CharField(max_length=100, blank=True, help_text="e.g. AI & AUTOMATION")
    heading_main = models.CharField(max_length=150, help_text="e.g. Put the repetitive work on")
    heading_highlight = models.CharField(max_length=150, blank=True, help_text="Accent-coloured second line, e.g. autopilot.")
    subtext = models.TextField(blank=True)
    image = models.ImageField(upload_to="services/", blank=True, null=True)
    image_position = models.CharField(max_length=5, choices=IMAGE_POSITION_CHOICES, default=IMAGE_LEFT)

    image_badge_text = models.CharField(max_length=100, blank=True, help_text="Floating badge on the image, e.g. Live automation running")
    image_tags = models.CharField(max_length=150, blank=True, help_text="Comma-separated short tags shown in the badge, e.g. AI, RPA, DOC, CRM")

    image_stat_value = models.CharField(max_length=20, blank=True, help_text="Stat-style badge on the image, e.g. 24/7")
    image_stat_caption = models.CharField(max_length=100, blank=True, help_text="e.g. Support coverage")

    corner_badge_icon = models.CharField(max_length=50, blank=True, help_text="Material icon name for the floating corner badge")
    corner_badge_title = models.CharField(max_length=100, blank=True, help_text="e.g. Workflows automated / ACTIVE CHANNELS")
    corner_badge_subtitle = models.CharField(max_length=150, blank=True, help_text="e.g. Across 4 service lines / Voice · Chat · Email")

    bottom_tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated pills below the features, e.g. Voice, Email, Chat, WhatsApp, 24/7")

    cta_heading = models.CharField(max_length=150, blank=True, help_text="e.g. Ready to automate?")
    cta_subtext = models.CharField(max_length=200, blank=True, help_text="e.g. We build around your existing systems.")
    cta_button_text = models.CharField(max_length=50, blank=True, help_text="e.g. Get started")
    cta_button_link = models.CharField(max_length=255, blank=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ["order"]

    def __str__(self):
        return self.heading_main


class ServiceFeature(models.Model):
    service = models.ForeignKey(ServiceShowcase, related_name="features", on_delete=models.CASCADE)
    icon = models.CharField(max_length=50, help_text="Material icon name, e.g. smart_toy, sync, description, sync_alt")
    title = models.CharField(max_length=100, help_text="e.g. AI chatbots")
    description = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class WhoWeAreSection(SingletonModel):
    eyebrow = models.CharField(max_length=100, blank=True, help_text="e.g. WHO WE ARE")
    heading = models.CharField(max_length=255, help_text="e.g. Two offices, one team, and the work that never stops.")
    body_text = models.TextField(blank=True, help_text="Paragraphs separated by a blank line")

    office1_image = models.ImageField(upload_to="offices/", blank=True, null=True)
    office1_badge_label = models.CharField(max_length=50, blank=True, help_text="e.g. HEAD OFFICE")
    office1_city = models.CharField(max_length=100, blank=True, help_text="e.g. Dubai, UAE")
    office1_subcaption = models.CharField(max_length=150, blank=True, help_text="e.g. Commercial relationship · GST UTC+4")
    office1_pill_label = models.CharField(max_length=30, blank=True, help_text="e.g. DUBAI")

    office2_image = models.ImageField(upload_to="offices/", blank=True, null=True)
    office2_badge_label = models.CharField(max_length=50, blank=True, help_text="e.g. DELIVERY CENTRE")
    office2_city = models.CharField(max_length=100, blank=True, help_text="e.g. Chennai, India")
    office2_subcaption = models.CharField(max_length=150, blank=True, help_text="e.g. Technical delivery · IST UTC+5:30")
    office2_pill_label = models.CharField(max_length=30, blank=True, help_text="e.g. CHENNAI")

    stat1_value = models.CharField(max_length=20, blank=True, help_text="e.g. 24/7")
    stat1_label = models.CharField(max_length=100, blank=True, help_text="e.g. Monitoring & service desk")
    stat2_value = models.CharField(max_length=20, blank=True, help_text="e.g. 2")
    stat2_label = models.CharField(max_length=100, blank=True, help_text="e.g. Offices, one team")
    stat3_value = models.CharField(max_length=20, blank=True, help_text="e.g. 8")
    stat3_label = models.CharField(max_length=100, blank=True, help_text="e.g. Service lines")

    class Meta:
        verbose_name = "Who We Are"
        verbose_name_plural = "Who We Are"

    def __str__(self):
        return "Who We Are"


class WhySection(SingletonModel):
    eyebrow = models.CharField(max_length=100, blank=True, help_text="e.g. WHY WORK WITH US")
    heading = models.CharField(max_length=255, help_text="e.g. Support measured by what it changes in your operation.")
    subtext = models.TextField(blank=True)
    image = models.ImageField(upload_to="why/", blank=True, null=True)
    image_badge_label = models.CharField(max_length=100, blank=True, help_text="e.g. One partner")
    image_badge_value = models.CharField(max_length=100, blank=True, help_text="e.g. 8 service lines")

    class Meta:
        verbose_name = "Why Work With Us"
        verbose_name_plural = "Why Work With Us"

    def __str__(self):
        return "Why Work With Us"


class WhyFeature(models.Model):
    section = models.ForeignKey(WhySection, related_name="features", on_delete=models.CASCADE)
    icon = models.CharField(max_length=50, help_text="Material icon name, e.g. verified_user, bolt, trending_up")
    title = models.CharField(max_length=100, help_text="e.g. Reliable expertise")
    description = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Alternates left/right around the image in display order")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class ProcessSection(SingletonModel):
    eyebrow = models.CharField(max_length=100, blank=True, help_text="e.g. HOW WE WORK")
    heading = models.CharField(max_length=255, help_text="e.g. Three commitments we hold to on every engagement.")

    class Meta:
        verbose_name = "How We Work"
        verbose_name_plural = "How We Work"

    def __str__(self):
        return "How We Work"


class ProcessStep(models.Model):
    section = models.ForeignKey(ProcessSection, related_name="steps", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="process/", blank=True, null=True)
    title = models.CharField(max_length=100, help_text="e.g. Scoped, not templated")
    description = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Also sets the displayed step number (01, 02, ...)")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class OurProcessSection(SingletonModel):
    eyebrow = models.CharField(max_length=100, blank=True, help_text="e.g. OUR PROCESS")
    heading = models.CharField(max_length=255, help_text="e.g. From first assessment to steady state.")
    subtext = models.CharField(max_length=255, blank=True, help_text="e.g. The same six steps whether we take one service line or several.")

    class Meta:
        verbose_name = "Our Process"
        verbose_name_plural = "Our Process"

    def __str__(self):
        return "Our Process"


class OurProcessStep(models.Model):
    section = models.ForeignKey(OurProcessSection, related_name="steps", on_delete=models.CASCADE)
    icon = models.CharField(max_length=50, blank=True, help_text="Material icon name, e.g. adjust, share, link, account_tree, headset_mic, auto_awesome")
    title = models.CharField(max_length=100, help_text="e.g. Assess")
    description = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Also sets the displayed step number (01, 02, ...)")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class WhatWeDoSection(SingletonModel):
    eyebrow = models.CharField(max_length=100, blank=True, help_text="e.g. WHAT WE DO")
    heading = models.CharField(max_length=255, help_text="e.g. Eight service lines, one point of contact.")
    subtext = models.CharField(max_length=255, blank=True, help_text="e.g. Take a single line, or run several under one agreement with the same team behind them.")

    class Meta:
        verbose_name = "What We Do"
        verbose_name_plural = "What We Do"

    def __str__(self):
        return "What We Do"


class WhatWeDoItem(models.Model):
    section = models.ForeignKey(WhatWeDoSection, related_name="items", on_delete=models.CASCADE)
    icon = models.CharField(max_length=50, help_text="Material icon name, e.g. hub, security, smart_toy")
    title = models.CharField(max_length=100, help_text="e.g. 24/7 IT Infrastructure Support")
    description = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="what-we-do/", blank=True, null=True)
    bullet_points = models.TextField(blank=True, help_text="One bullet per line, e.g. 24/7 NOC and service desk")
    cta_text = models.CharField(max_length=50, blank=True, default="Enquire About This Service")
    cta_link = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Also sets the displayed number (01, 02, ...)")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class OfficesSection(SingletonModel):
    eyebrow = models.CharField(max_length=100, blank=True, help_text="e.g. WHERE WE WORK FROM")
    heading = models.CharField(max_length=255, help_text="e.g. Dubai for the relationship, Chennai for the engineering.")
    subtext = models.TextField(blank=True)

    office1_image = models.ImageField(upload_to="offices/", blank=True, null=True)
    office1_badge_label = models.CharField(max_length=50, blank=True, help_text="e.g. HEAD OFFICE")
    office1_city = models.CharField(max_length=100, blank=True, help_text="e.g. Dubai, UAE")
    office1_address = models.CharField(max_length=255, blank=True)
    office1_timezone = models.CharField(max_length=50, blank=True, help_text="e.g. GST · UTC+4")
    office1_phone = models.CharField(max_length=30, blank=True)

    office2_image = models.ImageField(upload_to="offices/", blank=True, null=True)
    office2_badge_label = models.CharField(max_length=50, blank=True, help_text="e.g. DELIVERY CENTRE")
    office2_city = models.CharField(max_length=100, blank=True, help_text="e.g. Chennai, India")
    office2_address = models.CharField(max_length=255, blank=True)
    office2_timezone = models.CharField(max_length=50, blank=True, help_text="e.g. IST · UTC+5:30")
    office2_phone = models.CharField(max_length=30, blank=True)

    banner_icon1 = models.CharField(max_length=50, blank=True, help_text="Material icon name, e.g. schedule")
    banner_title1 = models.CharField(max_length=100, blank=True, help_text="e.g. Around the clock")
    banner_text1 = models.CharField(max_length=255, blank=True)

    banner_icon2 = models.CharField(max_length=50, blank=True, help_text="Material icon name, e.g. public")
    banner_title2 = models.CharField(max_length=100, blank=True, help_text="e.g. Channels")
    banner_tags2 = models.CharField(max_length=150, blank=True, help_text="Comma-separated, e.g. Voice, Chat, Email")

    class Meta:
        verbose_name = "Offices"
        verbose_name_plural = "Offices"

    def __str__(self):
        return "Offices"


class FAQSection(SingletonModel):
    eyebrow = models.CharField(max_length=100, blank=True, help_text="e.g. QUESTIONS")
    heading = models.CharField(max_length=255, help_text="e.g. What clients ask before they start.")
    image = models.ImageField(upload_to="faq/", blank=True, null=True)
    quote_text = models.TextField(blank=True, help_text="e.g. One point of contact for your core operational needs, with consistent quality and measurable results.")
    quote_attribution = models.CharField(max_length=100, blank=True, help_text="e.g. TrueTechs")

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"

    def __str__(self):
        return "FAQ"


class FAQItem(models.Model):
    section = models.ForeignKey(FAQSection, related_name="items", on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.question


class ContactSection(SingletonModel):
    eyebrow = models.CharField(max_length=100, blank=True, help_text="e.g. GET IN TOUCH")
    heading = models.CharField(max_length=255, help_text="e.g. Tell us what your operation needs.")
    subtext = models.TextField(blank=True)
    background_image = models.ImageField(upload_to="contact/", blank=True, null=True)
    submit_button_text = models.CharField(max_length=50, blank=True, default="Send Your Enquiry")

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contact"

    def __str__(self):
        return "Contact"


class ContactChecklistItem(models.Model):
    section = models.ForeignKey(ContactSection, related_name="checklist_items", on_delete=models.CASCADE)
    text = models.CharField(max_length=200, help_text="e.g. One point of contact across all service lines")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.text


class ContactSubmission(models.Model):
    full_name = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    service_interested = models.CharField(max_length=150, blank=True)
    requirement = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Enquiry"
        verbose_name_plural = "Enquiries"
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.full_name} ({self.company})"


class FooterSection(SingletonModel):
    description = models.TextField(blank=True, help_text="e.g. IT infrastructure, automation and business process operations — delivered from Dubai and Chennai.")

    whatsapp_number = models.CharField(max_length=255, blank=True, help_text="Digits only with country code (e.g. 971501234567) for WhatsApp links, or paste a full URL to link elsewhere instead")
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    phone_number = models.CharField(max_length=30, blank=True, help_text="e.g. +971 50 123 4567 (used for the call icon)")

    contact_email = models.CharField(max_length=150, blank=True, help_text="e.g. hello@truetechs.com, or 'To be confirmed'")
    hours_text = models.CharField(max_length=150, blank=True, help_text="e.g. Service desk 24/7 · Office hours GST and IST")

    copyright_text = models.CharField(max_length=150, blank=True, help_text="e.g. © 2026 TrueTechs. All rights reserved.")
    bottom_note = models.CharField(max_length=150, blank=True, help_text="e.g. 24/7 monitoring and service desk")

    class Meta:
        verbose_name = "Footer"
        verbose_name_plural = "Footer"

    def __str__(self):
        return "Footer"


class FooterLink(models.Model):
    section = models.ForeignKey(FooterSection, related_name="links", on_delete=models.CASCADE)
    group_label = models.CharField(max_length=50, help_text="Column this link appears under, e.g. Quick Links, Services")
    label = models.CharField(max_length=100)
    link = models.CharField(max_length=255, help_text="URL or path")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["group_label", "order"]

    def __str__(self):
        return f"{self.group_label} — {self.label}"

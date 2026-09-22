from django.contrib import admin
from django.shortcuts import redirect

from .models import (
    ContactChecklistItem,
    ContactSection,
    ContactSubmission,
    FAQItem,
    FAQSection,
    FooterLink,
    FooterSection,
    HeroFeature,
    HeroSection,
    NavMenuItem,
    ServiceFeature,
    ServiceShowcase,
    OfficesSection,
    OurProcessSection,
    OurProcessStep,
    ProcessSection,
    ProcessStep,
    SiteHeader,
    WhatWeDoItem,
    WhatWeDoSection,
    WhoWeAreSection,
    WhyFeature,
    WhySection,
)


class SingletonAdmin(admin.ModelAdmin):
    """Skips the changelist entirely — the menu entry opens straight to the one row."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = self.model.load()
        return redirect("admin:%s_%s_change" % (self.model._meta.app_label, self.model._meta.model_name), obj.pk)


class NavMenuItemInline(admin.TabularInline):
    model = NavMenuItem
    extra = 1
    fields = ("label", "link", "order", "is_active")


@admin.register(SiteHeader)
class SiteHeaderAdmin(SingletonAdmin):
    inlines = [NavMenuItemInline]
    fieldsets = (
        (None, {"fields": ("brand_name", "tagline", "logo")}),
        ("Call to action", {"fields": ("cta_text", "cta_link")}),
    )


class HeroFeatureInline(admin.TabularInline):
    model = HeroFeature
    extra = 1
    fields = ("icon", "label", "order")


@admin.register(HeroSection)
class HeroSectionAdmin(SingletonAdmin):
    inlines = [HeroFeatureInline]
    fieldsets = (
        ("General", {"fields": ("eyebrow", "heading_main", "heading_highlight", "subtext", "background_image")}),
        ("Call to action", {"fields": ("primary_cta_text", "primary_cta_link", "secondary_cta_text", "secondary_cta_link")}),
        ("Stat badge", {"fields": ("stat_value", "stat_caption")}),
    )


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1
    fields = ("icon", "title", "description", "order")


@admin.register(ServiceShowcase)
class ServiceShowcaseAdmin(admin.ModelAdmin):
    list_display = ("heading_main", "eyebrow", "order", "is_active")
    list_editable = ("order", "is_active")
    inlines = [ServiceFeatureInline]
    fieldsets = (
        ("General", {"fields": ("eyebrow", "heading_main", "heading_highlight", "subtext", "image", "image_position", "order", "is_active")}),
        ("Image badges", {"fields": ("image_badge_text", "image_tags", "image_stat_value", "image_stat_caption", "corner_badge_icon", "corner_badge_title", "corner_badge_subtitle")}),
        ("Bottom tags", {"fields": ("bottom_tags",)}),
        ("CTA banner", {"fields": ("cta_heading", "cta_subtext", "cta_button_text", "cta_button_link")}),
    )


@admin.register(WhoWeAreSection)
class WhoWeAreSectionAdmin(SingletonAdmin):
    fieldsets = (
        ("General", {"fields": ("eyebrow", "heading", "body_text")}),
        ("Office 1", {"fields": ("office1_image", "office1_badge_label", "office1_city", "office1_subcaption", "office1_pill_label")}),
        ("Office 2", {"fields": ("office2_image", "office2_badge_label", "office2_city", "office2_subcaption", "office2_pill_label")}),
        ("Stats", {"fields": ("stat1_value", "stat1_label", "stat2_value", "stat2_label", "stat3_value", "stat3_label")}),
    )


class WhyFeatureInline(admin.TabularInline):
    model = WhyFeature
    extra = 1
    fields = ("icon", "title", "description", "order")


@admin.register(WhySection)
class WhySectionAdmin(SingletonAdmin):
    inlines = [WhyFeatureInline]
    fieldsets = (
        ("General", {"fields": ("eyebrow", "heading", "subtext", "image")}),
        ("Image badge", {"fields": ("image_badge_label", "image_badge_value")}),
    )


class ProcessStepInline(admin.TabularInline):
    model = ProcessStep
    extra = 1
    fields = ("image", "title", "description", "order")


@admin.register(ProcessSection)
class ProcessSectionAdmin(SingletonAdmin):
    inlines = [ProcessStepInline]
    fieldsets = (
        ("General", {"fields": ("eyebrow", "heading")}),
    )


class OurProcessStepInline(admin.TabularInline):
    model = OurProcessStep
    extra = 1
    fields = ("icon", "title", "description", "order")


@admin.register(OurProcessSection)
class OurProcessSectionAdmin(SingletonAdmin):
    inlines = [OurProcessStepInline]
    fieldsets = (
        ("General", {"fields": ("eyebrow", "heading", "subtext")}),
    )


class WhatWeDoItemInline(admin.StackedInline):
    model = WhatWeDoItem
    extra = 1
    fields = ("icon", "title", "description", "image", "bullet_points", "cta_text", "cta_link", "order")


@admin.register(WhatWeDoSection)
class WhatWeDoSectionAdmin(SingletonAdmin):
    inlines = [WhatWeDoItemInline]
    fieldsets = (
        ("General", {"fields": ("eyebrow", "heading", "subtext")}),
    )


@admin.register(OfficesSection)
class OfficesSectionAdmin(SingletonAdmin):
    fieldsets = (
        ("General", {"fields": ("eyebrow", "heading", "subtext")}),
        ("Office 1", {"fields": ("office1_image", "office1_badge_label", "office1_city", "office1_description", "office1_address", "office1_timezone", "office1_phone")}),
        ("Office 2", {"fields": ("office2_image", "office2_badge_label", "office2_city", "office2_description", "office2_address", "office2_timezone", "office2_phone")}),
        ("Card 3 (coverage / channels)", {"fields": ("banner_image", "banner_icon1", "banner_badge1", "banner_title1", "banner_text1", "banner_icon2", "banner_title2", "banner_tags2")}),
    )


class FAQItemInline(admin.TabularInline):
    model = FAQItem
    extra = 1
    fields = ("question", "answer", "order")


@admin.register(FAQSection)
class FAQSectionAdmin(SingletonAdmin):
    inlines = [FAQItemInline]
    fieldsets = (
        ("General", {"fields": ("eyebrow", "heading", "image")}),
        ("Quote", {"fields": ("quote_text", "quote_attribution")}),
    )


class ContactChecklistItemInline(admin.TabularInline):
    model = ContactChecklistItem
    extra = 1
    fields = ("text", "order")


@admin.register(ContactSection)
class ContactSectionAdmin(SingletonAdmin):
    inlines = [ContactChecklistItemInline]
    fieldsets = (
        ("General", {"fields": ("eyebrow", "heading", "subtext", "background_image", "submit_button_text")}),
    )


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("full_name", "company", "email", "phone", "service_interested", "submitted_at")
    list_filter = ("service_interested", "submitted_at")
    search_fields = ("full_name", "company", "email", "phone")
    readonly_fields = ("full_name", "company", "email", "phone", "service_interested", "requirement", "submitted_at")

    def has_add_permission(self, request):
        return False


class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1
    fields = ("group_label", "label", "link", "order")


@admin.register(FooterSection)
class FooterSectionAdmin(SingletonAdmin):
    inlines = [FooterLinkInline]
    fieldsets = (
        ("General", {"fields": ("description",)}),
        ("Social links", {"fields": ("whatsapp_number", "linkedin_url", "twitter_url", "instagram_url", "facebook_url", "youtube_url")}),
        ("Contact info", {"fields": ("contact_email", "phone_number", "hours_text")}),
        ("Bottom bar", {"fields": ("copyright_text", "bottom_note")}),
    )

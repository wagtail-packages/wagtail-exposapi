from django.db import models
from django.http import HttpResponse
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet


class HomePage(Page):
    pass


class SecondHomePage(Page):
    pass


class StandardPageOne(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


class StandardPageTwo(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


class StandardPageThree(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


class FormFieldOne(AbstractFormField):
    page = ParentalKey(
        "FormPageOne", on_delete=models.CASCADE, related_name="form_fields"
    )


class FormPageOne(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Form fields"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            "Email",
        ),
    ]


class FormFieldTwo(AbstractFormField):
    page = ParentalKey(
        "FormPageTwo", on_delete=models.CASCADE, related_name="form_fields"
    )


class FormPageTwo(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Form fields"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            "Email",
        ),
    ]


@register_snippet
class TestSnippetOne(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Test Snippet One"
        verbose_name_plural = "Test Snippets One"


@register_snippet
class TestSnippetTwo(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Test Snippet Two"
        verbose_name_plural = "Test Snippets Two"


@register_snippet
class TestSnippetThree(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Test Snippet Three"
        verbose_name_plural = "Test Snippets Three"


class TestModelAdminOne(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Model Admin One"
        verbose_name_plural = "Model Admins One"


class TestModelAdminTwo(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Model Admin Two"
        verbose_name_plural = "Model Admins Two"


class TestModelAdminThree(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Model Admin Three"
        verbose_name_plural = "Model Admins Three"


@register_setting
class GenericSettingOne(BaseGenericSetting):
    name = models.CharField(max_length=255)


@register_setting
class GenericSettingTwo(BaseGenericSetting):
    name = models.CharField(max_length=255)


@register_setting
class GenericSettingThree(BaseGenericSetting):
    name = models.CharField(max_length=255)


@register_setting
class SiteSettingOne(BaseSiteSetting):
    name = models.CharField(max_length=255)


@register_setting
class SiteSettingTwo(BaseSiteSetting):
    name = models.CharField(max_length=255)


@register_setting
class SiteSettingThree(BaseSiteSetting):
    name = models.CharField(max_length=255)


class FrontendPage500(Page):
    # returns a 500 response
    def serve(self, request, *args, **kwargs):
        return HttpResponse(status=500)


class FrontendPage404(Page):
    # returns a 404 response
    def serve(self, request, *args, **kwargs):
        return HttpResponse(status=404)


class FrontendPage302(Page):
    # returns a 302 response
    def serve(self, request, *args, **kwargs):
        return HttpResponse(status=302)


class FrontendPage200(Page):
    # returns a 200 response
    def serve(self, request, *args, **kwargs):
        return HttpResponse(status=200)

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, ButtonHolder, Submit, HTML, Field, Button
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from apps.blog.models import Article


class ArticleForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField(
        widget=forms.HiddenInput(), required=False, initial=False
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Article title"}),
        max_length=400,
        required=True,
        label="Title of your masterpiece",
    )
    content = forms.CharField(
        widget=SummernoteInplaceWidget(attrs={"summernote": {"width": "100%", "height": "350px"}}),
        max_length=10000,
        help_text="Think about how to use images, subheadings, testimonials and the length of your main content",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            "title",
            "content",
            "status",
            "edited",
            ButtonHolder(
                Submit("submit", "Publish", css_class="publish btn btn-lg btn-primary mr-2"),
                HTML(
                    """
                    <button type="button" class="btn btn-lg btn-subtle-primary draft mr-2">Save as draft</button>
                    <a href="{% url 'articles:list' %}" class="btn btn-lg btn-default">Cancel</a>
                    """
                )
                ),
        )

    class Meta:
        model = Article
        fields = ["title", "content", "status", "edited"]
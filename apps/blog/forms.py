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
        help_text="max 10000 characters",
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
            HTML(
                """
                {% if article.payments.all %}
                <div id="publishInvoice" class="mt-3">
                    {% for payment in article.payments.all %}
                    {% include 'partials/partial_pub_invoice.html' %}
                    {% endfor %}
                </div>
                {% endif %}
                """
            ),
            ButtonHolder(
                Submit("submit", "Save as draft", css_class="publish btn btn-lg btn-subtle-success mr-2"),
                HTML(
                    """
                    <a href="{% url 'articles:list' %}" class="btn btn-lg btn-subtle-dark">Cancel</a>
                    """
                )
                ),
        )

    class Meta:
        model = Article
        fields = ["title", "content", "status", "edited"]
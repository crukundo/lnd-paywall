from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, ButtonHolder, Submit, HTML, Field, Button
from tinymce.widgets import TinyMCE
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
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}),
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
                {% if payment_made %}
                <div id='paymentStatus' data-status='paid' class='alert alert-success' role='alert'>Payment confirmed. Thank you</div>
                {% else %}
                <div id="publishInvoice" class="mt-3">
                    {% if invoice %}
                    {% include 'partials/partial_invoice.html' with purpose='publish' %}
                    {% endif %}
                </div>
                {% endif %}
                """
            ),
            ButtonHolder(
                Submit("publish", "Publish article", css_class="publish btn btn-lg btn-success mr-2"),
                Submit("save", "Save as draft", css_class="draft btn btn-lg btn-subtle-primary mr-2"),
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
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError



from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit
from crispy_forms.bootstrap import InlineRadios

from .models import Ticket, Review, UserFollows

User = get_user_model()


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {
            'description':forms.Textarea(),
            'image' : forms.FileInput()
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
             Fieldset(
                "Livre / Article",
                Row(
                    Column("title"),
                ),
                Row(
                    Column("description"),
                ),
                Row(
                    Column("image"),
                ),

                # Utilisez des classes css pour le style
                style="""
                    border: 1px black solid; 
                    border-radius: 10px; 
                    margin-bottom: 1rem;
                """,
            ), 
        )


class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    CHOICES =[(0,0), (1,1), (2,2), (3, 3), (4,4), (5,5)]
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={
                'class': 'd-flex justify-content-around'}), label="Note")
    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Critique",
                Row(
                    Column("headline"),
                ),
                Row(
                    InlineRadios("rating"),
                ),
                Row(
                    Column("body"),
                ),
                # Utilisez des classes css pour le style
                style="""
                    border: 1px black solid; 
                    border-radius: 10px; 
                    margin-bottom: 2rem;
                    padding: 1rem;
                """,
            ),
        )
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
        self.helper.form_method = 'POST'


class FollowUsersForm(forms.ModelForm):
    followed_user = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': "Nom de l'utilisateur a suivre..."}))  
    class Meta:
        model = UserFollows
        fields = ["followed_user"]

    def clean(self):
        cleaned_data = super().clean()
        try:
            user = User.objects.get(username=self.cleaned_data["followed_user"])
            cleaned_data["followed_user"] = user
        except(User.DoesNotExist, ValueError):
            cleaned_data["followed_user"] = None
            raise ValidationError("Cet utilisateur n'existe pas !")

        return cleaned_data

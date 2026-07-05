from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:

        model = Review

        fields = [

            "rating",

            "review",

        ]

        widgets = {

            "review": forms.Textarea(

                attrs={

                    "rows": 5,

                    "placeholder": "Write your review..."

                }

            ),

        }
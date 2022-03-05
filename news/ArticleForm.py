from django import forms


class ArticleForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    title = forms.CharField(max_length=200)


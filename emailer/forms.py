from django import forms

class PromptForm(forms.Form):
    recipients = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Comma separated emails'}))
    prompt = forms.CharField(widget=forms.Textarea)
    generated_email = forms.CharField(widget=forms.Textarea, required=False)

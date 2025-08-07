from django.shortcuts import render
from .forms import PromptForm
import requests
from django.core.mail import EmailMessage

GROQ_API_KEY = 'Mention_API_KEY_Here'
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

def home(request):
    if request.method == 'POST':
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            headers = {
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            }
            data = {
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
            response = requests.post(GROQ_API_URL, headers=headers, json=data)
            email_content = response.json()['choices'][0]['message']['content']
            form.initial['generated_email'] = email_content
            return render(request, 'emailer/generated.html', {'form': form, 'email_content': email_content})
    else:
        form = PromptForm()
    return render(request, 'emailer/home.html', {'form': form})

def send_email(request):
    if request.method == 'POST':
        recipients = request.POST['recipients'].split(',')
        email_body = request.POST['generated_email']
        email = EmailMessage(
            subject="AI Generated Email",
            body=email_body,
            from_email='your_email@gmail.com',
            to=recipients
        )
        email.send()
        return render(request, 'emailer/home.html', {'form': PromptForm(), 'message': 'Email Sent Successfully!'})

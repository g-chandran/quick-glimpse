from django.shortcuts import render
from django.http import HttpResponseRedirect
from nltk import text, tokenize
from nltk.util import tokenwrap
from numpy import extract
from requests.api import request
from .forms import InputDataForm
from .runner import *
import urllib.request
from bs4 import BeautifulSoup
from bs4.element import Comment
import nltk.data

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


def retrieve_data(input_data):
    return getData(input_data)


def extract_text_from_html(link):
    html_data = urllib.request.urlopen(link).read()
    soup = BeautifulSoup(html_data, 'html.parser')
    text = [i.get_text() for i in soup.find_all('p')]
    return " ".join(t.strip() for t in text)


def print_data(inp):
    print("Word Length: " + str(len(inp.split(" "))))
    data = tokenizer.tokenize(inp)
    print("Sentence Length: " + str(len(data)))


def text_validator(inp):
    sentence = tokenizer.tokenize(inp)
    if len(sentence) > 30:
        return " ".join(sentence[:15] + sentence[len(sentence) - 15:])
    return " ".join(sentence)


def get_data(request):
    if request.method == 'POST':
        form = InputDataForm(request.POST, request.FILES)
        original_data = input_data = ""

        if form.is_valid():
            if 'text' in request.POST:
                input_data = form.cleaned_data['enter_text']
                original_data = text_validator(input_data)
            elif 'url' in request.POST:
                input_data = extract_text_from_html(form.cleaned_data['enter_url'])
                original_data = text_validator(input_data)
            elif 'file' in request.POST:
                input_file = form.cleaned_data['enter_file']
                if (input_file):
                    input_data = input_file.read().decode('utf-8')
                    original_data = text_validator(input_data)
            if original_data != "":
                result = retrieve_data(original_data)
                print(result)
            else:
                result = ""
            # return HttpResponseRedirect('/result')
            return render(request, 'home.html', {'result_data': result, 'form': form, 'input_data': input_data})
    else:
        form = InputDataForm()
        return render(request, 'home.html', {'form': form})

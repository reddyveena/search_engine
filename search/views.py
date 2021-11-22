from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
import requests
from bs4 import BeautifulSoup as bs
from spellchecker import SpellChecker
# Create your views here.

def index(request):
    return render(request, 'index.html')

def search(request):
    if request.method == 'POST':
        search1 = request.POST['search']
        spell = SpellChecker()
        misspelled = spell.unknown([search1])
        if misspelled:
            print(misspelled)
            for word in misspelled:
                # Get the one `most likely` answer
                print(spell.correction(word))
                search = spell.correction(word)
                # Get a list of `likely` options
                print(spell.candidates(word))
            url = 'https://www.ask.com/web?q='+search
        else:
            url = 'https://www.ask.com/web?q=' + search1
        res = requests.get(url)
        print("ask = ",res)
        soup = bs(res.text, 'lxml')

        top_first_related = soup.find_all('ul', {'class': 'PartialRelatedSearch-first-column'})
        #print(top)
        if not top_first_related:
            final_result1 = []
        else:
            for d in top_first_related:
                result_listings1 = d.find_all('li', {'class': 'PartialRelatedSearch-item'})

            #print(result_listings1)

            final_result1 = []

            for result in result_listings1:
                result_text = result.find(class_='PartialRelatedSearch-item-link-text').text
                #result_title = result.find('span').text
                result_url = result.find('a').get('href')
                final_result1.append((result_text, result_url))

            #print(final_result1)

        top_second_related = soup.find_all('ul', {'class': 'PartialRelatedSearch-second-column'})
        #print
        if not top_second_related:
            final_result2 = []
        else:
            for d in top_second_related:
                result_listings2 = d.find_all('li', {'class': 'PartialRelatedSearch-item'})

        #print(result_listings1)

            final_result2 = []

            for result in result_listings2:
                result_text = result.find(class_='PartialRelatedSearch-item-link-text').text
                #result_title = result.find('span').text
                result_url = result.find('a').get('href')
                final_result2.append((result_text, result_url))

        result_listings3 = soup.find_all('div', {'class': 'PartialSearchResults-item'})

        final_result3 = []

        for result in result_listings3:
            result_title = result.find(class_='PartialSearchResults-item-title').text
            result_url = result.find('a').get('href')
            result_desc = result.find(class_='PartialSearchResults-item-abstract').text
            final_result3.append((result_title, result_url, result_desc))

        #print(final_result2)
        if misspelled:
            url1 = 'https://www.bing.com/search?q=' + search
        else:
            url1 = 'https://www.bing.com/search?q=' + search1
        res1 = requests.get(url1)
        print("bing = ",res1)
        soup1 = bs(res1.text, 'lxml')

        result_listings4 = soup1.find_all('li', {'class': 'b_algo'})
        final_result4 = []

        for result in result_listings4:
            result_title = result.find('h2').text
            result_url = result.find('a').get('href')
            result_desc = result.find('p').text

            final_result4.append((result_title, result_url, result_desc))
        #print(final_result4)

        if misspelled:
            res2 = requests.get('https://www.bing.com/images/search?q='+search)
        else:
            res2 = requests.get('https://www.bing.com/images/search?q=' + search1)
        print("bing = ", res2)
        soup2 = bs(res2.text, 'lxml')
        img = soup2.find_all('div', {'class': 'imgpt'})

        imgres2 = []
        for result in img:
            if result is not None:
                url = result.find('a').get('href')
                src = result.find('img').get('src')
                imgres2.append((url,src))


        if misspelled:
            context = {
                'search1': search1,
                'search': search,
                'final_result1': final_result1,
                'final_result2': final_result2,
                'final_result3': final_result3,
                'final_result4': final_result4,
                'imgres':imgres2,
            }
        else:
            context = {
                'final_result1': final_result1,
                'final_result2': final_result2,
                'final_result3': final_result3,
                'final_result4': final_result4,
                'imgres': imgres2,
            }

        #def images(img):
            #context = {
                #'imgres': img,
            #}
            #return render('images.html', context)
        #images=images(imgres2)

        return render(request, 'search.html', context)


    else:
        return render(request, 'search.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Sorry,Username Taken!')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Sorry,Email Taken!')
                return redirect('register')
            else:
                newuser = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name,last_name=last_name);
                newuser.save();
                messages.info(request, 'User created :) ')
                return redirect('login')

        else:
            messages.info(request,'Sorry, passwords are not matching.. ')
            return redirect('register')
        return redirect('/')
    else:
        return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def images(request):
    if request.method == 'POST':
        search1 = request.POST['search']
        spell = SpellChecker()
        misspelled = spell.unknown([search1])
        if misspelled:
            print(misspelled)
            for word in misspelled:
                # Get the one `most likely` answer
                print(spell.correction(word))
                search = spell.correction(word)
                # Get a list of `likely` options
                print(spell.candidates(word))
                url = 'https://www.bing.com/images/search?q=' + search
        else:
            url = 'https://www.bing.com/images/search?q='+search1
        res2 = requests.get(url)
        print("bing = ", res2)
        soup2 = bs(res2.text, 'lxml')
        img = soup2.find_all('div', {'class': 'imgpt'})
        imgres1 = []
        for result in img:
            url = result.find('a').get('href')
            src = result.find('img').get('src')
            imgres1.append((url,src))

        if misspelled:
            url = 'https://www.picsearch.com/index.cgi?q='+search
        else:
            url = 'https://www.picsearch.com/index.cgi?q='+search1
        res3 = requests.get(url)
        print("picsearch = ", res3)
        soup3 = bs(res3.text, 'lxml')

        img3 = soup3.find_all('span', {'class': 'result'})

        imgres3 = []
        for result in img3:
            url = result.find('a').get('href')
            src = result.find('img').get('src')
            imgres3.append((url,src))

        if misspelled:
            context = {
                'search1': search1,
                'search': search,
                'imgres1':imgres1,
                'imgres3' : imgres3,
            }
        else:
            context = {
                'imgres1':imgres1,
                'imgres3' : imgres3,
            }

        return render(request, 'images.html', context)
    else:
        return render(request,'images.html')
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .odds_scraper.scraper import get_match_urls, get_single_match_result
import datetime
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Creating Views Here


# Login the User View


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home_main')
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
            print("User doesn't exist")

        user = authenticate(
            request=request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("User Login")
            return redirect('home_main')
        else:
            print("INVALID PASS")
            messages.error(request, "Invalid Username or Password")

    form = CustomUserCreationForm
    context = {'form': form}
    return render(request, 'customodds/login_user.html', context=context)

# Main Home Page View


def home_page(request, url):
    context = {}
    if request.user.is_authenticated:
        dates = []
        today_date = datetime.date.today()
        for i in range(-1, 6):
            td = datetime.timedelta(i)
            date = today_date + td
            dates.append([date.strftime("%Y%m%d"),
                         str(date.day) + " " + str(date.strftime("%B"))])
        context["dates"] = dates

        return render(request, 'customodds/home_page.html', context=context)
    else:
        return redirect('login')


def home_main(request):
    context = {}
    if request.user.is_authenticated:
        dates = []
        today_date = datetime.date.today()
        for i in range(-1, 6):
            td = datetime.timedelta(i)
            date = today_date + td
            dates.append([date.strftime("%Y%m%d"),
                         str(date.day) + " " + str(date.strftime("%B"))])
        context["dates"] = dates

        return render(request, 'customodds/home_page.html', context=context)
    else:
        return redirect('login')


@csrf_exempt
def get_odds(request):
    context = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            response = json.loads(request.body)
            url = response["url"]
            odds = get_single_match_result(url)
            if odds == -1:
                return JsonResponse({"odds": ["-1"]})
            elif odds != None:
                if odds[len(odds) - 1]:
                    odds.append("red")

                else:
                    odds.append("green")
                context["odds"] = odds
                return JsonResponse({"odds": odds})
            else:
                return JsonResponse({"odds": []})


@csrf_exempt
def get_matches_urls(request):
    context = {}
    if request.user.is_authenticated:
        if request.method == "POST":
            response = json.loads(request.body)
            url = response["url"]
            urls = get_match_urls(url)
            context["urls"] = urls
            return JsonResponse(context)


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        return redirect('home_main')

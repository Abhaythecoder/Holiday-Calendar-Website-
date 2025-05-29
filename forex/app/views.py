from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import urllib.parse
import requests
from .forms import Loginform
from datetime import datetime
from .models import Login
import json


def get_holidays(request):
    # Initialize variables
    holidays = []
    error = None

    try:
        # Debug: Print the entire request GET data
        print("Request GET data:", request.GET)

        api_key = ""# put your own api key here
        date = request.GET.get('date')
        print("Date from request:", date)  # Debug print
        country = request.GET.get("country", "in")
        year = request.GET.get("year", "2025")

        # Properly formatted URL
        url = f"https://calendarific.com/api/v2/holidays?api_key={
            api_key}&country={country}&year={year}"

        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (e.g., 404)

        data = response.json()
        holidays_data = data.get('response', {}).get('holidays', [])

        if date:
            try:
                selected_date = datetime.strptime(date, '%Y-%m-%d').date()
                holidays = [
                    holiday for holiday in holidays_data
                    if datetime.strptime(holiday['date']['iso'].split("T")[0], '%Y-%m-%d').date() == selected_date
                ]
                if not holidays:
                    error = "No holidays found for the selected date."
            except ValueError as e:
                print(f"Error parsing date: {e}")  # Debug
                error = "Invalid date format."
        else:
            error = "Select a date to find the holiday"

    except requests.RequestException as e:
        error = f"Error fetching holidays: {e}"

    # Render the template with holidays or error message
    return render(request, 'holidays_list.html', {'holidays': holidays, 'error': error})


def loginView(request):
    if request.method == 'POST':
        form = Loginform(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Check if the user exists
            user = authenticate(username=username, password=password)

            if not user:  # If user doesn't exist, create a new one
                from django.contrib.auth.models import User  # Import User model
                user = User.objects.create_user(
                    username=username, password=password)
                user.save()
                print(f"New user created: {user.username}")

            # Log in the user
            login(request, user)
            return redirect('get_holidays')  # Redirect after successful login

        else:
            print("Form is invalid:", form.errors)  # Debugging

    else:
        form = Loginform()

    return render(request, 'app/login.html', {'form': form})


def loginbutton(request):
    return redirect('get_holidays')


def holi_wiki(request):
    # Get the holiday name from the request
    holiday_name = request.GET.get("holiday_name")

    if holiday_name:
        # Encode the holiday name for a valid URL
        wiki_url = f"https://en.wikipedia.org/wiki/{
            urllib.parse.quote(holiday_name)}"
        return redirect(wiki_url)  # Redirect to the Wikipedia page
    else:
        # If no holiday name is provided, redirect to a default page or show an error
        return redirect('get_holidays')  # Redirect to the holidays page

# def get_wiki(request):

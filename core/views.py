from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CustomUser  # Import your custom user model
 # Import CustomUser model

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(email=email)  # Fetch user by email
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect("login_view")

        user = authenticate(request, username=user.username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirect based on user type
            if user.user_type == "freelancer":
                return redirect("freelance_dashboard")
            elif user.user_type == "client":
                return redirect("client_dashboard")
            else:
                return redirect("home")  # Default fallback

        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "login.html")

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from .models import CustomUser  # Import the custom user model
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import CustomUser  # Import your custom user model

def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        user_type = request.GET.get("type", "freelancer")  # Default to freelancer

        # Validate passwords
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return render(request, "register.html")

        # Check if user already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered")
            return render(request, "register.html")

        # Create the user
        user = CustomUser.objects.create(
            username=email,  # Using email as username
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password1),  # Hash the password
            user_type=user_type,
        )

        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login_view")  # Redirect to login page

    return render(request, "register.html")



def account_selection(request):
    return render(request, 'account_selection.html')



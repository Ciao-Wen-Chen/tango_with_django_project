from django.urls import reverse
from unicodedata import category
from django.shortcuts import render
from django.http import HttpResponse
from rango.forms import CategoryForm, PageForm 
from rango.models import Page
from django.shortcuts import redirect

# Chapter 6
# Import the Category model and Page
from rango.models import Category
from rango.models import Page

#@ Chapter 9
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

#@ Chapter 10
from datetime import datetime

def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Chapter 6
    # order the like and retrieve top 5
    # place into context dic which will pass to template engine by render()
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    
    category_list = Category.objects.order_by('-likes')[:5] #removed - the results would be in ascending order)
    context_dict['categories'] = category_list

    page_list = Page.objects.order_by('-views')[:5] 
    context_dict['pages'] = page_list
    
    #@ Chapter 3
    #return HttpResponse("Rango says hey there partner!<br> <a href='/rango/about'>About</a>.")

    #@ Chapter 10
    visitor_cookie_handler(request)
    #context_dict['visits'] = request.session['visits']
    response = render(request, 'rango/index.html', context=context_dict)
    return response

    #@ Chapter 4 
    #return render(request, 'rango/index.html', context=context_dict)

def about(request):
    #@ Chapter 3
    #return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>.")
    #@ Chapter 4
    #return render(request, 'rango/about.html')
    #@ Chapter 8 
    print(request.method)
    print(request.user)

    #@ Chapter 10
    context_dict = {}
    if request.session.test_cookie_worked(): 
        print("TEST COOKIE WORKED!") 
        request.session.delete_test_cookie()
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    return render(request, 'rango/about.html', context=context_dict)
    

#Chapter 6
#category_name_slug, which will store the encoded category name.
#
def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context = context_dict)

@login_required
def add_category(request):
    
    # blank form for adding category
    form = CategoryForm()

    # A HTTP POST? did user submit data via the form?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

    # Have we been provided with a valid form?
    if form.is_valid():
        # Save the new category to the database. 
        cat = form.save(commit=True)
        print(cat, cat.slug)
        # Now that the category is saved, we could confirm this. 
        # # For now, just redirect the user back to the index view. 
        return redirect('/rango/')
    else:
        print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None
    
    # You cannot add a page to a Category that does not exist... DM
    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', 
                                kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)  # This could be better done; for the purposes of TwD, this is fine. DM.
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

from rango.forms import UserForm, UserProfileForm
def register(request):
    # telling the template whether the registration was successful.
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid(): 
            # Save the user's form data to the database. 
            user = user_form.save()
         
            # hash the password with the set_password method. 
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model because 
            # save the new instance in an incomplete state (the like between two model is requires)
            # would raise a referential integrity error

            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and 
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture'] 

            profile.save()
            # registration success.
            registered = True

        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal. 
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances. 
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, 'rango/register.html',
                  context = {'user_form': user_form,
                             'profile_form': profile_form,
                             'registered': registered})

#@ Chapter 9
def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information. 
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') rather than request.POST['<variable>'], 
        # because the request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>'] will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password 
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user 
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
            # If the account is valid and active, we can log the user in. # We'll send the user back to the homepage.
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
            # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in. print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
            # The request is not a HTTP POST, so display the login form.
        
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the 
        # blank dictionary object...
        return render(request, 'rango/login.html')

# The val of LOGIN_URL in setting specify the redirect url if the user didn't login
@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

# Use the login_required() decorator to ensure only those logged in can # access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('rango:index'))

#@ Chapter 10
# A helper method
def get_server_side_cookie(request, cookie, default_val=None): 
    val = request.session.get(cookie)
    if not val:
        val = default_val 
    return val

# Updated the function definition
def visitor_cookie_handler(request):

    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer. 
    # If the cookie doesn't exist, then the default value of 1 is used. 
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count 
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie 
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    request.session['visits'] = visits
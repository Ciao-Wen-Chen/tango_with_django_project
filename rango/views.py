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
    #@ Chapter 4 
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    #@ Chapter 3
    #return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>.")
    #@ Chapter 4
    #return render(request, 'rango/about.html')
    #@ Chapter 8 
    print(request.method)
    print(request.user)
    return render(request, 'rango/about.html', {})
    

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
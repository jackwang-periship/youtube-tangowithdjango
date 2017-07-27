from rango.models import Category, Course
from django.shortcuts import render
from django.core.urlresolvers import reverse
from rango.forms import CategoryForm
from rango.forms import CourseForm
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    category_list = Category.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list}
    
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'rango/index.html', context_dict)

def category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        course = Course.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['course'] = course
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)
    
def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

def add_course(request, category_name_slug):

    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            if category:
                course = form.save(commit=False)
                course.category = category
                course.views = 0
                course.save()
                return HttpResponseRedirect(
                        reverse('category', kwargs={'category_name_slug':category_name_slug}) )
        else:
            print(form.errors)
    else:
        form = CourseForm()

    context_dict = {'form':form, 'category': category}

    return render(request, 'rango/add_course.html', context_dict)    
    
def about(request):
    return HttpResponse('Rango Says: Here is the about page.<br><a href="/rango/">Back to home page</a>')


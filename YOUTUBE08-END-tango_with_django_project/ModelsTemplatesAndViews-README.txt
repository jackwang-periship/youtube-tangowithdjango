
* Steps to get the records in the database to the web pages
(Assuming you already have the model created):

(1) Update the "index" function in the application (rango)'s "views.py" module
The function will retrieve the records from database 
then pass the retrieved records to the desinated template by use a Python dictionary

(2) Update the template to use the Django template variable that was passed via "index" function.

* Add the Category page to the site:
(1) Modify the "index,html" by use the "slug" attrubute in category object the to construct a <href> 
while iterating through each object in the dictionary.
(2) While we got the <href>, the link goes nowhere.
(3) Check the error message. It is giving us the hint.
(4) Need to add a new URL switch in the "rango" application "urls.py" file.
(5) Here it is:

url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),)  # New!

Please note the "(?P<category_name_slug>[\w\-]+)". This is a Python regular expression.
It says: only accept a string that contains a-zA-Z, 0-9. Once it passed validation
then assign it to "category_name_slug". The state also says: call views.category with
the varable "category_name_slug" as the parameter.

(6) With the "switch" statement in place, we need to add a function "category".
This is to tell URL switch what function to call when the link is clicked.


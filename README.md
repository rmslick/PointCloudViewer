# Sandbox testing:

### Project overview

Open source web-based, 3D modelling platform.

### Web stack overview
1) Front-end: For the front-end development, you are using HTML, CSS, and JavaScript. HTML provides the structure and content of your web pages, CSS is used for styling and layout, and JavaScript adds interactivity and dynamic behavior to your application.

2) Bootstrap: You have integrated Bootstrap into your project. Bootstrap is a popular front-end framework that provides pre-built CSS styles and JavaScript components. It helps you create responsive and visually appealing web pages with ease.

3) Three.js: You are using Three.js, a JavaScript library, for 3D rendering in the browser. Three.js abstracts away many complexities of WebGL, allowing you to create and manipulate 3D scenes, render 3D objects, and apply materials and lighting.

4) Django: Django is a high-level Python web framework that follows the Model-View-Controller (MVC) architectural pattern. It provides a set of tools and features for building web applications efficiently. In your project, Django is used for handling HTTP requests, managing URLs, rendering templates, and processing data.

5) Python: Python is the programming language used for developing the server-side logic of your web application. Django is built on top of Python and provides a clean and efficient way to write server-side code. You use Python to define views, models, and perform data processing tasks.

6) Open3D: Open3D is a library for 3D data processing and visualization. It provides functionalities to work with point clouds, meshes, and other 3D data formats. In your application, you utilize Open3D to process and visualize the uploaded point cloud data.

7) RESTful API: You have implemented a RESTful API using Django. This API endpoint allows you to send point cloud data to the server using POST requests. The server processes the data and returns a response. This API can be used to interact with your application programmatically or integrate it with other systems.

8) Overall, your web stack consists of a combination of front-end technologies (HTML, CSS, JavaScript, Bootstrap, Three.js) and back-end technologies (Django, Python, Open3D). This stack enables you to create a web application that can render and interact with 3D point cloud data in the browser, process the data on the server, and provide a user-friendly interface.

#### Django:
- Django : Django provides a framework for handling HTTP requests, managing URLs, rendering templates, and processing data. It helps you build web applications in a structured and efficient manner, handling many common web development tasks out of the box.

Django is being used in your app so far:

1) Project Structure: Your Django project consists of multiple components, including the main project directory and the pcdprocessor app.

2) URL Configuration: In the project's urls.py file, you've defined URL patterns and associated them with corresponding views. These patterns determine how incoming requests are handled and which views are called.

3) Views: In the views.py file within the pcdprocessor app, you've defined several view functions that handle specific URL patterns. These views receive HTTP requests, process the data, and generate responses.

4) Templates: You've used Django templates to generate HTML content dynamically. Templates allow you to separate the presentation logic from the Python code in your views, making it easier to create dynamic web pages.

5) Static Files: Static files, such as CSS and JavaScript files, are stored in the static directory within the app. These files are served directly by Django and can be included in your HTML templates.

6) File Upload: You've implemented a file upload feature using Django's FileField in the models.py file. This allows users to upload point cloud files, which are then processed by your view function.

7) RESTful API: You've created an endpoint in the views.py file that accepts POST requests with JSON data. This endpoint receives the uploaded point cloud data and processes it.

8) CSRF Protection: Django's CSRF protection is enabled by default, which helps prevent Cross-Site Request Forgery attacks. However, you encountered a CSRF verification error when making POST requests from your JavaScript code. To address this, you added the {% csrf_token %} template tag to include the CSRF token in your HTML form.

Integrating Bootstrap: You've integrated Bootstrap into your app by including the Bootstrap CSS and JavaScript files in your HTML templates. This allows you to utilize Bootstrap's styling and components.

#### Render a web page:

1) Add a view method to render page:
```python
# Example
def index(request):
    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key
    if session_id not in global_session_dict.keys():
        s = Scene(session_id)
        add_scene_info(session_id,s)
        print("New user: ",session_id)
    else:
        print("Welcome back user: ",session_id)
    current_scene = get_scene_info(session_id)
    return render(request, 'index.html')
```
2) Add the url path for this view in  sandbox_testing/urls.py

```python
from .views import robcd 
urlpatterns = [
    path('pcdprocessor/', include('pcdprocessor.urls')),
    path('rob/', rob, name='rob'),
]
```
3) Add the url path for this view in  pcdproccessor/urls.py

```python
from pcdprocessor.views import rob
urlpatterns = [
    path('pcdprocessor/', include('pcdprocessor.urls')),
    path('rob/', rob, name='rob'),
]
```
### Add an endpoint

1. First, make sure you have Django installed. You can install it using pip:

```
pip install django
```

2. Create a new Django project:

```
django-admin startproject myproject
```

This will create a new directory called `myproject` with the following structure:

```
myproject/
    manage.py
    myproject/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

3. Create a new Django app:

```
cd myproject
python manage.py startapp myapp
```

This will create a new directory called `myapp` inside the `myproject` directory.

4. Open `myproject/settings.py` and add `'myapp'` to the `INSTALLED_APPS` list:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # add your app here
    'myapp',
]
```

5. Open `myproject/urls.py` and add a new route to your app:

```python
from django.urls import path, include

urlpatterns = [
    path('myapp/', include('myapp.urls')),
]
```

6. Create a new file called `myapp/views.py` with the following content:

```python
from django.http import JsonResponse

def hello(request):
    return JsonResponse({'message': 'Hello, World!'})
```

This defines a view function that returns a JSON response with a "Hello, World!" message.

7. Create a new file called `myapp/urls.py` with the following content:

```python
from django.urls import path

from . import views

urlpatterns = [
    path('hello/', views.hello),
]
```

This defines a new route for your app that maps to the `hello` view.

8. Run the development server:

```
python manage.py runserver
```

This will start the development server on `http://localhost:8000/`.

9. Test your API:

Open your browser and go to `http://localhost:8000/myapp/hello/`. You should see a JSON response with a "Hello, World!" message.

For the sandbox, you could use something like the Python `exec` function to execute the user's code in a sandboxed environment. However, this can be dangerous if you don't properly restrict the user's access to system resources. There are also existing libraries like `PySandbox` and `PyExecJS` that can help you create a safe sandbox environment for running untrusted code.

### To run:
```bash
cd /home/rmslick/PointCloudBrowser/sandbox_testing 


#start the sandbox server
python manage.py runserver
```

```bash
# open terminal and run
curl --header "Content-Type: application/json"   --request POST   http://localhost:8000/api/sandbox/ --data '{"script":"print()"}'
```

# Sandbox client side:
- MonacoEditorPython.html
- MonacoEditorPythonSyntax.html : Better syntax highlighting
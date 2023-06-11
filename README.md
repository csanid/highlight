# Highlight
#### Video Demo:  <Agregar URL>
#### Description:
Highlight is a single-page note-taking app for readings built with Django. It allows users to create an account with an username and a password. Once the user is logged in, they can add a new note through a form where they must fill in the title of the note and its content. Optionally, users can also fill in four other fields useful for those who may wish to store more specific information on their readings: author, title of the book, publisher and year. The main page of Highlight shows all of the notes saved by the user currently logged in. The notes can be edited or deleted, and the user can also search through the notes. Finally, the user can access their account settings in order to change their password or delete their account along with all of their notes from the database. 

##### **First steps**

The back-end of my project is built with Django. I chose this framework instead of Flask mainly because I wanted to challenge myself to learn to work with a more complex and widely used framework for Python. I found Django to be relatively easy to pick up after the experience with Flask provided by CS50x. Brian's lectures in CS50's Introduction to Web Programming were also incredibly helpful and instructive. 

I worked on the project locally with Visual Studio Code and WSL on a Windows computer. After setting up a virtual environment and activating it, I downloaded Python and Django inside the environment and created the project. I also used git to keep track of the changes made and pushed the commits to a private repository in my GitHub account. The files included in ``.gitignore`` are ignored by git. 

##### **Models and forms**
In the file ``models.py``, I created the database model for the notes taking advantage of Django's ORM (Object-relational mapping) in order to set up and interact with a SQL database with techniques and syntax derived from object-oriented programming. The class ``Note`` inherits from Django's custom class ``models`` and includes the ``user_id`` as a foreign key also associated to a related name, ``notes``, which will be useful later for displaying the notes saved by the current user. If the user is deleted from the database, all the notes having their id as a foreign key will also be deleted. The other fields in the model are for the title, author, book title, publisher, year, content and timestamp. By default there is also an ``id`` field for each note as a primary key handled by Django. 

The ``title`` and ``content`` fields are mandatory, the fields corresponding to ``id``, ``user_id`` and ``timestamp`` are completed by Django requiring no extra action from the user, and the rest of the fields can be left blank by the user. The timestamp is included so that the notes can be ordered on the main page according to the date and time they were added. The ``content`` field has a maximum length of 8500 characters. Finally, there is also a string method defined for the class so that the notes can be viewed in the admin in a more semantic way than the default one. 

At this point, I debated myself between creating a single database with a column for user id or creating a database for each user. After some research, I found out that I should go for the first alternative, as it would quickly become highly inefficient to have to create a separate database for each user. 

In ``forms.py``, I created the forms for the app making use of the classes, methods and other tools provided by Django. The class ``RegisterForm`` inherits from ``UserCreationForm`` and the model for this class is Django's default ``User`` model. The class ``LoginForm`` inherits from Django's ``forms`` class and defines two fields, ``username`` and ``password``. The class ``CustomPasswordChangeForm`` inherits from ``PasswordChangeForm`` and includes a customized validation method that checks if the two fields for the new password match, and then if the new password is different from the old password. If any of these conditions is not met, then a validation error is shown to the user. I added this custom validation because the default Django form didn't check if the new password matched the old one and instead, when this was the case, proceeded to validate the update even if no change had actually been made. 

The class ``NoteForm`` creates a form based on the model ``Note`` that will be used for adding, viewing and editing the notes. In the widgets, the fields ``title`` and ``content`` are set to show an error message if they are empty when form is submitted, so as to offer front-end validation. Additionally the ``textarea`` element for the ``content`` field is initially set to a size of three rows. Finally, I defined a ``clean`` method for the class in order to perform server-side validation for the form as well.    

##### **Views**
In ``views.py``, the logic of the app and its different functionalities are defined. Each of the views corresponds to a url specified in ``urls.py``, as is required by Django.

The ``index`` view first checks if there is no user logged in and, in that case, redirects to the ``login`` view. If a user is currently logged in, the ``index.html`` template is rendered. Provided as context are an instance of ``NoteForm`` (which will be visible in a modal) and a QuerySet object containing all the notes added by the current user ordered according to their timestamp, newest first. To create the QuerySet, I made use of the related name defined in the model. The template ``index.html`` will show a grid of cards representing all the notes saved by the user. Each card shows the title of the note and the first four lines of the content.

The ``register`` view renders the ``register.html`` template with an instance of ``RegisterForm`` if the request method is ``get``. If the request method is ``post``, the view first checks if the data provided in the form is valid. In that case, it proceeds to add the username and password to the database with the logic provided by Django, logs the user in and redirects to the ``index`` view. If the form isn't valid, the view renders the ``register.html`` template again so as to show the custom error messages defined by Django. Thus the function provides server-side validation. 

The ``login_view`` view works in a similar way. If the request method is ``get``, it renders the ``login.html`` template with an instance of ``LoginForm`` as context. If the method is ``post``, the function checks if the form is valid. If it is and if the credentials correspond to a registered user, they are logged in and redirected to the ``index`` view. Otherwise, the ``login.html`` template is rendered showing an error message. 

The ``logout_view`` logs the user out with the default method provided by Django and redirects to the ``login`` view. 

The ``settings`` view renders the ``settings.html`` template.

The ``change_password`` view renders the ``password_update.html`` template if the request method is ``get``. If the method is ``post``, the view checks if the data submitted via the form is valid and, in that case, proceeds to save the new password to the database. If the form isn't valid, the form is shown again with the error messages defined in ``forms.py``.

The ``delete_account`` view deletes the user from the database and redirects them to the ``login`` view showing a success message that informs that the account has been deleted. 

The ``add`` view first checks if the data submitted through the instance of ``NoteForm`` is valid. If it is, the note is saved to the database and the view returns a ``JsonResponse`` with a dictionary containing the key-value pair ``"success": True``. If the form isn't valid, the view will return a ``JsonResponse`` with the ``success`` key set to ``False`` and another key, ``errors``, listing the form errors. This ``JsonResponse`` will be handled with a JavaScript function that hides the modal and redirects to ``index.html`` if the value received was ``"success": True``, and keeps the modal open and shows the validation errors if the ``JsonResponse`` is ``"success": False``. This JavaScript function was necessary to avoid the closing of the modal once the submit button is clicked when there are validation errors. This way, server-side validation is ensured if browser validation were to fail.

The ``edit`` view takes as arguments the request and the ``note_id`` corresponding to the card the user clicked on on the main page of the app. It first retrieves from the database the note identified with the ``note_id`` provided as argument, so that it will be possible to update that record with the data submitted via the form. If the form is valid, the update is saved to the database. The function returns, just like the ``add`` view, a ``JsonResponse`` indicating if the form was validated or not. The JSON response will be handled by the same JavaScript function explained in the previous paragraph: the modal will hide if the data submitted was OK, or otherwise will remain open showing the errors. 

The ``delete`` view also takes a ``note_id`` as argument in order to delete from the database the note that corresponds to the card the user clicked on.

The ``search`` view retrieves from the form the search term provided by the user and queries the records of the notes saved by them to check if that term is present in any of the fields. If there are notes where that term appears, they will be added to a QuerySet object that will be returned to the ``index.html`` template so that they can be displayed to the user. Otherwise, the QuerySet will be empty and a message will be shown indicating that there are no results.

Finally, the ``get_note`` view handles the API request made when the user clicks on a card to view the whole contents of the note or to edit it. The ``note_id`` that this view takes as argument is used to retrieve the data associated to that note from the database. The view then proceeds to create with that data a set of key-value pairs that is returned as a ``JsonResponse`` and will be handled by a JavaScript function that populates the form with the data received. 

##### **Interaction with database**
One of the most challenging problems I had to solve while working on the app was the communication between the database and the front-end. I had to write some JavaScript functions and create an API endpoint so that, when the user clicks on a card displayed on the main page of the app, the modal would open up and the form be populated with the data from the corresponding note. The form modal for viewing the complete content of the notes and for editing them is the same used for adding a new note. 
To achieve this, an anonymous JavaScript function written in the file ``highlight.js`` listens for any click made on a card shown on the main page. The function then opens up the modal and saves in a variable the id stored in the dataset of the card. It finally calls the ``get_note`` function with the value saved in ``note_id`` as parameter. 

The ``get_note`` function in ``highlight.js`` makes an API request to an endpoint that will retrieve the content of the note taking that id as parameter as I explained above on the paragraph about the ``get_note`` view. 


##### **User interface** 
Justificar fields específicos: the notes to serve as well as bibliographic records. 

Reconocer que se podría haber incorporado framework de front-end 

Hablar de los templates: describe the app from the point of view of the user experience 

CSS
Favicon

##### **Additional comments**

Your README.md file should be minimally multiple paragraphs in length, and should explain what your project is, what each of the files you wrote for the project contains and does, and if you debated certain design choices, explaining why you made them. 
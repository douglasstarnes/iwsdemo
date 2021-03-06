## *While the following instructions still apply, Cloud9 is no longer free.  But you can run the application locally assuming you have Pyhton 3.4x available and the permissions to install packages.*
The application can be run on the Cloud9 IDE which is an easy way to view the code running in a development environment.

 1. Go to http://c9.io and sign in with your Github account (or BitBucket)
 2. Create a new public, Python workspace.  For demo purposes I'll call mine, `iwsdemo`.
 3. Clone the repo using HTTPS: `git clone https://github.com/douglasstarnes/iwsdemo.git`
 4. In the terminal, create a new environment variable for the database URI in the development config: `export DEVDB=sqlite:///data.db`
 5. Create a new Python 3 virtual environment: ``mkvirtualenv --python=`which python3` iwsdemo``
 6. Change to the `iwsdemo` repo directory: `cd iwsdemo`
 7. Install the dependencies with `pip install -r requirements.txt`
 8. Run the script to create the database: `python manage.py reset_database` (answer 'y' to the prompt)
 9. Run the script to create the sample data: `python manage.py populate_database`
 10. Start the development server: `python manage.py runserver -p 8080 -h 0.0.0.0` (Cloud 9 will map internal port 8080 to 80 on the public URL in the next step)
 11. The application is now accessible at  `http://{workspacename}-{username}.c9users.io`.  The workspace and user names can be found in the URL for the workspace.  For mine the URL is: `https://ide.c9.io/douglasstarnes/iwsdemo` My user name is `douglasstarnes` and my workspace name is `iwsdemo` so the public URL is `http://iwsdemo-douglasstarnes.c9users.io`.
 
The application itself is using Flask and Python 3.4.x.  A number of extensions are used such a Flask-Security, Flask-SQLAlchemy, Flask-RESTful and Flask-Script.  JavaScript with Angular JS, and Angular UI provide some interactivity.  The UI is styled with BootStrap. It can be easily cloned into any Linux environment and use one of the databases supported by SQLAlchemy (the configuration here uses SQLite for development and MySQL for production).

A walkthrough of the application follows:

There are two types of users, admins and developers.  Admins create feature request tickets and assign them to developers (or themselves).  The application has an admin and two developers already:

 * **Email**: admin@example.com **Password**: adminP@55word
 * **Email**: developer1@example.com **Password**: P@55word
 * **Email**: developer2@example.com **Password**: P@55word

The admin will have a link to the admin dashboard, where users and tickets can be managed.  The email address for a user is their login and must be unique.  Also, a random password can be generated or provided and confirmed.  Manage users will show a list of the users in the system and a link to access the details where the active state can be toggled and the roles (admin) can be changed.

New tickets can be created by the admin.  The date picker on the new ticket page is from Angular UI.  Also, tickets have a priority.  By default, a new ticket is given lowest priority for the client is it associated with, but checking the top of queue checkbox will place it at the highest priority for that client.  The manage tickets link goes to a page powered by a small API that can be dynamically filtered by client using the drop down box.  Notice that tickets which are overdue have their date in bold red text.  A link for the ticket will show the ticket details.  Comments can be added to a ticket.  Only admins and the developer assigned to the ticket can comment.  Also, admin can edit a ticket.  All fields can be edited except the priority and the client.  Editing the client could lead to priority conflicts so instead the ticket can be deleted.  The modal dialog is also from Angular UI.  When a ticket is deleted, all comments associated with it are deleted and any tickets for the client with lower priority are moved up by one.

Developers can view the tickets assigned to them which are grouped by client and ordered by priority.  The overdue tickets' dates are in bold red text.  On the ticket details page, there is a button that represents the stages of a theoretical workflow.  When the admin creates a ticket, it is in the `Open` state.  The developer then accepts the ticket, begins works on it which puts it in the `In Progress` state and when it is finished puts it in the `Completed` state.  Each state change is reflected in a comment for the ticket.

A management script (`manage.py`) is to manage the database from the command line.  
There are 3 commands to work with the DB:
 1. `reset_database` drops all the tables and creates them again
 2. `populate_database` creates the clients and product areas and some sample users and tickets  
 3. `create_user` will create a specific user.  There is also a built in command to start the development server  

There are also two configurations in `config.py` that handle which database is used (the connection strings are stored in environment variables for security and flexibility) and turn debugging off in production.



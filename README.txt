Team Member Management Application
====================================

Overview:
---------
This is a simple team member management application built using Django and Django REST Framework on the backend, and a Single Page Application (SPA) built with Vue.js on the frontend. The application allows users to view, add, edit, and delete team members. Additional features include:
- A dynamic header that displays the current count of team members.
- A search box to filter team members by name.
- User notifications for successful or failed actions.
- A confirmation dialog before deleting a team member.

Project Structure:
------------------
team_member_management/       # Django project root
├── manage.py                 # Django management script
├── team_member_management/   # Django project settings & configuration
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── members/                  # Django app for team member management
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py              # Model registration for admin interface
│   ├── apps.py
│   ├── models.py             # TeamMember model
│   ├── serializers.py        # DRF serializers
│   ├── views.py              # API viewset
│   ├── urls.py               # API endpoint routes
│   └── tests.py              # Automated tests
├── templates/
│   └── index.html            # Frontend SPA built with Vue.js, HTML, and CSS
├── static/                   # Static files (if needed)
├── README.txt                # Project documentation (this file)
└── TESTING.txt               # Instructions for testing the application
└── requirements.txt          # Denotes the required dependencies

Setup Instructions:
-------------------
1. **Clone the Repository:**
git clone <repository_url> cd team_member_management

2. **Create a Virtual Environment:**
python3 -m venv env source env/bin/activate # On Windows: env\Scripts\activate

3. **Install required dependencies**
Then run:
pip install -r requirements.txt

4. **Apply Migrations:**
python manage.py migrate

5. **Run the Development Server:**
python manage.py runserver
Then open your web browser and navigate to: http://127.0.0.1:8000/

6. **Admin Access (Optional):**
To use the Django admin panel, create a superuser:
python manage.py createsuperuser

markdown
Copy
And visit: http://127.0.0.1:8000/admin/

Testing:
--------
Please refer to the `TESTING.txt` file for detailed instructions on testing this application.

Additional Notes:
-----------------
- The API endpoints are available at `/members/api/team-members/`.
- The frontend SPA is built using Vue.js (included via CDN) and communicates with the API using JavaScript’s fetch API.
- User experience has been enhanced with inline search, confirmation dialogs, and notifications.
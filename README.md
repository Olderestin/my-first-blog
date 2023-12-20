# Django Blog Application

This project represents a web application for managing a blog. It allows users to register and perform CRUD operations (Create, Read, Update, Delete) on blog posts, enabling the attachment of up to four images per post via an intuitive web interface.

## Technical Tasks

- Implemented a user registration and authentication system using email.
- Developed the ability for users to upload multiple images.
- Implemented search and pagination functionality.
- Created API endpoints using DRF.
- Built a Dockerfile and docker-compose file to package the project.
- Added Redis for caching and Celery for background tasks.
- Created an email sending task using Celery.

___

## Technologies Used

### Backend
- Python
- Django
- Django REST Framework
- Celery

### Frontend
- HTML
- CSS
- Bootstrap

### Databases and Infrastructure
- PostgreSQL
- Docker
- Redis
___
## Installation

To run this project locally, follow these steps:

1. Download [Docker](https://www.docker.com/get-started).

2. Clone the repository:
   ```bash
   git clone https://github.com/Olderestin/my-first-blog.git

3. Navigate to the project directory:
   ```bash
   cd my-first-blog

4. Create a .env file based on the provided example:
   ```bash
   cp .env.example .env

5. Start the application with Docker:
   ```bash
   docker compose up

6. Access the application in your web browser at http://127.0.0.1:8000

7. Perform database migrations:
   ```bash
   docker exec -it django python manage.py migrate

8. Create a superuser:  
   ```bash
   docker exec -it django python manage.py createsuperuser

9. Setting up Google authentication for the admin panel ([Exapmle video on youtube](https://youtu.be/Gk9tsLHMMsM?t=423)):
   - Go to Google Developers Console
   - Create a project and configure the "OAuth consent screen" by adding necessary scopes
   - Create OAuth 2.0 credentials for a web application, specifying authorized redirect URIs
   - In Django's admin panel:
      - Add a "Site" via /admin/sites/site/
        - Domain name: your local domain
        - Display name: Your site name
      - Add a "Social Application" via /admin/socialaccount/socialapp/:
        - Provider: Google
        - Name: Your application name
        - Use the Client ID and Secret Key from your Google OAuth credentials
        - Select the site you created

These steps will guide you through setting up the application locally, performing necessary configurations, and accessing it in your web browser.
___

## Unfinished Tasks

- [ ] Add API for social authentication.
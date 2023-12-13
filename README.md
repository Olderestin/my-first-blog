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

3. Start the application with Docker:
   ```bash
   docker compose up

4. Access the application in your web browser at http://127.0.0.1:8000

___

## Unfinished Tasks

- [ ] Create API for comments.
- [ ] Implement user avatar changing functionality.
- [ ] Add API for social authentication.
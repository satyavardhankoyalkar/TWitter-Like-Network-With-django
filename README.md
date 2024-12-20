Social Network - Project Overview
This project implements a basic social network platform where users can create posts, follow other users, and "like" posts. The web application is built using Python (Django) for the backend, JavaScript for the frontend, and HTML/CSS for the user interface.

Features
1. New Post
Description: Users who are signed in can create new posts by typing text into a text area and submitting it.
Implementation: The "New Post" feature appears at the top of the "All Posts" page. Alternatively, this can be a separate page dedicated to posting.
2. All Posts
Description: Displays all posts from all users, sorted by the most recent posts first.
Implementation: Each post includes:
Username of the poster.
Content of the post.
Date and time of the post.
Number of "likes" (initially set to 0 for all posts).
3. Profile Page
Description: Clicking on a username will load the user's profile page, which includes:
Number of followers and people followed.
A list of all the user’s posts in reverse chronological order.
A "Follow" or "Unfollow" button for other users (not applicable to the current user).
A user cannot follow themselves.
4. Following Page
Description: Users can view posts made by users they follow on a separate page.
Implementation: The "Following" link in the navigation bar takes the user to a page where they can see posts from only the users they follow. This page functions like the "All Posts" page but with a limited set of posts.
Access: Available only to signed-in users.
5. Pagination
Description: For any page displaying posts, only 10 posts will be shown per page. A "Next" button will allow users to navigate to older posts, while a "Previous" button allows navigation to earlier posts.
Implementation: If there are more than 10 posts, the pagination system will be activated.
6. Edit Post
Description: Users can edit their posts by clicking the "Edit" button on their posts.
Implementation: The post content will be replaced with a text area allowing the user to make changes. The post can be saved without reloading the page, using JavaScript.
Security: Only the owner of the post can edit it. Users cannot edit posts created by others.
7. Like and Unlike Posts
Description: Users can "like" or "unlike" any post.
Implementation: The like count will be updated asynchronously using JavaScript without requiring a page reload. Clicking the "like" button will toggle the like status.
Technology Stack
Backend: Python (Django)
Frontend: JavaScript, HTML, CSS
Database: SQLite (or your preferred database)
Setup and Installation
Prerequisites
Python 3.x
Django (install via pip install django)
Installation
Clone the repository:
bash
Copy code
git clone https://github.com/USERNAME/repository-name.git
Navigate into the project directory:
bash
Copy code
cd repository-name
Install the dependencies:
bash
Copy code
pip install -r requirements.txt
Apply database migrations:
bash
Copy code
python manage.py migrate
Create a superuser to access the admin interface:
bash
Copy code
python manage.py createsuperuser
Run the development server:
bash
Copy code
python manage.py runserver
Accessing the Application
Open your browser and visit http://127.0.0.1:8000/ to interact with the social network.
Testing the Features
Ensure that all features work as expected:
Users can create, edit, and delete posts.
Users can follow/unfollow others and see posts from those they follow.
Pagination and like/unlike functionality should work without page reloads.
Security Considerations
The application ensures that users can only edit their own posts.
Data is handled securely by Django's built-in authentication system.
Conclusion
This project provides a simple yet functional social network where users can interact with posts, follow others, and engage in basic social interactions. The use of Django for the backend and JavaScript for frontend interactivity makes it a modern web application.

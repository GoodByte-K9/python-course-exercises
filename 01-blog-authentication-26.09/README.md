## Simple Blog With Authentication

What I worked with:
- Flask
- WTForms
- Flask Login
- SQLAlchemy
- Werkzeug Security

For this exercise I created registration and login forms, hashing the password with scrypt and storing it (along with other user data) in an SQLite database. I also made an `admin_only` decorator to guard admin-only features, like creating new blog posts or deleting existing ones. Non-admin registered users can only make comments under each blog post. Creating the comments functionality required linking tables together in the database so the right comments appeared under the right posts.

Admin status is assigned simplistically, meaning the first two registered users will become admins. The rest will be regular users.

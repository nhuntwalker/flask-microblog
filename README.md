# Flask Microblog

This is my run through Miguel Grinberg's existing [Flask MegaTutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) (before he updates to the next iteration of it).
The goal here is to learn about the workings of Flask enough to write good flask apps.

## Progress

I'll update as I work through each section of the megatutorial.

- [x] Hello World
- [x] Templating
- [x] Web Forms
- [x] Database
- [x] User Logins
- [x] Profile Page and Avatars
- [x] Unit Testing
- [x] Followers, Contacts, and Friends
- [x] Pagination
- [ ] Full Text Search -- Not doing
- [ ] Email Support -- Not doing
- [ ] Facelift -- Nope
- [ ] Dates and Times -- Not important
- [ ] I18n and L10n -- Nope
- [ ] Ajax
- [ ] Debugging, Testing, and Profiling -- Nah
- [ ] Deployment on Linux -- Nah
- [ ] Deployment on Heroku -- Nah

## Alterations 

- Instead of using OpenID like the tutorial, I'm using a simple User model through  Flask SQLAlchemy
- Instead of using sqlite as my database, I'm using a PostgreSQL database, with configuration set up in my environment.
- Added Python 3.6 type annotations.
- Using a dictionary for view context instead of explicit keyword arguments
- I didn't really feel like using Gravatar for images so the users have no images on them. Tough.
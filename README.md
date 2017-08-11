# Flask Microblog

This is my run through Miguel Grinberg's existing [Flask MegaTutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) (before he updates to the next iteration of it).
The goal here is to learn about the workings of Flask enough to write good flask apps.

## Progress

I'll update as I work through each section of the megatutorial.

- [x] Hello World
- [x] Templating
- [x] Web Forms
- [x] Database
- [ ] User Logins
- [ ] Profile Page and Avatars
- [x] Unit Testing
- [ ] Followers, Contacts, and Friends
- [ ] Pagination
- [ ] Full Text Search
- [ ] Email Support
- [ ] Facelift
- [ ] Dates and Times
- [ ] I18n and L10n
- [ ] Ajax
- [ ] Debugging, Testing, and Profiling
- [ ] Deployment on Linux
- [ ] Deployment on Heroku

## Alterations 

- Instead of using OpenID like the tutorial, I'm using a simple User model through  Flask SQLAlchemy
- Instead of using sqlite as my database, I'm using a PostgreSQL database, with configuration set up in my environment.

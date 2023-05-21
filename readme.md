# FlaskForum
For school I made a simple forum web app with a group, at the end we had a functional product but I'd like to redo it and focus on implementing more features, and having a more thoughtfully designed back end.
There wasn't anything inherently wrong with ours, but I want to be more idiomatic in my approach to the RESTful design, and to do it from the ground up myself (without a deadline) so I can take as much time on the various parts as I'd like.

Besides that I also want to use Flask concepts like the application factory, and have the components be more modular instead of a monolithic `app.py`. I'll be starting off by following the flask tutorial and then building more features from there.

## Goals (in vague descending order of importance, bold are main, italics are maybe)
- **Posts**
  - **Title/body**
  - Like/Dislikes
  - Can tap a post to make it take up the full view 
    - Comments/replies
  - Public or private
  - Markdown support (probably reduced, just headers italics and bold)
  - *Image support*
- **Users**
  - **Have/make posts**
    - *Anonymous user posts*
  - **Follow/Unfollow mechanism**
  - **Profiles**
    - **List of their posts**
    - **Bios**
    - Public or private
  - *Profile pictures*
- **Global feed of (public) posts**
- **User feed of posts from users they follow**
- *User-User messaging*

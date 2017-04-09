# Pitchy

[Pitchy](https://www.getpitchy.com/) is my capstone project for [Ada Developers Academy](http://adadevelopersacademy.org/). It's a social networking site for public relations professionals and journalists. The project was driven by equal parts of wanting to tackle a problem from my past career and of wanting to explore internet protocols.

## Background
Before Ada, I worked in crisis communications/public relations. Finding the right journalists to connect with and communicating effectively with them wasn't as easy as it should be. Journalists' inboxes were always full but I knew they wanted my emails because I represented a large tech company. Plus, the email I used for talking to my clients was the same email I used to talking to journalists. Accidentally sending something to journalists that you meant to send to clients is always a fear and does happen. So, I decided to create Pitchy to mediate these issues. 

## Functionalities
Users have all the normal "friending" options (request friend, confirm/reject friend request, remove friend), can find new connections via recommendations based on their focus(es), and can message their friends in real-time (uses websockets).  

Since everything happens behind the login, here are some small clips of a few functionalities.  

#### Messaging
![](https://media.giphy.com/media/IwpbEVjdFK012/giphy.gif)  

#### Unfriending
![](https://media.giphy.com/media/CzHqDjcpQnvDG/giphy.gif)  

#### Friending
![](https://media.giphy.com/media/dnuF1RqvSMPSw/giphy.gif)  

*Feel free to sign up on the site with fake info if you want to check it out further*

## Tech Stack
* **Languages** - Python, Javascript
* **Framework** - Django
* **Libraries** - Django Channels, Django Storages
* **Databases** - PostgreSQL, Redis (caching layer)
* **Infrastructure** - Heroku, AWS S3

## Notes
I also gained experience in:  
* **API creation** - I used Django REST Framework to produce an API that ultimately was not utilized (but is still in codebase for reference)
* **AWS deployment** - Initially I deployed the project via AWS EB but support for websockets was more complex compared to support via Heroku.
* **Working with new tech** - Django Channels (brings async tasks to Django, aka websocket support) released the same month I worked on this project, so it forced me to look outside my usual approach of tutorials/Stack Overflow for answers.

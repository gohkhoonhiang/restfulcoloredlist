### Table of Contents

* [Introduction](#introduction)
* [Redesign](#redesign)
  * [Page Flow Redesign](#page-flow-redesign)

# Introduction

This tutorial is an extension of my previous [tutorial](https://github.com/gohkhoonhiang/coloredlist) on learning Tornado framework.

I have wanted to refactor the previous code base to make it more RESTful, but in the process of doing so, I found that it was actually pretty difficult and complicated to refactor the code. The difficulty is mostly due to lack of planning upfront and also because I have picked up some new knowledge along the way which makes the existing structure quite incompatible for a change.

As such, I have decided to start an entirely new repo. This time, I will try to plan more deliberately and keep in mind the practices of REST, so that I can write a more RESTful app this time.

I'm glad I started the previous tutorial, because it lead me to discover more about how most web apps out there write in RESTful style, so that I can apply what I have learnt in this new tutorial. Given that I have just started learning the concepts, I'm sure this tutorial will again be full of incorrect practices. As with the previous tutorial, I will discover such errors along the way, and will surely rewrite and rewrite and rewrite again and again and again.

With that said, you will probably find that I will make references to the previous tutorial. If you are unsure, you can always refer back to the previous tutorial and read the history of it to get a clearer picture of the story.

I hope you will enjoy this tutorial as much as the previous one. Again, feel free to file issues regarding the tutorial or the code itself. Thank you!

[Back to top](#table-of-contents)

# Redesign

I didn't really talk much about the design process in the previous tutorial, because frankly, there wasn't any. I was just taking literally everything out of the [reference](https://css-tricks.com/app-from-scratch-1-design/), including the template structure and CSS. Because of this, I didn't really put any thought into designing the page flow, user experience and client-server interaction.

[Back to top](#table-of-contents)

## Page Flow Redesign

Let's talk about the UI/UX design seriously now. In our Colored List App, there are only a few things that the user will need: a page to login, a page to see all items and perform CRUD actions, a page to change profile, and a page for new user to create an account. That will be a total of 4 pages.

```
if logged in:                                            if not logged in:
|------------------------|                               |------------------------|
|                        |           logout              |                        |<--\
|  [          ] / -      |         ------------->        |  [username]            |    \
|  [          ] / -      |                               |  [password]            |     \ error
|  [          ] / -      |         <-------------        |  [Submit]              |     /
|                        |              ok               |                        |    /
|  [          ] +        |                               |  [error message]       |---/
|                        | <---\                         |                        |
|------------------------|      \                        |------------------------|
list.html                        \                       login.html
     |        / \                 \                            |       / \
     |         |                   \                           |        |
     |         |                    \                          |        |
     | view    | view                \                         | signup | login
     | account | list                 \ ok                     |        |
     |         |                       \                       |        |
     |         |                        \                      |        |
    \ /        |                         \                    \ /       |
|------------------------|                \              |------------------------|
|                        |<--\             \             |                        |<--\
|  [username]            |    \             \            |  [username]            |    \
|  [password]            |     \ ok/error    \           |  [password]            |     \ error
|  [confirmpassword]     |     /              \          |  [confirmpassword]     |     /
|  [Submit]              |    /                \         |  [Submit]              |    /
|                        |---/                  \        |                        |---/
|  [error message]       |                       \       |  [error message]       |
|                        |                        \------|                        |
|------------------------|                               |------------------------|
account.html                                             account_new.html
```

**Legends:**
* `/` in `list.html` page indicates an `edit` button.
* `-` in `list.html` page indicates a `delete` button.
* `+` in `list.html` page indicates an `add` button.

I hope you can understand the diagram drawn with pure ASCII characters above. Basically, it's a page flow diagram showing how the various pages in the app interact.

1. When the user hits `/`, if he is logged in, then the `list.html` is rendered with all the existing items and a `Add New Item` form displayed. Otherwise, he is redirected to `login.html` to login with his username and password.
2. If the login is unsuccessful, an error message will be displayed. After which, the user may go to the `account_new.html` to sign up for an account.
3. If the login is successful, the user will see the `list.html` page.
4. From `list.html`, the user can go to `account.html` to view his profile and make changes to his passwords.
5. If the password update is successful, he will remain on the same page with no error message. Otherwise, an error message will be displayed below the form.
6. From the `account.html` page, the user can navigate back to the `list.html`.
7. If a new user signs up for an account successfully, he is immediately redirected to the `list.html` with an empty list where he can start adding new items. Otherwise, he will remain on the `account_new.html` with an error message displayed.
8. From the `account_new.html` page, the user may suddenly remember his login credentials and can navigate back to `login.html` page to perform login.

[Back to top](#table-of-contents)


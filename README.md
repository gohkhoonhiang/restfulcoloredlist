### Table of Contents

* [Introduction](#introduction)
* [Redesign](#redesign)
  * [Page Flow Redesign](#page-flow-redesign)
* [RESTful Services](#restful-services)
  * [Rewriting URI Endpoints](#rewriting-uri-endpoints)
  * [Rewriting Request Handlers](#rewriting-request-handlers)
  * [Separating UI and APIs](#separating-ui-and-apis)

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

# RESTful Services

Notice that in the previous tutorial, I have used the term `REST` in sections that concern getting a JSON response from the server. Upon reading more about what RESTfulness actually is, it's obvious that the app we have built so far does not comply with REST guidelines. There are few things we did that have violated the rules:

### No Verbs in Resource URI

Having a URI like `/list/create` is a no-no. The URI should describe what resource will be involved, and the action for each resource should be defined in each HTTP verb such as `GET`, `POST`, `PUT` and `DELETE`. A good design of a URI for our case will be `/items/{id}`, where `id` is the identifier of the single resource in the collection, and each HTTP verb will corresponding to getting a list of items, creating a new item in the list, updating an item and deleting and item. 

### Use Plural Nouns

Instead of using singular noun, it is better and simpler to use a standardized plural form for all resources name. For our list page, the actual resources requested are the list items, instead of the lists, so instead of using `/list`, it is clearer to use `/items`. And don't use collection nouns like `/itemList` or `/itemSet`.

### Separate URIs for Views

Since everything returned by the server is a resource, an HTML template that is returned is also considered a resource, so we should have a proper URI structure for that as well. Instead of the current `/list`, which should be reserved for returning list data, we will use `/p/list` instead, where `p` is shorthand for `pages`.

[Back to top](#table-of-contents)

## Rewriting URI Endpoints

Now that we are clear of RESTful API style, we should redesign our own APIs to make them more RESTful.

Let's start with listing down all available resources from our server.

1. Pages
2. List Items
3. User Profile (although we have yet to implement the User Account page, we are expected to have the user data as one available resource)

Now, we will define just one URI for each resource, because every operation on the resource should be defined by the HTTP verb.

### Pages

```
/p/{page_name}
```

For example:

```
/p/account`
```

### List Items

```
/items/{item_id}
```

For example:

```
/items/5745b7feaeca1313f23acb44
```

### User Profile

```
/accounts/{user_id}
```

For example:

```
/accounts/572cbfceaeca133de672b178
```

Even though there are mainly 4 HTTP verbs that the client can use for each type of resource, we may not necessarily have to grant them all the actions. For example, we will not allow users to "deregister" themselves directly from the client-side, so we should block the `DELETE` request on `/users/{user_id}`. To do so, we just simply do not override the `delete()` method in our request handler.

### URLs Redesigned

Let's rewrite our `urls.py` to define the necessary resource URIs.

```
url_patterns = [
    url(r"/", MainHandler, dict(db=db)),
    url(r"/items/([0-9a-zA-Z\-]+)", ListItemHandler, dict(db=db)),
    url(r"/items", ListItemListHandler, dict(db=db)),
    url(r"/p/items", ListItemPageHandler, dict(db=db)),
    url(r"/login", LoginHandler, dict(db=db)),
    url(r"/p/login", LoginPageHandler, dict(db=db)),
    url(r"/logout", LogoutHandler, dict(db=db)),
    url(r"/accounts/([0-9a-zA-Z\-]+)", AccountHandler, dict(db=db)),
    url(r"/accounts", AccountListHandler, dict(db=db)),
    url(r"/p/account/create", AccountCreatePageHandler, dict(db=db)),
    url(r"/p/account/view", AccountViewPageHandler, dict(db=db)),
]
```

Let's discuss the design of the URLs we have just defined.

For each type of resources, we have 2 versions of the URIs: one with a regex suffix, another without. For example, we have `/items/([0-9a-zA-Z]+)` and `/items`. The first URI is used for a single resource request, and the latter is used for collection resource request. When the client requires a single item, it will call `/items/{item_id}` with `GET` method, then the endpoint should respond with a single `item` data. On the other hand, when the client requires a list of items, it will call `/items` with `GET` method, and the endpoint will respond with a list of `item`s data. Additionally, if the client wants to create a new resource in the `item` collection, it will call `/items` with `POST` method, together with the new `item` data as request body. This is in line with the RESTful design guideline.

Besides the resource URIs, we also need to define the page URIs. To display the list of `item`s, we provide the `/p/items` URI for the client to request, then the endpoint will render the `items.html` template accordingly.

[Back to top](#table-of-contents)

## Rewriting Request Handlers

When we redesigned the URL patterns, we also introduced a few new request handlers. Here is the complete list of handlers in the new design:

* MainHandler (GET)
* ListItemHandler (GET, PUT, DELETE)
* ListItemListHandler (GET, POST)
* ListItemPageHandler (GET)
* LoginHandler (POST)
* LoginPageHandler (GET)
* LogoutHandler (POST)
* AccountHandler (GET, PUT, DELETE)
* AccountListHandler (GET, POST)
* AccountCreatePageHandler (GET)
* AccountViewPageHandler (GET)

For each of the request handlers, we have indicated the methods that we will implement. The client may only make a request via these methods to each of the URI, accordingly.

[Back to top](#table-of-contents)

## Separating UI and APIs

[Back to top](#table-of-contents)



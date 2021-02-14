# Social Network
Simple REST API for StarNavi test task. Created with Django.


# Installation
Download the repository with `git clone`:
```console
$ git clone https://github.com/tcysin/test-task-starnavi
```

Then, navigate inside the fetched `test-task-starnavi/` folder and run `pip install -r requirements.txt` to take care of dependencides:
```console
$ cd test-task-starnavi
$ pip install -r requirements.txt
```

Apply database migrations:
```console
$ python3 manage.py migrate
```

Run the tests with `python3 manage.py test` to make sure everything is working:
```console
$ python3 manage.py test
```


## API endpoints

### Authentication and registration
- `api/auth/registration/` handles registration of new users and accepts **POST** requests with the following fields
    - `username`
    - `password1` -- must be 8+ characters and lowercase and uppercase
    - `password2` -- must be the same as `password1`
    - `email` (optional) -- valid email address
- `api/auth/login/` handles login and token generation & assignment. Accepts **POST** requests with the following fields and returns a *token* if credentials match those in the database
    - `username`
    - `password`
    - `email` (optional)
- `api/auth/logout/` -- accepts **POST** request, removes client's token.

Authentication is *token-based*, meaning that users must include their token in the `Authorization` HTTP header. The key should be prefixed by the string literal "Token", with whitespace separating the two strings. For example, like so
```http
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Posts
- `api/posts/` handles listing of posts and their creation.
    - **GET** returns JSON response with a list of all posts, where each element has the following fields: `'id', 'author', 'title', 'body', 'created', 'users_who_liked'`.
    - **POST** request with supplied `title` field and `body` fields creates a new post and returns it back.
- `api/posts/<id>/` handles listing and editing of a particular instance of a post.
    - **GET** returns detailed information about a post. Same fields as in `api/posts/` GET request.
    - **PUT** updates the `title` and/or `body` of a post.
    - **DELETE** deletes a post.
- `api/posts/<id>/like/` adds a user who made **POST** request to the set of users who liked the given post.
- `api/posts/<id>/unlike/` removes a user who made **POST** request from the set of users who liked the given post.
- `api/analytics/` handles **GET** requests and returns the count of likes generated between given `start_date` and `end_date`, grouped by the date of generation. Specifically, returns a collection of `date: likes_count` elements. Requires following arguments to GET request:
    - `start_date` -- date in ISO format, must be before `end_date`
    - `end_date` -- date in ISO format


# Notes

## Models
- I implement **likes** functionality via `ManyToMany` relationship between users 
and posts through `Like` model. This takes care of liking functionality by tracking who liked what and restricting users to only one like per post.

## Permissions
- Only authenticated users are allowed to create new posts, like/unlike existing ones and check analytics.
- Only the author of a post is allowed to edit or delete it.

# Social Network
Simple REST API for StarNavi task.

# Quickstart

## Installation
Download the repository with `git clone https://github.com/tcysin/test-task-starnavi`. Then, navigate inside the `test-task-starnavi` folder and run `pip3 install -r requirements.txt` to take care of dependencides.

## API endpoints

### Authentication and registration
- `api/auth/registration/` handles registration of new users and accepts **POST** requests with the following keyword arguments
    - `username`
    - `password1` -- must be 8+ digits and contain lowercase and uppercase chars
    - `password2` -- must be the same as `password1`
    - `email` (optional)
- `api/auth/login/` handles login and token generation and assignment. Accepts **POST** requests with the following parameters and returns a **token** if credentials match those in the database
    - `username`
    - `password`
    - `email` (optional)
- `api/auth/logout/` -- **POST** requests

Authentication is *token-based*, meaning that users must include their token in the `Authorization` HTTP header. The key should be prefixed by the string literal "Token", with whitespace separating the two strings. For example, like so
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Posts
- `api/posts/` handles listing of *Post* and their creation.
    - **GET** returns JSON response with a list of all posts, where each has the fields `'id', 'author', 'title', 'body', 'created', 'users_who_liked'`.
    - **POST** requires the field `title`. Optional field is `body`. Creates a new post.
- `api/posts/<id>/` handles listing and editing of a particular instance of a *Post*.
    - **GET** returns detailed information about a particular *Post*. Same fields as in `api/posts/` GET request.
    - **PUT** updates the `title` and/or `body` of a *Post*.
    - **DELETE** deletes a post.
- `api/posts/<id>/like/` adds a user who made **POST** request to the set of users who liked the *Post*.
- `api/posts/<id>/unlike/` removes a user who made **POST** request from the set of users who liked the *Post*.
- `api/analytics/` handles **GET** requests and returns the count of likes generated between given `start_date` and `end_date`, grouped by the date of generation. Requires following arguments to GET request:
    - `start_date` -- date in ISO format, must be before `end_date`
    - `end_date` -- date in ISO format


# Notes

## Models
- I implement **likes** functionality via `ManyToMany` relationship between users 
and posts through `Like` model. This takes care of liking functionality by tracking who liked what and restricting users to only one like per post.

## Permissions
- Only authenticated users are allowed to create new posts, like/unlike existing ones and check analytics.
- Only the author of a post is allowed to edit or delete it.
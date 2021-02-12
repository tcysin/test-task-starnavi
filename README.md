# Social Network
Simple REST API for StarNavi task.

# Quickstart
**TODO**

# Notes

## Models
- I implement **likes** functionality via `ManyToMany` relationship between users 
and posts. This allows to keep track of who already liked the post.

## Permissions
- Only authenticated users are allowed to create new posts and like existing ones.
- Only the author of a post is allowed to edit or delete it.

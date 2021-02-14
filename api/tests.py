from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Post, User

# TODO: running tests takes too much time - around 3 seconds


class PostListTests(APITestCase):
    """Tests for `/api/posts/` endpoint.

    Test listing via GET request and post creation via POST request.
    Everyone may view the posts but only authenticated users can create new
    ones.
    """

    def setUp(self):
        """Populate the database with some data."""

        # users
        spam = User.objects.create_user('spam', 'spam@gmail.com', 'spam-pass')
        eggs = User.objects.create_user('eggs', 'eggs@gmail.com', 'eggs-pass')

        # posts
        post1 = Post.objects.create(author=spam, title='ZZZ', body='we sleep')
        post2 = Post.objects.create(author=eggs, title='TEST POST', body='hey')

    def test_list_all(self):
        """Ensure we get a valid list of all posts."""

        url = reverse('all')
        response = self.client.get(url)

        self.assertEqual(len(response.data), 2)
        # make sure response contains both post titles
        self.assertContains(response, 'ZZZ')
        self.assertContains(response, 'TEST POST')

    def test_create_anonymous(self):
        """Ensure anonymous users cannot create new posts."""

        url = reverse('all')
        data_in = {'title': 'spam', 'body': 'ham-ham-ham'}
        response = self.client.post(url, data_in)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_authenticated(self):
        """Check that authenticated users can create new posts."""

        url = reverse('all')
        # setp up authenticated access
        user = User.objects.get(username='spam')
        client = APIClient()
        client.force_authenticate(user=user)

        # create a new post
        data = {'title': 'new post', 'body': 'lets go'}
        response = client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)
        self.assertEqual(Post.objects.latest('created').title, 'new post')


class PostDetailTests(APITestCase):
    """Tests for `/api/posts/<pk>/` post instances."""

    def setUp(self):
        """Populate the database with some data."""

        # users
        spam = User.objects.create_user('spam', 'spam@gmail.com', 'spam-pass')
        eggs = User.objects.create_user('eggs', 'eggs@gmail.com', 'eggs-pass')

        # posts
        post1 = Post.objects.create(author=spam, title='ZZZ', body='we sleep')
        post2 = Post.objects.create(author=eggs, title='TEST POST', body='hey')

    def test_detail(self):
        """Ensure we get a valid details of a post."""

        post = Post.objects.get(title='ZZZ')
        url = reverse('detail', args=(post.pk,))
        response = self.client.get(url)
        data = response.data

        self.assertEqual(data['id'], post.pk)
        self.assertEqual(data['title'], post.title)
        self.assertEqual(data['body'], post.body)

    # TODO
    def test_update_anonymous(self):
        pass

    # TODO
    def test_update_other(self):
        pass

    # TODO
    def test_update_author(self):
        pass

    def test_delete_anonymous(self):
        """Ensure anonymous users cannot delete a post."""

        post = Post.objects.get(title='ZZZ')
        url = reverse('detail', args=(post.pk,))
        response = self.client.delete(url)  # anonymous client

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_other(self):
        """Ensure other authenticated users cannot delete a post."""

        # post by user=spam
        post = Post.objects.get(title='ZZZ')
        url = reverse('detail', args=(post.pk,))
        # set up credentials for user=eggs
        user = User.objects.get(username='eggs')
        client = APIClient()
        client.force_authenticate(user=user)
        # try deletion
        response = client.delete(url)  # user=eggs

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_author(self):
        """Ensure only authenticated author of a post can delete it."""

        # post by user=spam
        post = Post.objects.get(title='ZZZ')
        url = reverse('detail', args=(post.pk,))
        # set up credentials for user=spam
        user = User.objects.get(username='spam')
        client = APIClient()
        client.force_authenticate(user=user)
        # delete a post
        response = client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)

# TODO: /auth/ tests

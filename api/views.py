from datetime import date

from django.http import Http404
from django.db.models import Count
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics

from .models import Post, Like
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    """List all posts, or create a new post.

    Only authenticated users are able to create a post.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Associate owner with the created post."""
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a post instance.

    Only authenticated authors are able to update or delete their post.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like(request, pk):
    """Add a user to those who liked the post.

    Only authenticated users are able to like a post.
    """

    if request.method == 'POST':
        # query the post in question
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # add a user to the list of those who liked this post
        # won't duplicate the relationship
        post.users_who_liked.add(request.user)

        return Response({'message': f'Liked the post {pk}.'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike(request, pk):
    """Remove a user from those who liked the post.

    Only authenticated users are able to unlike a post.
    """

    if request.method == 'POST':
        # query the post in question
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # add a user to the list of those who liked this post
        # won't duplicate the relationship
        post.users_who_liked.remove(request.user)

        return Response({f'message': f'Unliked the post {pk}.'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def analytics(request):
    """Return count of likes aggregated by day from start to end dates."""

    # extract and clean start/end dates from GET request kwargs
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    # validation
    try:
        start_date = date.fromisoformat(start_date)
        end_date = date.fromisoformat(end_date)
    except:
        return Response(
            {'message':
                'Invalid start/end dates. Make sure to follow ISO format.'},
            status=status.HTTP_400_BAD_REQUEST)
    if not (start_date <= end_date):
        return Response(
            {'message': 'start_date must precede end_date.'},
            status=status.HTTP_400_BAD_REQUEST)

    # query the data, group by date liked and return the counts
    in_range = Like.objects.filter(date_liked__range=(start_date, end_date))
    in_range = in_range.values('date_liked')
    qs = in_range.annotate(count=Count('date_liked'))
    data = {
        D['date_liked'].isoformat(): D['count']
        for D in qs
    }

    return Response(data)

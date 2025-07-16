# main/views_api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Property, Favorite, Review, Category, Inquiry
from .serializers import PropertySerializer, ReviewSerializer, CategorySerializer, FavoriteSerializer, InquirySerializer

class PropertyListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        qs = Property.objects.filter(is_approved=True)
        if category := request.GET.get('category'):
            qs = qs.filter(category_id=category)
        serializer = PropertySerializer(qs, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PropertyDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request, pk):
        prop = get_object_or_404(Property, id=pk)
        return Response(PropertySerializer(prop).data)
    
    def put(self, request, pk):
        prop = get_object_or_404(Property, id=pk, owner=request.user)
        serializer = PropertySerializer(prop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        prop = get_object_or_404(Property, id=pk, owner=request.user)
        serializer = PropertySerializer(prop, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        prop = get_object_or_404(Property, id=pk, owner=request.user)
        prop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FavoriteToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, property_id):
        prop = get_object_or_404(Property, id=property_id)
        fav, created = Favorite.objects.get_or_create(user=request.user, property=prop)
        if not created:
            fav.delete()
            return Response({'message': 'Removed'}, status=status.HTTP_200_OK)
        return Response({'message': 'Added'}, status=status.HTTP_201_CREATED)

class FavoriteListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        favs = Favorite.objects.filter(user=request.user)
        serializer = FavoriteSerializer(favs, many=True)
        return Response(serializer.data)

class AddOrUpdateReviewAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, property_id):
        prop = get_object_or_404(Property, id=property_id)
        review, created = Review.objects.get_or_create(property=prop, user=request.user, defaults={'rating': request.data.get('rating'), 'comment': request.data.get('comment')})
        if not created:
            review.rating = request.data.get('rating', review.rating)
            review.comment = request.data.get('comment', review.comment)
            review.save()
        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class DeleteReviewAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, property_id):
        prop = get_object_or_404(Property, id=property_id)
        Review.objects.filter(property=prop, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

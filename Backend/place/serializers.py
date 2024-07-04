from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Review, Place, WomenOnlyPlace, Scrap


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class WomenOnlyPlaceSerializer(ModelSerializer):
    class Meta:
        model = WomenOnlyPlace
        fields = '__all__'

class PlaceSerializer(ModelSerializer):
    average_review_rate = serializers.FloatField(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True, source='review_set')
    women_only_category = WomenOnlyPlaceSerializer(many=True, read_only=True, source='women_only_places')

    class Meta:
        model = Place
        fields = '__all__'

class ScrapSerializer(ModelSerializer):
    class Meta:
        model = Scrap
        fields = '__all__'


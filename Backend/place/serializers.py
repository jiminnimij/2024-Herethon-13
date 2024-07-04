from rest_framework.serializers import ModelSerializer
from .models import Review, Place, WomenOnlyPlace


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class WomenOnlyPlaceSerializer(ModelSerializer):
    class Meta:
        model = WomenOnlyPlace
        fields = '__all__'

class PlaceSerializer(ModelSerializer):
    # review_rate_average 
    reviews = ReviewSerializer(many=True, read_only=True, source='review_set')
    women_only_category = WomenOnlyPlaceSerializer(many=True, read_only=True, source='women_only_places')

    class Meta:
        model = Place
        fields = '__all__'




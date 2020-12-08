from rest_framework.serializers import ModelSerializer
from .models import Post
from accounts.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        depth = 1
        fields = '__all__'
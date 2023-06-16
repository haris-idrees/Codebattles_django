from .models import User, Admin, Post,Problems,Results
from rest_framework import serializers

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id','email','password']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'age', 'email', 'contact', 'user_type', 'password', 'country',
                  'date_of_joining', 'description','profile_picture','cover_photo',
                  'requests_sent_to_groups', 'pending_requests_to_groups',
                  'approved_requests']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','user_id','post_text','post_image','num_of_likes','num_of_dislikes','date_added',
                  'user_img','user_name']

class ProblemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problems
        fields = '__all__'

class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = '__all__'
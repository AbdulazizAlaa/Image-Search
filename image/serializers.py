from image.models import Image, Tag, TagText, TagUsername
from User.serializers import UserTagSerializer, UserLoginSerializer, UsernameTagSerializer
# from django.contrib.auth.models import Image
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User


class TagSerializer(serializers.ModelSerializer):

    tag = serializers.CharField()

    class Meta:
        model = Tag
        # Input to the tag serializer
        fields = ['tag']


class ImageRetrieveSerializer(serializers.ModelSerializer):#test
    # image = serializers.CharField()
    #id = serializers.IntegerField()
    # Parameter many was used to serialize a list instead of 1 string
    Tags = TagSerializer(required=True, many=True)
    # image_url = serializers.SerializerMethodField('get_image_url')
    # image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Image
        # The input to the ImageRetrieveSerializer
        # This should include the input to the TagSerializer
        fields = ('__all__')


class ImageUploadSerializer(serializers.ModelSerializer):#test

    # tag = TagSerializer(many = True, read_only=True)#ques
    # image_url = serializers.SerializerMethodField('get_image_url')
    image = serializers.ImageField(max_length=None, use_url=True)
    uploaded_by = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="username")

    class Meta:
        model = Image
        fields = ('__all__')

    # def get_image_url(aself, obj):
    #   return obj.image.url


# class TagListSerializer(serializers.ListSerializer):
#     def create(self, validated_data):
#         tags = [TagText(**item) for item in validated_data]
#         # print tags
#         return TagText.objects.bulk_create(tags)


class TagTextSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=True)
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="username")
    image = serializers.CharField(source='image_id')

    class Meta:
        model = TagText
        # list_serializer_class = TagListSerializer
        fields = ('__all__')

    # def create(self, validated_data):
    #     tag_data = []
    #     print validated_data
    #     # for i in validated_data['tag']:
    #     #     print i
    #     #     tag_data.append(i)
    #     # print tag_data
    #     print validated_data['tag']
    #     tag_data = validated_data['tag']
    #     tag = Tag.objects.get_or_create(tag=tag_data)
    #     validated_data.pop('tag')
    #     print validated_data
    #     TagText.objects.create(tag=tag, **validated_data)
    #     print "done"
    #     return tag


class TagUsernameSerializer(serializers.ModelSerializer):
    tag = UsernameTagSerializer(read_only=True)
    user = serializers.CharField(source='user_username')
    image = serializers.CharField(source='image_id')

    class Meta:
        model = TagUsername
        fields = ('tag', 'user', 'image')

    def create(self, validated_data):
        # tag_username = super(serializers.ModelSerializer, self).create(validated_data=validated_data)
        # print tag_username
        print validated_data['tag']
        for i in validated_data['tag']:
            user = User.objects.get(username=i['username'])
            tag_username.tag.add(user)
        return tag_username
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
    #     # tag_username = super(serializers.ModelSerializer, self).create(validated_data)
    #     # print tag_username
    #     print validated_data
    #     image = Image.objects.get(id=validated_data['image_id'])
    #     t = TagUsername.objects.create(image=image, user=validated_data['user'])
    #     for tag in validated_data['tag']:
    #         try:
    #             print tag['tag']
    #             tag = Tag.objects.get(tag=tag['tag'])
    #             print tag
    #             t.tag.add(tag)
    #         except User.DoesNotExist:
    #             print "exception"
    #             pass
    #     return t


class TagUsernameSerializer(serializers.ModelSerializer):
    tag = UsernameTagSerializer(many=True)
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="username")
    image = serializers.CharField(source='image_id')

    class Meta:
        model = TagUsername
        fields = ('tag', 'user', 'image')

    def create(self, validated_data):
        # tag_username = super(serializers.ModelSerializer, self).create(validated_data)
        # print tag_username
        tag_username = []
        print validated_data
        image = Image.objects.get(id=validated_data['image_id'])
        t = TagUsername.objects.create(image=image, user=validated_data['user'])
        for tag in validated_data['tag']:
            try:
                print tag['username']
                user = User.objects.get(username=tag['username'])
                print user
                t.tag.add(user)
                # tag_username.append(t)
            except User.DoesNotExist:
                print "exception"
                pass
        return t
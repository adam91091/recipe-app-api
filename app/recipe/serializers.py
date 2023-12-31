"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import (
    Tag,
    Recipe,
    Ingredient,
)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags',
                  'ingredients']
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed."""
        auth_user = self.context['request'].user
        for tag in tags:
            # create tag if does not exist, or take existing
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                # instead of name=tag['name'], use kwargs to secure
                # this code from update
                # if more fields would be added in tag in the future
                **tag,
            )
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self, ingredients, recipe):
        """Handle getting or creating tags as needed."""
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            # create tag if does not exist, or take existing
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user,
                # instead of name=tag['name'], use kwargs to secure
                # this code from update
                # if more fields would be added in tag in the future
                **ingredient,
            )
            recipe.ingredients.add(ingredient_obj)

    # provide custom logic to make writable nested serializer
    def create(self, validated_data):
        """Create a recipe."""
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])

        # remove tag from validated data - recipe cannot get it
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        """Update recipe."""
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        # we want to allow tags can be empty list
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerialzer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']


# create separate serializer for recipe uploading image, because
# we want to upload only image in the action
# Best practice is - upload only one type of data to an API.
# better to provide specific API for handling image upload
class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipes."""

    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}

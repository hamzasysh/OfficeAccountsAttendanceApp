from rest_framework import serializers
from .models import Accounts

class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Accounts model.

    Attributes:
        model (Accounts): The model associated with this serializer.
        fields (str): The fields to include in the serialized representation. 
                      In this case, '__all__' means include all fields from the model.

    Example:
        An instance of this serializer can be used to convert an Accounts model instance
        into JSON format for API responses, and vice versa.

    Note:
        This serializer inherits from the ModelSerializer provided by Django Rest Framework,
        which simplifies the process of creating serializers for Django models.

    See Also:
        - Django Rest Framework ModelSerializer:
          https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
    """

    class Meta:
        """
        Meta class for AccountSerializer.

        Attributes:
            model (Accounts): The model associated with this serializer.
            fields (str): The fields to include in the serialized representation.
        """
        model = Accounts
        fields = '__all__'

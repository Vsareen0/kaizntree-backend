from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import GetItemSerializer, AddItemSerializer, CategorySerializer, TagSerializer, DateRangeSerializer
from .models import Item, Category, Tags
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .utils import (
    get_headers, 
    get_create_category_request_body,
    get_create_category_response,
    get_items_response,
    get_create_item_request_body,
    get_create_item_response,
    get_create_tag_request_body,
    get_create_tag_response
)


@swagger_auto_schema(
    method='post',
    manual_parameters=get_headers(),
    request_body=get_create_category_request_body(),
    responses=get_create_category_response()
)
@api_view(['POST'])
def create_category(request):
    """
    API endpoint to create a category.

    Parameters:
        - name (string): The name of category.
    Returns:
        - 201 Created: Item created successfully.
        - 400 Bad Request: Invalid data provided/Some error occured.
    """
    try:
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.create(request.data)
            return Response({ 'data': serializer.data }, status=status.HTTP_200_OK)
        else:
            return Response({ 
                'message': 'Unable to create category', 
                'error': serializer.errors 
            }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as ex:
        template = "Create category: An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        
        return Response({ 
            'message': 'Something went wrong !'
        }, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(
    method='get',
    manual_parameters=get_headers(),
    responses=get_items_response()
)
@api_view(['GET'])
def get_items(request):
    """
    API endpoint to get paginated items.

    Parameters:
     - start_date (date): Start date of the date range.
     - end_date (date): End date of the date range.
     - search (str): Optional. Search term to filter items by name or SKU.

    Returns:
    - 200: Item fetched successfully.
    - 400 Bad Request: Invalid data provided/Some error occured.
    
    - count (number): Total items in inventory.
    - next(link): The url for next page.
    - prev(link): The url for previous page.

    An Array of results with below attributes.
    - sku (string).
    - name (string): The name of item.
    - category (string): The category item belongs to.
    - tags (array number): Tags associated with this item.
    - in_stock (number)
    - available_stock (number)
    """
    try:
        paginator = PageNumberPagination()
        paginator.page_size = 10 

        # Get query parameters for search terms
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        search_term = request.GET.get('search')
        user_id = request.jwt_payload['user_id']

        if start_date and end_date:
            date_range_serializer = DateRangeSerializer(data={'start_date': start_date, 'end_date': end_date})
            date_range_serializer.is_valid(raise_exception=True)

            # Filter items by date range
            items = Item.objects.filter(created_at__range=[start_date, end_date])


        # Filter items by name or SKU if search term is provided
        if search_term:
            items = Item.objects.filter(Q(name__icontains=search_term) | Q(sku__icontains=search_term))
        else:
            items = Item.objects.all()
        
        if user_id:
            items = items.filter(user_id=user_id)
        
        result_page = paginator.paginate_queryset(items, request)
        serializer = GetItemSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    
    except Exception as ex:
        template = "Get Items: An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

        return Response({ 'message': 'Unable to get items' }, status=status.HTTP_400_BAD_REQUEST)




@swagger_auto_schema(
    method='post',
    manual_parameters=get_headers(),
    request_body=get_create_item_request_body(),
    responses=get_create_item_response()
)
@api_view(['POST'])
def create_item(request):
    """
    API endpoint to create a new item.

    Parameters:
        - sku (string).
        - name (string): The name of item.
        - category (string): The category item belongs to.
        - tags (array number): Tags associated with this item.
        - in_stock (number)
        - available_stock (number)
    Returns:
        - 201 Created: Item created successfully.
        - 400 Bad Request: Invalid data provided/Some error occured.
    """
    try:
        data = request.data
        data['user'] = request.jwt_payload['user_id']
        print('user id: ', data['user_id'], ' ', request.jwt_payload['user_id'])
        serializer = AddItemSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({ 'data': serializer.data }, status=status.HTTP_200_OK)
        else:
            return Response({ 
                'message': 'Unable to create item', 
                'error': serializer.errors 
            }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as ex:
        template = "Create category: An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

        print("Request data:", request.data)
        print("Serialized data:", serializer.data)

        return Response({ 'message': 'Something went wrong !' }, status=status.HTTP_400_BAD_REQUEST)

    

@swagger_auto_schema(
    method='post',
    manual_parameters=get_headers(),
    request_body=get_create_tag_request_body(),
    responses=get_create_tag_response()
)
@api_view(['POST'])
def create_tag(request):
    """
    API endpoint to create a new tag.

    Parameters:
        - name (string): The name of tag.
        - img (string): The source of image.
    Returns:
        - 201 Created: tag created successfully.
        - 400 Bad Request: Invalid data provided/Some error occured.
    """
    try:
        serializer = TagSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({ 'data': serializer.data }, status=status.HTTP_200_OK)
        else:
            return Response({ 
                'message': 'Unable to create tag', 
                'error': serializer.errors 
            }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as ex:
        template = "Create tag: An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

        print("Request data:", request.data)
        print("Serialized data:", serializer.data)

        return Response({ 'message': 'Something went wrong !' }, status=status.HTTP_400_BAD_REQUEST)




@swagger_auto_schema(
    method='get',
    manual_parameters=get_headers(),
)
@api_view(['GET'])
def get_category(request):
    """
    API endpoint to get all category.

    Parameters:
     
    Returns:
    - 200: Category fetched.
    - 400 Bad Request: Invalid data provided/Some error occured.
    

    An Array of results with below attributes.
    - id (number): The id of category.
    - name (string): The name of category .
    """
    try:
        paginator = PageNumberPagination()
        categories = Category.objects.all()
        paginator.page_size = categories.count() 
        
        result_page = paginator.paginate_queryset(categories, request)
        serializer = CategorySerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    
    except Exception as ex:
        template = "Get Items: An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

        return Response({ 'message': 'Unable to get category' }, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(
    method='get',
    manual_parameters=get_headers(),
)
@api_view(['GET'])
def get_tags(request):
    """
    API endpoint to get all tags.

    Parameters:
     
    Returns:
    - 200: Tags fetched.
    - 400 Bad Request: Invalid data provided/Some error occured.
    

    An Array of results with below attributes.
    - id (number): The id of tag.
    - name (string): The name of tag.
    - img (string): The img of tag.
    """
    try:
        paginator = PageNumberPagination()
        tags = Tags.objects.all()
        paginator.page_size = tags.count() 
        
        result_page = paginator.paginate_queryset(tags, request)
        serializer = TagSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    
    except Exception as ex:
        template = "Get Items: An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

        return Response({ 'message': 'Unable to get tags' }, status=status.HTTP_400_BAD_REQUEST)


from drf_yasg import openapi


def get_headers():
    return [openapi.Parameter('token', openapi.IN_HEADER, description="JWT token", type=openapi.TYPE_STRING)]


def get_create_category_request_body():
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['name']
    )


def get_create_category_response():
    return {
        "200": openapi.Response(
            description="200 description",
            examples={
                "application/json": {
                    "data": {
                        "name": "test cat"
                    }
                }
            }
        ),
        "400": openapi.Response(
            description="400 description",
            examples={
                "application/json": {
                    "message": "Something went wrong !"
                }
            }
        ),
    } 


def get_items_response():
    return {
        "200": openapi.Response(
            description="200 description",
            examples={
                "application/json": {
                    "count": 20,
                    "next": "http://localhost:8000/api/inventory/list?page=2",
                    "previous": "null",
                    "results": [
                        {
                        "id": 1,
                        "sku": "ETSY-FOREST",
                        "name": "Etsy Bundle Pack",
                        "in_stock": 100,
                        "available_stock": 88,
                        "tags": [],
                        "category": {
                            "id": 1,
                            "name": "Bundles"
                        }
                        }
                    ]
                }
            }
        ),
        "400": openapi.Response(
            description="400 description",
            examples={
                "application/json": {
                    "message": "Something went wrong !"
                }
            }
        ),
    }


def get_create_item_request_body():
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'sku': openapi.Schema(type=openapi.TYPE_STRING),
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'category': openapi.Schema(type=openapi.TYPE_NUMBER),
            'tags': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_NUMBER)),
            'in_stock': openapi.Schema(type=openapi.TYPE_NUMBER),
            'available_stock': openapi.Schema(type=openapi.TYPE_NUMBER),
        },
        required=['sku', 'name', 'category', 'tags', 'in_stock', 'available_stock']
    )


def get_create_item_response():
    return {
        "200": openapi.Response(
            description="200 description",
            examples={
                "application/json": {
                    "data": {
                        "id": 21,
                        "sku": "TEST-5",
                        "name": "Test 5",
                        "in_stock": 0,
                        "available_stock": 0,
                        "tags": [ 1, 3 ],
                        "category": 1
                    }
                }
            }
        ),
        "400": openapi.Response(
            description="400 description",
            examples={
                "application/json": {
                    "message": "Something went wrong !"
                }
            }
        ),
    }


def get_create_tag_request_body():
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'img': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['name', 'img']
    )


def get_create_tag_response():
    return {
        "200": openapi.Response(
            description="200 description",
            examples={
                "application/json": {
                    "data": {
                        "id": 4,
                        "name": "Sample tag",
                        "img": "https://upload.wikimedia.org/wikipedia/en/thumb/9/9f/Xero_software_logo.svg/1200px-Xero_software_logo.svg.png"
                    }
                }
            }
        ),
        "400": openapi.Response(
            description="400 description",
            examples={
                "application/json": {
                    "message": "Something went wrong !"
                }
            }
        ),
    }
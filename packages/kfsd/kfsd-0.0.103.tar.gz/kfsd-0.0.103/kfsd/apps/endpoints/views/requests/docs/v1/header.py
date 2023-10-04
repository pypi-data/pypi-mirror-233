from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class HeaderV1Doc:
    @staticmethod
    def modelviewset_list_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.QUERY,
                name="page",
                required=False,
                type=OpenApiTypes.INT,
                examples=[
                    OpenApiExample("Example 1", summary="Pagination", value=1),
                    OpenApiExample("Example 2", summary="Pagination", value=2),
                ],
            )
        ]

    @staticmethod
    def modelviewset_list_examples():
        return [
            OpenApiExample(
                "Header - List All",
                value=[
                    {
                        "identifier": "ENDPOINT=Postmark,METHOD=POST,HEADER=Accept",
                        "endpoint": "ENDPOINT=Postmark,METHOD=POST",
                        "key": "Accept",
                        "value": "application/json",
                        "description": "",
                    }
                ],
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_get_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "Header - Get",
                        summary="Header Identifier",
                        description="Header - Get",
                        value="ENDPOINT=Postmark,METHOD=POST,HEADER=Accept",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "Header - Get",
                value={
                    "identifier": "ENDPOINT=Postmark,METHOD=POST,HEADER=Accept",
                    "endpoint": "ENDPOINT=Postmark,METHOD=POST",
                    "key": "Accept",
                    "value": "application/json",
                    "description": "",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "Header - Create",
                value={
                    "endpoint": "ENDPOINT=Postmark,METHOD=POST",
                    "key": "Accept",
                    "value": "application/json",
                    "description": "",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Header - Create",
                value={
                    "identifier": "ENDPOINT=Postmark,METHOD=POST,HEADER=Accept",
                    "endpoint": "ENDPOINT=Postmark,METHOD=POST",
                    "key": "Accept",
                    "value": "application/json",
                    "description": "",
                },
                request_only=False,
                response_only=True,
            ),
        ]

    @staticmethod
    def modelviewset_delete_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "Header - Delete",
                        summary="Header Identifier",
                        description="Header - Delete",
                        value="ENDPOINT=Postmark,METHOD=POST,HEADER=Accept",
                    )
                ],
            )
        ]

    @staticmethod
    def exec_view_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "Header - Exec",
                        summary="Header Identifier",
                        description="Header - Exec",
                        value="ENDPOINT=Postmark,METHOD=POST,HEADER=Accept",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "Header - Patch",
                        summary="Header Identifier",
                        description="Header - Patch",
                        value="ENDPOINT=Postmark,METHOD=POST,HEADER=Accept",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "Header - Patch",
                value={
                    "value": "application/json",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "Header - Patch",
                value={
                    "identifier": "ENDPOINT=Postmark,METHOD=POST,HEADER=Accept",
                    "endpoint": "ENDPOINT=Postmark,METHOD=POST",
                    "key": "Accept",
                    "value": "application/json",
                    "description": "",
                },
                request_only=False,
                response_only=True,
            ),
        ]

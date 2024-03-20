Order Store
###########

    The ``order_store`` module provides a way to keep track of the state of an order. It offers methods that can be called from the CPEE to update the state of the order. The state of the order is stored on a thread safe que.
    Also it provides getter methods to get the state of the order which is used by the Website to display the states of the orders to the user.

    The figure below shows the high-level architecture of the ``order_store`` module:
    The order store is the interface between the CPEE and the website. The CPEE sends the order state to the order store and the website gets the order state from the order store.



    .. image:: images/order_store.png
       :alt: alternative text
       :align: center

    The ``order_store`` supports a RESTful API implemented using Flask.
    See below for detailed documentation of its API endpoints and functionality.

    **API Endpoints**:

        **Update Order Status**:

        - **URL**: ``/update_order`` (configured via ``conf_order_store.URL_UPDATE``)
        - **Method**: ``PUT``
        - **Description**: Updates the status of an order based on the provided order ID, orderbot ID, and new status. The endpoint accepts both JSON and form-encoded request bodies.
        - **Request Fields**:

        When sending form-encoded data:

            - ``order_id``: The ID of the order to update.
            - ``orderbot_id``: The ID of the orderbot associated with the order.
            - ``status``: The new status of the order.

        When sending JSON data:

            - ``id``: The ID of the order to update.
            - ``orderbot_id``: The ID of the orderbot associated with the order.
            - ``status``: The new status of the order.

        - **Example request with JSON data**:

            .. sourcecode:: http

                PUT /update-order HTTP/1.1
                Host: example.com
                Content-Type: application/json

                {
                    "id": 1,
                    "orderbot_id": "123",
                    "status": "Processing"
                }

        - **Success Response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Content-Type: application/json

                {
                    "message": "Order updated"
                }

        - **Error Response**:

            If the request is missing required data:

            .. sourcecode:: http

                HTTP/1.1 400 Bad Request
                Content-Type: application/json

                {
                    "error": "Missing data"
                }




        **Get All Orders**:

        - **URL**: ``/get_all`` (configured via ``conf_order_store.URL_GET_ALL``)
        - **Method**: ``GET``
        - **Description**: Retrieves a list of all orders, useful for debugging purposes.
        - **Success Response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Content-Type: application/json

                    [
                        {
                            "order_id": 1,
                            "status": "Processing",
                            "orderbot_id": "123"
                        },
                        "..."
                    ]


        **Get Current Orders**:

        - **URL**: ``/get_current_order`` (configured via ``conf_order_store.URL_GET_CURRENT``)
        - **Method**: ``GET``
        - **Description**: Fetches orders that have not yet been served and are currently in progress.

        - **Success Response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Content-Type: application/json

                    {
                        "incomplete_orders": [
                        {
                            "id": 1,
                            "orderbot_id": "123",
                            "status": "Processing"
                        },
                        "..."
                        ]
                    }


    **Get Completed Orders**:

    - **URL**: ``/get_completed_orders`` (configured via ``conf_order_store.URL_GET_COMPLETED``)
    - **Method**: ``GET``
    - **Description**: Retrieves orders that have been marked as served.
    - **Success Response**:

        .. sourcecode:: http

          HTTP/1.1 200 OK
          Content-Type: application/json

          {
              "completed_orders": "[1, 2, 3, ...]"
          }



    **Get New Orders**:

    - **URL**: ``/get_new_orders`` (configured via ``conf_order_store.URL_GET_NEW``)
    - **Method**: ``GET``
    - **Description**: Fetches orders that have been initiated but not yet started or served.
    - **Success Response**:

       .. sourcecode:: http

          HTTP/1.1 200 OK
          Content-Type: application/json

          {
              "new_orders": "[4, 5, 6, ...]"
          }


    **Module Implementation**:

    .. automodule:: order_store
        :members:
        :undoc-members:
        :show-inheritance:
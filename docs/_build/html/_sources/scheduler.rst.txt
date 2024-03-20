Schedulers
##########
    The schedulers are the heart of the order system. They manage the callbacks and the orders that arrive from the CPEE and the user.
    The figure below describes the interaction between the different modules and the CPEE.

    .. image:: images/Scheduler.png
       :alt: alternative text
       :align: center


callback_scheduler
******************

    The ``callback_scheduler`` module is designed to provide interaction with the CPEE by managing callback URLs. It is integrated closely with the ``order_scheduler'' module to allow seamless processing of new orders and callbacks. The module provides a mechanism for registering new callback URLs, which are then used to notify the CPEE of new orders. If no new orders are available when a callback is registered, the callback URL is placed in a thread-safe queue until it can be processed. This module includes functionality to add and retrieve callbacks to the queue, allowing efficient communication with the CPEE.

    The ``callback_scheduler`` supports a RESTful API implemented using Flask.
    See below for detailed documentation of its API endpoints and functionality.



    **API Endpoints**:


        **Set Callback**

        - **URL**: ``/set_callback`` (configurable via ``conf_callback.URL_SET``)
        - **Method**: ``GET``
        - **Description**: Adds a new callback URL to the queue if there are no immediate orders to process. If an order is available, the order data is sent back immediately.
        - **Headers**: Must include ``Cpee-Callback`` with the callback URL.
        - **Success Response**:

          If an order is available:

          .. sourcecode:: http

             HTTP/1.1 200 OK
             Content-Type: application/json

             {
                "id": "...",
                "orderbot_id": -1,
                "status": "Order Initiated"
             }

          If no order is available and the callback is queued:

          .. sourcecode:: http

             HTTP/1.1 200 OK
             Content-Type: application/json
             CPEE-CALLBACK: true

             {
                "message": "Callback URL added to the queue"
             }
        - **Error Response**:

            **Code**: 400 (Bad Request),
            **Content**: ``{"error": "No Cpee-Callback header found"}``


            **Code**: 500 (Internal Server Error),
            **Content**: ``{"error": "<error_message>"}``

        **Get Callback**

        - **URL**: ``/get_callback`` (configurable via ``conf_callback.URL_GET``)
        - **Method**: ``GET``
        - **Description**: Retrieves and removes the next callback URL from the queue if available.
        - **Success Response**:
          If a callback URL is available:

          .. sourcecode:: http

             HTTP/1.1 200 OK
             Content-Type: application/json

             {
                "callback_url": "CPEE Callback URL"
             }

          If no callback URL is available:

          .. sourcecode:: http

             HTTP/1.1 204 OK
             Content-Type: application/json

             {
                "message": "There are currently no callbacks available"
             }

        - **Error Response**:

          **Code**: 204 (No Content),
          **Content**: ``{"message": "There are currently no callbacks available"}``


        **Get All Callbacks (Debug)**

        - **URL**: ``/get_all_callbacks`` (configurable via ``conf_callback.URL_DEBUG``)
        - **Method**: ``GET``
        - **Description**: Returns a list of all callback URLs currently in the queue. This endpoint is intended for debugging purposes.
        - **Success Response**:

            .. sourcecode:: http

                 HTTP/1.1 200 OK
                 Content-Type: application/json

                 {
                    "all_callbacks": "[<callback_url_1>, <callback_url_2>, ...]"
                 }


    **Module Implementation**:


    .. automodule:: callback_scheduler
        :members:
        :undoc-members:
        :show-inheritance:

order_scheduler
***************

    The ``order_scheduler`` module is designed to provide interaction between the ``order_management_system`` and the ``callback_scheduler``. The module provides a mechanism for registering a new orders or getting new set orders from a que. After registering a new order, it first checks the ``callback_scheduler`` if there are currently any callback URLs available. If so it fetches a new callback URL and sends the order back to the CPEE using the callback URL. If there are currently no callback URLs available, it stores the new order inside a thread safe que until the order can be further processed by the ``callback_scheduler``. This module includes functionality to add and retrieve orders to the queue, allowing efficient communication with the CPEE.

    The ``order_scheduler`` supports a RESTful API implemented using Flask.
    See below for detailed documentation of its API endpoints and functionality.

    **API Endpoints**:

        **Set Order**

        - **Endpoint**: ``/set_order`` (configurable via ``conf_order.URL_SET``)
        - **Method**: ``POST``
        - **Description**: Adds a new order to the queue. If a callback URL is available, the order is sent directly to the callback URL.
        - **Request Body**: The expected JSON payload containing the order data:

           .. sourcecode:: json

              {
                "drink": "Gin Tonic",
                "size": "Medium",
                "name": "John Doe"
              }


        - **Success Response**:
            If the order is added to the queue:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Content-Type: application/json

                {
                    "message": "Order added to the queue",
                    "order_id": 1
                }

            If the order is sent to a callback URL:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Content-Type: application/json

                {
                    "message": "Order sent to callback URL",
                    "order_id": 1
                }

        - **Error Response**:

                If no order data is provided or data is incomplete:

                .. sourcecode:: http

                    HTTP/1.1 400 Bad Request
                    Content-Type: application/json

                    {
                        "error": "No order data provided/Missing order details"
                    }

                If there is an error with the request to the callback URL:

                .. sourcecode:: http

                    HTTP/1.1 500 Internal Server Error
                    Content-Type: application/json

                    {
                        "error": "Error message describing the issue"
                    }


        **Get Order**

        - **Endpoint**: ``/get_order`` (configurable via ``conf_order.URL_GET``)
        - **Method**: ``GET``
        - **Description**: Retrieves the next order from the queue and removes it.
        - **Success Response**:
            If an order is available:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Content-Type: application/json

                {
                    "order_id": 1,
                    "drink": "Gin Tonic",
                    "size": "Medium",
                    "name": "John Doe",
                }

            If the queue is empty:

            .. sourcecode:: http

                HTTP/1.1 204 No Content
                Content-Type: application/json

                {
                    "message": "No orders in the queue"
                }

        **Get All Orders (Debug)**

           - **Endpoint**: ``/get_all_orders`` (configurable via ``conf_order.URL_DEBUG``)
           - **Method**: ``GET``
           - **Description**: Retrieves all orders currently in the queue. Intended for debugging purposes.
           - **Success Response**:
            Allways returns a list of all orders currently in the queue.

            .. sourcecode:: http

              HTTP/1.1 200 OK
              Content-Type: application/json

              {
                  "all_orders": [
                      {
                          "order_id": 1,
                          "drink": "Gin Tonic",
                          "size": "Medium",
                          "name": "John Doe",
                      },
                      "..."
                  ]
              }

    **Module Implementation**:

    .. automodule:: order_scheduler
        :members:
        :undoc-members:
        :show-inheritance:
Simulator
#########

    The ``simulator`` module provides a simple simulator simulating the behavior of the mechanics behind the cocktail making machine.

    It offers the simulation of the following components:
    - The pumping of non alcoholic and alcoholic liquids
    - The processing of non liquid ingredients
    - The mixing of the ingredients

    The figure below shows the high-level architecture of the ``simulator`` module:
    The simulator just simulates the consume of different ingredients and the mixing of them. It does not have any physical components.

    .. image:: images/Simulator.png
       :alt: alternative text
       :align: center

    The ``simulator`` supports a RESTful API implemented using Flask.
    See below for detailed documentation of its API endpoints and functionality.


    **API Endpoints**:


        **Pump Liquids**:

        - **URL**: ``/pump_liquid``
        - **Method**: ``POST``
        - **Description**: Simulates pumping alcoholic and non alcoholic liquids based on the given amount and type defined by each recipe.
        - **Request Fields**:

            When sending form-encoded data:

            - ``liquor``: A JSON-encoded array containing liquor items with their names and amounts in grams.
            - ``non_alcohol``: A JSON-encoded array containing non-alcohol items with their names and amounts in grams.

            When sending JSON data:

            - ``liquor``: An array containing liquor items with their names and amounts in grams.
            - ``non_alcohol``: An array containing non-alcohol items with their names and amounts in grams.

        - **Example request with JSON data**:

        .. sourcecode:: http

            POST /pump_liquid HTTP/1.1
            Host: example.com
            Content-Type: application/json

                {
                    "liquor": [
                        {
                            "name": "Vodka",
                            "amount_grams": 50
                        }
                    ],
                    "non_alcohol": [
                        {
                            "name": "Orange Juice",
                            "amount_grams": 100
                        }
                    ]
                }

        - **Success Response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                "message": "Ingredients processed successfully"
            }

        - **Error Response**:

        If the request is invalid or missing required fields:

        .. sourcecode:: http

            HTTP/1.1 400 Bad Request
            Content-Type: application/json

            {
                "error": "Invalid request, missing 'liquor' or 'non_alcohol'"
            }


        **Processing Other Ingredients**:

        - **URL**: ``/process_ingredient``
        - **Method**: ``POST``
        - **Description**: Simulates the processing of non liquid ingredients. (e.g. ice, sugar, salt, etc.)
        - **Request Fields**:

            When sending form-encoded data:

            - ``other``: A JSON-encoded array containing other ingredient items with their names and amounts in grams.

            When sending JSON data:

            - ``other``: An array containing other ingredient items with their names and amounts in grams.

        - **Example request with JSON data**:

        .. sourcecode:: http

            POST /process_ingredient HTTP/1.1
            Host: example.com
            Content-Type: application/json

            {
                "other": [
                    {
                        "name": "Garnish",
                        "amount_grams": 5
                    }
                ]
            }

        - **Success Response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                "message": "Other ingredients processed successfully"
            }

        - **Error Response**:

        If the request is invalid or missing the 'other' field:

        .. sourcecode:: http

            HTTP/1.1 400 Bad Request
            Content-Type: application/json

            {
                "error": "Invalid request, missing 'Other'"
            }

        **Mix**:

        - **URL**: ``/mix``
        - **Method**: ``POST``
        - **Description**: Simulates mixing the cocktail based on the given mix technique, strength and duration defined by each cocktail recipe.
        - **Request Fields**:

            When sending form-encoded data:

            - ``mix_technique``: A JSON-encoded object containing the mixing technique, strength, and duration.

            When sending JSON data:

            - ``technique``: The technique used for mixing the cocktail.
            - ``strength``: The intensity of mixing.
            - ``duration``: The time duration for which ingredients are to be mixed.

        - **Example request with JSON data**:

        .. sourcecode:: http

            POST /mix HTTP/1.1
            Host: example.com
            Content-Type: application/json

            {
                "technique": "Shake",
                "strength": "Medium",
                "duration": "5"
            }

        - **Success Response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                "message": "Mixed cocktail successfully"
            }

        - **Error Response**:

        If the request is invalid or missing required fields:

        .. sourcecode:: http

            HTTP/1.1 400 Bad Request
            Content-Type: application/json

            {
                "error": "Invalid request, missing required mixing parameters"
            }

    **Module Implementation**:

    .. automodule:: simulator
        :members:
        :undoc-members:
        :show-inheritance:
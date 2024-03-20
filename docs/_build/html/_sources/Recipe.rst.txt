Recipe Service
##############

    The ``recipe_service`` is a simple service that allows to qurry the database for recipes. The recipes can be updated by editing the recipe.json file.

    The figure below shows the high-level architecture of the ``recipe_service`` module:
    The CPEE querrys a new recipe and the recipe service returns the recipe from the recipe.json file.

    .. image:: images/recipe_service.png
       :alt: alternative text
       :align: center

    The ``recipe_service`` supports a RESTful API implemented using Flask.
    See below for detailed documentation of its API endpoints and functionality.

    **API Endpoints**:

        **Get Recipe**

        - **URL**: ``/get`` (configurable via ``conf_recepie.URL_GET``)
        - **Method**: ``GET``
        - **Description**: Returns a JSON object containing the ingredients for the requested cocktail.
        - **Query Parameters**:

            - ``cocktail``: The name of the cocktail for which to retrieve ingredients.

        - **Success Response**:

            If the cocktail is found:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Content-Type: application/json

                {
                  "name": "Mojito",
                  "cocktail_id": 5,
                  "ingredients": {
                    "non_alcohol": [
                      {
                        "name": "Soda Water",
                        "amount_grams": 100
                      },
                      {
                        "name": "Lime Juice",
                        "amount_grams": 30
                      }
                    ],
                    "liquor": [
                      {
                        "name": "White Rum",
                        "amount_grams": 50
                      }
                    ],
                    "other": [
                      {
                        "name": "Mint Leaves",
                        "amount_grams": 10
                      },
                      {
                        "name": "Sugar",
                        "amount_grams": 20
                      }
                    ]
                  },
                  "mix_technique":
                      {
                        "technique": "mix",
                        "strength": 8,
                        "duration": 15
                      }

                }

        - **Error Response**:
            If the cocktail is not found:

            .. sourcecode:: http

                HTTP/1.1 404 Not Found
                Content-Type: application/json

                {
                    "error": "Cocktail not found"
                }

            If there is an error fetching cocktails data:

            .. sourcecode:: http

                HTTP/1.1 <ErrorStatusCode>
                Content-Type: application/json

                {
                    "error": "Failed to fetch cocktails data"
                }

            If there is a server error:

            .. sourcecode:: http

                HTTP/1.1 500 Internal Server Error
                Content-Type: application/json

                {
                    "error": "Server error",
                    "message": "<ErrorDescription>"
                }

    **Module Implementation**:

    .. automodule:: recipe_service
        :members:
        :undoc-members:
        :show-inheritance:
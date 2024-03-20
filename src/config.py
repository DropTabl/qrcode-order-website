BASE_URL = "https://lehre.bpm.in.tum.de/ports/"
#https://lehre.bpm.in.tum.de/ports/8120/set_callback

#https://lehre.bpm.in.tum.de/ports/8120/
class conf_callback_sched:
    PORT = 8120
    URL_GET = "/get_callback"
    URL_SET = "/set_callback"
    URL_DEBUG = "/getall"


#https://lehre.bpm.in.tum.de/ports/8121/
class conf_order_sched:
    PORT = 8121
    URL_GET = "/get_order"
    URL_SET = "/set_order"
    URL_DEBUG = "/getall"

#Order Example
orderexamlple = {
    "order_id": 123,
    "drink": "GinTonic",
    "size": "Large",
    "name": "John Doe"
}

class conf_static_oms:
    PORT = 8122
    URL_SET = "/OMS/"

class conf_link_creation:
    PORT = 8123
    URL_GET = "/get_cocktail_links"


class conf_avail_cocktails:
    URL_GET = "https://lehre.bpm.in.tum.de/~ge56qon/PHP/avail_cocktails.php"

class conf_static_website:
    # https://lehre.bpm.in.tum.de/ports/8124
    PORT = 8124



#https://lehre.bpm.in.tum.de/ports/8125/get_ingredients
class conf_querry_recepie:
    PORT = 8125
    URL_GET = "/get_ingredients"
    RECEPIE_PATH = "https://lehre.bpm.in.tum.de/~ge56qon/PHP/serve_cocktails.php"


#https://lehre.bpm.in.tum.de/ports/8126/pump_ingredients
#https://lehre.bpm.in.tum.de/ports/8126/process_ingredients
class conf_process_ingredients:
    PORT = 8126
    URL_PUMP = "/pump_liquids"
    URL_PROCESS = "/process_ingredients"
    URL_MIX = "/mix_ingredients"
    URL_SERVE = "/serve_cocktail"
    URL_COMPLETE= "/complete"

class conf_shoutout:
    PORT = 8127
    URL_SET = "/shoutout"

class conf_analyse_logs:
    PORT = 8128
    URL_SET = "/analyse"


#https://lehre.bpm.in.tum.de/ports/8129/get_current

class conf_order_store:
    PORT = 8129
    URL_UPDATE = "/update_status"
    URL_GET = "/get_status/<int:id>'"
    URL_GET_ALL = "/get_all"
    URL_GET_CURRENT = "/get_current"
    URL_GET_COMPLETED = "/get_completed"
    URL_GET_NEW = "/get_new"
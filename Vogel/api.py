from ninja import NinjaAPI

api = NinjaAPI()

api.add_router("/observations/", "observation.api.router")
api.add_router("/species/", "species.api.router")
from ninja import NinjaAPI
from award.api import router as award_router
from user.api import router as user_router
from trivia.api import router as trivia_router

api = NinjaAPI()

api.add_router("/awards/", award_router)
api.add_router("/authenticate/", user_router)
api.add_router("/trivia/", trivia_router)

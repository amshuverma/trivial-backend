from ninja import Router
from .schema import TriviaCategorySchema
from .models import TriviaCategory as TriviaCategoryModel
from user.api import AuthBearer

router = Router(auth=AuthBearer())


@router.get("/trivia-categories")
def get_trivia_categories(request):
    trivias = TriviaCategoryModel.objects.all()
    return 200, trivias


@router.post("/trivia-categories")
def create_trivia_category(request, payload: TriviaCategorySchema):
    trivia_category = TriviaCategoryModel(**payload.dict())
    trivia_category.save()
    return 200, {"trivia_category_id": trivia_category.uid}

from ninja import Router
from typing import List

from .schema import TriviaCategoryInSchema, TriviaCategoryOutSchema, AllTriviaSchema, TriviaLogOutSchema
from .models import TriviaCategory as TriviaCategory, Trivia, UserTriviaLog
from user.api import AuthBearer

router = Router(auth=AuthBearer())


@router.get("/trivia-categories", response=List[TriviaCategoryOutSchema])
def get_trivia_categories(request):
    trivia_categories = TriviaCategory.objects.all()
    return 200, trivia_categories


@router.post("/trivia-categories")
def create_trivia_category(request, payload: TriviaCategoryInSchema):
    trivia_category = TriviaCategoryModel(**payload.dict())
    trivia_category.save()
    return 200, {"trivia_category_id": trivia_category.uid}


@router.get("/all-trivia", response=List[AllTriviaSchema])
def get_all_trivia(request):
    trivias = Trivia.objects.all()
    return 200, trivias


@router.get("/trivia-logs", response=List[TriviaLogOutSchema])
def get_all_logs(request):
    logs = UserTriviaLog.objects.all()
    return 200, logs
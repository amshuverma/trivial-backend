from typing import List

from ninja import Router
from user.api import AuthBearer

from .models import Trivia, TriviaCategory, UserTriviaLog
from .schema import (AllTriviaSchema, TriviaCategoryInSchema,
                     TriviaCategoryOutSchema, TriviaLogOutSchema)

router = Router(auth=AuthBearer())


@router.get("/trivia-categories", response=List[TriviaCategoryOutSchema])
def get_trivia_categories(request):
    trivia_categories = TriviaCategory.objects.all()
    return 200, trivia_categories


@router.post("/trivia-categories")
def create_trivia_category(request, payload: TriviaCategoryInSchema):
    trivia_category = TriviaCategory(**payload.dict())
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

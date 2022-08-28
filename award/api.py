from typing import List

from ninja import Router
from user.api import AuthBearer

from .models import Award as AwardModel
from .schema import AwardSchema

router = Router()


@router.get("/", response=List[AwardSchema])
def get_awards(request):
    awards = AwardModel.objects.all()
    return 200, awards


@router.post("/create")
def create_award(request, payload: AwardSchema):
    award = AwardModel(**payload.dict())
    award.save()
    return 200, {"award_id": award.uid}

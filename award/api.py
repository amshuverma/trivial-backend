from ninja import Router
from typing import List

from user.api import AuthBearer

from .models import Award as AwardModel
from .schema import AwardSchema

router = Router(auth=AuthBearer())


@router.get("/", response=List[AwardSchema])
def get_awards(request):
    awards = AwardModel.objects.all()
    print(request.auth.first_name)
    return 200, awards


@router.post("/")
def create_award(request, payload: AwardSchema):
    award = AwardModel(**payload.dict())
    award.save()
    return 200, {"award_id": award.uid}

from fastapi import APIRouter

from common.decorator.responseMessage import response_message
from common.middleware.response_wrapper import ResponseInterceptorRoute

router = APIRouter(route_class=ResponseInterceptorRoute)


@router.get(
    "",
)
@response_message("OK")
async def get():
    return {"a": "a"}


@router.get(
    "/test",
)
async def get():
    return {"a": "a"}

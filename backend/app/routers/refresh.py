from logging import Logger

from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from fastapi.requests import Request

from containers import Container
from custom_exceptions import NotAuthenticatedException
from services import JwtToken
from utils import refresh_token_cookies

router = APIRouter(
    prefix="/refresh", tags=["User"]
)

 
@router.post("/")
@inject
async def new_token(
    request: Request,
    response: Response,
    jwt_token_service: JwtToken = Depends(Provide[Container.jwt_token]),
    logger: Logger = Depends(Provide[Container.logger]),
    config = Depends(Provide[Container.config]),
):
    """ Gets refresh token from the cookies and creates new access token and rotates refesh token. """

    refresh_token_key = "refresh_token"
    request_refresh_token = request.cookies.get(refresh_token_key)

    if request_refresh_token is None:
        logger.error("'POST /refresh' hit without provided refesh token in cookies.")
        raise NotAuthenticatedException

    access_token, refresh_token = await jwt_token_service.create_token_pair_from_refresh(encoded_refresh_token=request_refresh_token)

    if refresh_token is not None:
        try:
            expiration_str = config["refresh_token_expiration_in_hours"]
            expiration = int(expiration_str)

        except ValueError:
            logger.error(f"Cannot parse '{expiration_str}' value.")
            expiration = 24

        refresh_token_cookies(response, value=refresh_token, max_age=expiration * 60 * 60)

    else:
        response.delete_cookie(refresh_token_key)
    
    # TODO: XSRF-TOKEN
    #refresh_token_cookies(response, key="XSRF-TOKEN", value="...")
    return {"token": access_token}

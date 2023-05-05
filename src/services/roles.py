from typing import List

from fastapi import Depends, HTTPException, status, Request

from src.database.models import Guest, Role
from src.services.auth import auth_service


class RoleAccess:
    def __init__(self, allowed_roles: List[Role]):
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request, current_user: Guest = Depends(auth_service.get_current_user)):
        """
        The __call__ function is the function that will be called when a user tries to access an endpoint.
        It takes in two parameters: request and current_user. The request parameter is the Request object, which contains all of
        the information about the incoming HTTP request (headers, body, etc.). The current_user parameter is a Guest object that
        contains information about who made this particular HTTP request (if they are logged in). This value comes from our auth_service's get_current_user() function.

        :param self: Refer to the class itself
        :param request: Request: Pass the request object to the function
        :param current_user: Guest: Get the current user from the database
        :return: A response object
        :doc-author: Trelent
        """
        if current_user.roles not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation forbidden")

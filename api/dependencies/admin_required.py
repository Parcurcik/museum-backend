from fastapi import Depends, HTTPException, status
from api.dependencies import get_current_user
from api.models import UserORM
from api.models.enums import UserRoleEnum


async def admin_required(current_user: UserORM = Depends(get_current_user)):
    if UserRoleEnum.admin not in [role.role for role in current_user.roles]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

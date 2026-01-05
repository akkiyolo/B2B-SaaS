import httpx # 
from fastapi import Depends, HTTPException, Request, status
from clerk_backend_api.security import AuthenticateRequestOptions
from app.core.config import settings
from app.core.clerk import clerk

## frontend sends a request to backend using a jwt token from clerk
## backend is going to authenticate this token
  ## after this we will get user details and we will check user permissions

class AuthUser:
  def __init__(self,user_id:str,org_id:str,org_permissions:list):
    self.user_id=user_id
    self.org_id=org_id
    self.org_permissions=org_permissions

    def has_permission(self,permission:str)->bool: # checks if user has a specific permission
      return permission in self.org_permissions

    @property
    def can_view(self)->bool:
      return self.has_permission("org:tasks:view") # view is associated with this tasks and tasks are associated with org
    
    @property
    def can_create(self)->bool:
      return self.has_permission("org:tasks:create") # create is associated with this tasks and tasks are associated with org
    
    @property
    def can_delete(self)->bool:
      return self.has_permission("org:tasks:delete") # delete is associated with this tasks and tasks are associated with org 
    
    @property
    def can_edit(self)->bool:
      return self.has_permission("org:tasks:edit") # edit is associated with this tasks and tasks are associated with org 

  def convert_to_httpx_request(self,request:Request)->httpx.Request:
    return httpx.Request(
      method=fastapi_request.method,
      url=str(fastapi_request.url),
      headers=dict(fastapi_request.headers)
    )

  async def get_current_user(request:Request)->AuthUser:
    httpx_request=convert_to_httpx_request(request)

    request_state=clerk.authenticate_request(
      httpx_request,
      AuthenticateRequestOptions(authorized_parties=[settings.FRONTEND_URL])
    )

    if not request.state.is_signed_in:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authenticated"
      )
    
    claims=request_state.payload
    user_id=claims.get("sub")
    org_id=claims.get("org_id")
    org_permissions=claims.get("permissions") or claims.get("org_permissions") or []

    if not user_id:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authenticated"

      )
    
    if not org_id:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,detail="No organization selected"

      )
    
    return AuthUser(user_id=user_id,org_id=org_id,org_permissions=org_permissions)
    

  def require_view(user:AuthUser=Depends(get_current_user))->AuthUser:
    if not user.can_view:
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="View permission required"

      )
    
    return user
  
  def require_create(user:AuthUser=Depends(get_current_user))->AuthUser:
    if not user.can_create:
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Create permission required"

      )
    
    return user
  
  def require_delete(user:AuthUser=Depends(get_current_user))->AuthUser:
    if not user.can_delete:
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Delete permission required"

      )
    
    return user
  
  def require_edit(user:AuthUser=Depends(get_current_user))->AuthUser:
    if not user.can_edit:
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Edit permission required"

      )
    
    return user
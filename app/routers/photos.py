from fastapi import APIRouter, Response
from fastapi.responses import FileResponse
from app.definitions import ROOT_DIR


router = APIRouter()

@router.get("/uploads/{filename}")
def get_photo_image(filename: str, response: Response):
    path = f"{ROOT_DIR}/uploads/{filename}"
    print(f"PATH: {path}")
    #if not path.is_file():
  #      response.status_code = status.HTTP_404_NOT_FOUND
  #      return {"error": "image not found"}
    return FileResponse(path)
    
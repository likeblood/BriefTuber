from typing import Any, Optional

from pydantic import BaseModel, Field

from service.enums import VideoLanguage, VideoPreprocessStatus


class Error(BaseModel):
    """
    Base error model for all errors in the API.
    """
    error_key: str = Field(..., description="Error key")
    error_message: str = Field(..., description="Error message")
    error_loc: Optional[Any] = Field(None, description="Error location")


class VideoObj(BaseModel):
    video_link: str = Field(..., description="Video link")
    preprocess_status: VideoPreprocessStatus = Field(..., description="Video preprocess status")
    ready_message: list = Field(..., description="Video preprocess status")
    video_start_time: str = Field(..., description="Video start time (hh:mm:ss or START)")
    video_end_time: str = Field(..., description="Video end time (hh:mm:ss or END)")
    annotation_length: str = Field(..., description="Annotation length (count or ANY)")
    article_length: str = Field(..., description="Article length (count or ANY)")


class VideoUploadFormat(BaseModel):
    video_link: str = Field(..., description="Video link")
    video_start_time: str = Field(..., description="Video start time (hh:mm:ss or START)")
    video_end_time: str = Field(..., description="Video end time (hh:mm:ss or END)")
    annotation_length: str = Field(..., description="Annotation length (count or ANY)")
    article_length: str = Field(..., description="Article length (count or ANY)")
    
class VideoResponceFormat(BaseModel):
    preprocess_status: str = Field(..., description="Video preprocess status")
    id: str = Field(..., description="Video id")
    ready_message: list = Field(..., description="Video preprocess status")

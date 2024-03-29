import os
import threading

from typing import Tuple

from fastapi import APIRouter, Depends, FastAPI
from fastapi.responses import JSONResponse

from service.api.exceptions import GeneralLogicError
from service.creds import MONGO_URI
from service.enums import VideoPreprocessStatus
from service.log import app_logger
from service.models import VideoObj, VideoUploadFormat, VideoResponceFormat
from service.mongo import MongoORM
from service.pipeline import Video2ArticlePipeline

router = APIRouter()


def build_connections() -> Tuple[MongoORM, Video2ArticlePipeline]:
    """
    Build connections to DB and web3.

    Returns:
        Tuple[MongoORM, Web3]: mongo and web3 connections
    """
    mongo_conn = MongoORM(MONGO_URI)
    mongo_conn.database = 'videos'

    pipeline = Video2ArticlePipeline(
        youtube_link=None, # than replace in upload_video
        json_key_path=os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )
    return mongo_conn, pipeline


MONGO_CONN, PIPELINE = build_connections()


@router.get(
    path="/health",
    tags=["Health"],
)
async def health() -> str:
    """
    Health service check.
    """
    return "I am alive"


@router.post(
    path="/upload_video",
    tags=["Upload video"],
)
async def upload_video(
    video: VideoUploadFormat = Depends(),
) -> str:
    """
    Upload video to the database.

    Args:
        video (VideoUploadFormat): video to upload

    Returns:
        str: id of the added video
    """
    app_logger.info("Upload video %s", video)
    try:
        app_logger.info("Upload video %s", video)
        video_obj = VideoObj(
            video_link=video.video_link,
            preprocess_status=VideoPreprocessStatus.UPLOADED,
            ready_message=['Working'],
            video_start_time=video.video_start_time,
            video_end_time=video.video_end_time,
            annotation_length=video.annotation_length,
            article_length=video.article_length
        )

        app_logger.info("Add video %s", video)
        video_id = MONGO_CONN.add_video(video_obj)
        video_responce_obj = VideoResponceFormat(
            preprocess_status=video_obj.preprocess_status.value,
            id=video_id,
            ready_message=video_obj.ready_message
        )

        app_logger.info("Run pipeline %s", video)
        PIPELINE.link = video.video_link
        PIPELINE._video_id = video_id
        PIPELINE._orm = MONGO_CONN

        # run pipeline in separate thread
        thread = threading.Thread(target=PIPELINE.run)
        thread.start()

        return JSONResponse({'preprocess_status': video_responce_obj.preprocess_status, 'id': video_responce_obj.id, 'ready_message': video_responce_obj.ready_message})
    except Exception as e:
        app_logger.exception(e)
        raise GeneralLogicError()


@router.post(
    path="/get_video_status/{video_id}",
    tags=["Get video status"],
)
async def get_video_status(
    video_id: str,
) -> VideoPreprocessStatus:
    """
    Get video preprocess status.

    Args:
        video_id (str): video id

    Returns:
        VideoPreprocessStatus: video preprocess status
    """
    try:
        app_logger.info("Get video status %s", video_id)
        video = MONGO_CONN.get_video(video_id)
        video_responce_obj = VideoResponceFormat(
            preprocess_status=video.preprocess_status.value,
            id=video_id,
            ready_message=video.ready_message
        )
        return JSONResponse({'preprocess_status': video_responce_obj.preprocess_status, 'id': video_responce_obj.id, 'ready_message': video_responce_obj.ready_message})
    except Exception as e:
        app_logger.exception(e)
        raise GeneralLogicError()


def add_views(app: FastAPI) -> None:
    app.include_router(router)

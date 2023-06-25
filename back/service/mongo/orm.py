from typing import Dict
from typing import List

from bson import BSON
from bson.objectid import ObjectId
from pymongo import MongoClient

from service.models import VideoObj
from service.enums import VideoPreprocessStatus
from service.mongo.abc_orm import ORM
from service.mongo.codecs import codec_options


class MongoORM(ORM):
    """
    Mongo ORM.
    """

    def __init__(self, mongo_uri: str) -> None:
        """
        Init Mongo ORM.

        Args:
            mongo_uri (str): mongo uri in format mongodb://<user>:<password>@<host>:<port>
                             should be passed from env variable from creds.py
        """
        self._client: MongoClient = MongoClient(mongo_uri)
        self._database: str = None

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database: str):
        self._database = database

    def add_video(self, video: VideoObj) -> str:
        """
        Add video to the database.

        Args:
            video (VideoObj): video to add

        Returns:
            str: id of the added video
        """
        collection = self._client[self._database]['videos']
        encoded_dict: Dict = BSON.decode(BSON.encode(video.dict(), codec_options=codec_options))
        result = collection.insert_one(encoded_dict)
        return str(result.inserted_id)

    def get_video(self, video_id: str) -> VideoObj:
        """
        Get video from the database.

        Args:
            video_id (str): video

        Returns:
            VideoObj: video
        """
        collection = self._client[self._database]['videos']
        encoded_dict = collection.find_one({'_id': ObjectId(video_id)})
        decoded_dict = BSON.decode(BSON.encode(encoded_dict, codec_options=codec_options))
        return VideoObj(**decoded_dict)

    def update_video(self, video_id: str, ready_message: List[Dict], status: VideoPreprocessStatus) -> None:
        """
        Update video in the database. ready_message is a list of dicts with keys:

        Args:
            video (VideoObj): video to update
        """
        collection = self._client[self._database]['videos']
        collection.update_one(
            {'_id': ObjectId(video_id)},
            {'$set': {'ready_message': ready_message, 'preprocess_status': status.value}}
        )

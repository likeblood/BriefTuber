from enum import Enum


class VideoLanguage(Enum):
    """
    Available video languages.
    """
    RUS = 'rus'
    ENG = 'eng'


class VideoPreprocessStatus(Enum):
    """
    Available video preprocess statuses.
    """
    UPLOADED = 'uploaded'
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'
    FAILED = 'failed'

from bson.codec_options import CodecOptions, TypeCodec, TypeRegistry

from service.enums import VideoLanguage, VideoPreprocessStatus


class VideoLanguageCodec(TypeCodec):
    """
    Codec for DEX enum.
    """
    python_type = VideoLanguage
    bson_type = str

    def transform_python(self, value):
        return value.value

    def transform_bson(self, value):
        return VideoLanguage(value)


class VideoPreprocessStatusCodec(TypeCodec):
    """
    Codec for DEX enum.
    """
    python_type = VideoPreprocessStatus
    bson_type = str

    def transform_python(self, value):
        return value.value

    def transform_bson(self, value):
        return VideoPreprocessStatus(value)


# apply codecs
codec_options: CodecOptions = CodecOptions(
    type_registry=TypeRegistry([VideoLanguageCodec(), VideoPreprocessStatusCodec()])
)

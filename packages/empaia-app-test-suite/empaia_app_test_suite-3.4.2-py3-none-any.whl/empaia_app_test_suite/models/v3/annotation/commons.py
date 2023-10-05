from ...singletons import model_settings
from ..commons import RestrictedBaseModel


class PostValidationBase(RestrictedBaseModel):
    def __init__(self, **data):
        is_post = str(self.__class__).split(".")[-1].lower().startswith("post")
        if is_post and model_settings.disable_post_validation:
            return
        super().__init__(**data)

from .database import category as DatabaseCategory
from .image import category as ImageCategory
from .image_adjustment import category as ImageAdjustmentCategory
from .utility import category as UtilityCategory
from .chat import category as ChatCategory

builtin_categories = [
    ChatCategory,
    DatabaseCategory,
    ImageCategory,
    ImageAdjustmentCategory,
    UtilityCategory,
]
category_order = [x.name for x in builtin_categories]

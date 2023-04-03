from .database import category as DatabaseCategory
from .image import category as ImageCategory
from .image_adjustment import category as ImageAdjustmentCategory
from .utility import category as UtilityCategory

builtin_categories = [
    DatabaseCategory,
    ImageCategory,
    ImageAdjustmentCategory,
    UtilityCategory,
]
category_order = [x.name for x in builtin_categories]
print(category_order)

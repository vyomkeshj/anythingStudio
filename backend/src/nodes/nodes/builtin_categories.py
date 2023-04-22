from .database import category as DatabaseCategory
from .utility import category as UtilityCategory
from .chat import category as ChatCategory
from .games import category as GamesCategory
from .image import category as ImageCategory
from .text import category as TextCategory
from .llm import category as LLMCategory
from .data_loaders import category as DataLoaderCategory

builtin_categories = [
    DataLoaderCategory,
    GamesCategory,
    ChatCategory,
    LLMCategory,
    DatabaseCategory,
    UtilityCategory,
    TextCategory,
    ImageCategory
]
category_order = [x.name for x in builtin_categories]

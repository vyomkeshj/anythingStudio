from .database import category as DatabaseCategory
from .utility import category as UtilityCategory
from .chat import category as ChatCategory
from .charts import category as ChartCategory
from .games import category as GamesCategory
from .image import category as ImageCategory
from .text import category as TextCategory
from .data_loaders import category as DataLoaderCategory
from .builder import category as BuilderCategory
from .api import category as APICategory
from .chroma import category as ChromaCategory

builtin_categories = [
    APICategory,
    ChatCategory,
    DatabaseCategory,
    ChartCategory,
    TextCategory,
    DataLoaderCategory,
    UtilityCategory,
    GamesCategory,
    BuilderCategory,
    ImageCategory,
    ChromaCategory,
]
category_order = [x.name for x in builtin_categories]

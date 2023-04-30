from .database import category as DatabaseCategory
from .utility import category as UtilityCategory
from .chat import category as ChatCategory
from .charts import category as ChartCategory
from .games import category as GamesCategory
from .image import category as ImageCategory
from .text import category as TextCategory
from .llm import category as LLMCategory
from .data_loaders import category as DataLoaderCategory
from .langchain import category as LangchainCategory
from .builder import category as BuilderCategory
# from .huggingface import category as HuggingfaceCategory

builtin_categories = [
    # HuggingfaceCategory,
    BuilderCategory,
    ChartCategory,
    GamesCategory,
    DataLoaderCategory,
    ChatCategory,
    LLMCategory,
    DatabaseCategory,
    UtilityCategory,
    TextCategory,
    ImageCategory,
    LangchainCategory,
]
category_order = [x.name for x in builtin_categories]

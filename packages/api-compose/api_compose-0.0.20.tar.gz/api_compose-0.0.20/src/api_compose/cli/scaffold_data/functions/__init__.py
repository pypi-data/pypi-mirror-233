from api_compose import get_logger
from api_compose import FunctionsRegistry

logger = get_logger(name=__name__)


@FunctionsRegistry.set(name='some_function')
def some_function() -> int:
    return 1


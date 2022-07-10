from ..application.handlers import get_pages
from ..application.queries import GetPages

query_handlers = {
    GetPages: get_pages,
}

from dataclasses import dataclass

from atoti_core import get_package_version, keyword_only_dataclass


@keyword_only_dataclass
@dataclass(frozen=True)
class WidgetConversionDetails:
    mdx: str
    session_id: str
    widget_creation_code: str


_MAJOR_VERSION = get_package_version(__name__).split(".", maxsplit=1)[0]

CONVERT_QUERY_RESULT_TO_WIDGET_MIME_TYPE = (
    f"application/vnd.atoti.convert-query-result-to-widget.v{_MAJOR_VERSION}+json"
)

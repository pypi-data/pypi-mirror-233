from typing import Dict, TypedDict, Union
from typing_extensions import Required


class IngestSpan(TypedDict, total=False):
    """ ingest_span. """

    description: str
    exclusive_time: Union[int, float]
    is_segment: bool
    op: str
    parent_span_id: str
    profile_id: str
    segment_id: str
    sentry_tags: Dict[str, str]
    span_id: str
    start_timestamp: Required[Union[int, float]]
    """ Required property """

    status: str
    tags: Dict[str, str]
    timestamp: Required[Union[int, float]]
    """ Required property """

    trace_id: Required[str]
    """ Required property """



class IngestSpanMessage(TypedDict, total=False):
    """ ingest_span_message. """

    event_id: str
    organization_id: Required[int]
    """ Required property """

    project_id: Required[int]
    """ Required property """

    retention_days: Required[int]
    """ Required property """

    span: Required["IngestSpan"]
    """ Required property """


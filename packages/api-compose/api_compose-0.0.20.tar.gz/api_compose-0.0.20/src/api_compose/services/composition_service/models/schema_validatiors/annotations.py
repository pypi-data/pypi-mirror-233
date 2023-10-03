from typing import Annotated

from pydantic import PlainSerializer

from api_compose.services.composition_service.models.schema_validatiors.enum import ValidateAgainst

ValidateAgainstAnnotation = Annotated[
    ValidateAgainst,
    PlainSerializer(lambda x: x.value, return_type=str, when_used='always')
]
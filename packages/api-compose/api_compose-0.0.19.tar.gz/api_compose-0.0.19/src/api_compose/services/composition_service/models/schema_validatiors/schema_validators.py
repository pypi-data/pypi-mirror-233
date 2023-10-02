from typing import Optional, Dict, List, Union, Any, Literal

from lxml.etree import ElementBase
from pydantic import Field, ConfigDict

from api_compose.core.lxml.parser import get_default_schema, PrintableElementAnnotation, get_default_element
from api_compose.services.common.models.base import BaseModel
from api_compose.services.composition_service.models.schema_validatiors.annotations import ValidateAgainstAnnotation
from api_compose.services.composition_service.models.schema_validatiors.enum import ValidateAgainst


class BaseSchemaValidatorModel(BaseModel, extra='forbid'):

    model_name: Literal['BaseSchemaValidatorModel'] = Field(
        description=BaseModel.model_fields['model_name'].description
    )

    # Expected Schema
    schema_id: str = Field(
        description='Id of the schema used for comparison',
    )

    expected_schema: Any = Field(
        None,
        description='Schema used to validate an object'
    )

    # Actual Object
    against: ValidateAgainstAnnotation = Field(
        description='Validate against which part of the action',
    )
    actual: Any = Field(
        None,
        description='Actual object to be validated'
    )

    exec: Optional[str] = Field(None, description='Exception while validating schema')
    is_valid: bool = Field(False, description='Whether the object is valid')


class JsonSchemaValidatorModel(BaseSchemaValidatorModel):
    model_name: Literal['JsonSchemaValidatorModel'] = Field(
        description=BaseSchemaValidatorModel.model_fields['model_name'].description
    )
    # Expected Schema
    expected_schema: Dict = Field(
        {},
        description=BaseSchemaValidatorModel.model_fields['expected_schema'].description
    )

    # Actual Object
    actual: Union[List, Dict] = Field(
        {},
        description=BaseSchemaValidatorModel.model_fields['actual'].description
    )


class XmlSchemaValidatorModel(BaseSchemaValidatorModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    model_name: Literal['XmlSchemaValidatorModel'] = Field(
        description=BaseSchemaValidatorModel.model_fields['model_name'].description
    )

    # Expected Schema
    expected_schema: PrintableElementAnnotation = Field(
        get_default_schema(),
        description=BaseSchemaValidatorModel.model_fields[
            'expected_schema'].description
    )

    # Actual Object
    actual: ElementBase = Field(
        get_default_element(),
        description=BaseSchemaValidatorModel.model_fields['actual'].description
    )

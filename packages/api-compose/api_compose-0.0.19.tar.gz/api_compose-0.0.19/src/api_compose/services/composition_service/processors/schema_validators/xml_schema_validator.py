__all__ = ["XmlSchemaValidator"]

import traceback
from abc import ABC

from lxml import etree

from api_compose.core.logging import get_logger
from api_compose.services.common.registry.processor_registry import ProcessorRegistry, ProcessorCategory
from api_compose.services.composition_service.events.schema_validator import SchemaValidatorEvent
from api_compose.services.composition_service.models.schema_validatiors.schema_validators import \
    XmlSchemaValidatorModel
from api_compose.services.composition_service.processors.schema_validators.base_schema_validator import \
    BaseSchemaValidator

logger = get_logger(__name__)


@ProcessorRegistry.set(
    processor_category=ProcessorCategory.SchemaValidator,
    models=[
        XmlSchemaValidatorModel(
            model_name='XmlSchemaValidatorModel',
            id='OK',
            schema_id='200',
            against='output_body',
        ),
    ]
)
class XmlSchemaValidator(BaseSchemaValidator, ABC):
    """
    validate

    """

    def __init__(
            self,
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)

    def validate(self):
        super().validate()

        if self.is_setup_success:
            self.schema_validator_model.actual = self.actual

        try:
            xml_schema = etree.XMLSchema(self.expected_schema)
            xml_schema.validate(self.actual)
        except Exception as e:
            logger.error(traceback.format_exc(), SchemaValidatorEvent())
            self.schema_validator_model.exec = traceback.format_exc()
            self.schema_validator_model.is_valid = False
        else:
            logger.debug(f"Schema is valid - {self.actual=}", SchemaValidatorEvent())
            self.schema_validator_model.is_valid = True


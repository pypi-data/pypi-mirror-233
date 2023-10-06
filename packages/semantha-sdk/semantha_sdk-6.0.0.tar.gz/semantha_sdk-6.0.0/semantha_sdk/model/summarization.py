
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import Optional


@dataclass(frozen=True)
class Summarization(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    summary: Optional[str] = None

SummarizationSchema = class_schema(Summarization, base_schema=SemanthaSchema)

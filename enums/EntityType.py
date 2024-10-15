from enum import Enum


class EntityType(Enum):
    VENDOR = "Vendor"
    ASSET = "Asset"
    ENTITY = "Entity"
    PROCESSING_ACTIVITY = "Processing Activity"
    CONTRACT = "Contract"
    ENGAGEMENT = "Engagement"
    POLICY = "Policy"
    EXCEPTION = "Exception"
    CONTROL = "Control"
    EVIDENCE_TASK = "Evidence Task"
    RISK = "Risk"
    PROJECT = "Project"
    MODEL = "AI Model"
    DATASET = "Dataset"

    @classmethod
    def from_value(cls, value):
        """
        Returns the corresponding enum member from the given value.

        :param value: The string representation of the enum value.
        :return: The corresponding EntityType member.
        :raises ValueError: If the value does not correspond to any EntityType.
        """
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"'{value}' is not a valid {cls.__name__} value.")

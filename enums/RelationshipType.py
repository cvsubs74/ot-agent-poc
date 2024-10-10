from enum import Enum


class RelationshipType(Enum):
    DATA_TRANSFER = 'Data Transfer'
    SALE_OF_DATA = 'Sale of Data'
    RELATED = 'Related'
    PRODUCT_OR_SERVICE_PROVIDER = 'Product or Service Provider'
    CONTROLLER = 'Controller'
    JOINT_CONTROLLER = 'Joint Controller'
    PROCESSOR = 'Processor'
    SUB_PROCESSOR = 'Sub Processor'
    POLICY_GOVERNED = 'Policy Governed'
    CONTROL_IMPLEMENTED = 'Control Implemented'
    RISK_ASSOCIATED = 'Risk Associated'
    EVIDENCE_PROVIDED = 'Evidence Provided'
    PROJECT_SUPPORTS = 'Project Supports'
    MANAGES = 'Manages'
    MAINTAINS = 'Maintains'
    WORKS_ON = 'Works On'
    USES = 'Uses'
    COVERS = 'Covers'
    SUPPORTS = 'Supports'

    @classmethod
    def from_value(cls, value):
        """
        Returns the corresponding enum member from the given value.

        :param value: The string representation of the enum value.
        :return: The corresponding RelationshipType member.
        :raises ValueError: If the value does not correspond to any RelationshipType.
        """
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"'{value}' is not a valid {cls.__name__} value.")

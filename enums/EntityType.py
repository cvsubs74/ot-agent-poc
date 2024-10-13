from enum import Enum


class EntityType(Enum):
    VENDOR = {
        "label": 'Vendor',
        "actions": [
            {
                "action_name": "Terminate Contract",
                "api_endpoint": "/vendor/terminate_contract",
                "description": "Terminate the contract with the vendor due to risk or policy violation."
            },
            {
                "action_name": "Request Vendor Audit",
                "api_endpoint": "/vendor/request_audit",
                "description": "Initiate an audit for the vendor to ensure compliance with contractual obligations."
            },
            {
                "action_name": "Review Vendor Risk",
                "api_endpoint": "/vendor/review_risk",
                "description": "Conduct a risk assessment to evaluate the vendor’s risk exposure."
            }
        ]
    }
    ASSET = {
        "label": 'Asset',
        "actions": [
            {
                "action_name": "Tag Asset as Critical",
                "api_endpoint": "/asset/tag_critical",
                "description": "Mark this asset as critical for enhanced monitoring and control."
            },
            {
                "action_name": "Run Asset Compliance Check",
                "api_endpoint": "/asset/compliance_check",
                "description": "Perform a compliance check on the asset to ensure it meets necessary security and privacy standards."
            },
            {
                "action_name": "Monitor Asset Usage",
                "api_endpoint": "/asset/monitor_usage",
                "description": "Monitor the usage of this asset to detect any anomalies."
            }
        ]
    }
    ENTITY = {
        "label": 'Entity',
        "actions": [
            {
                "action_name": "Review Entity Access",
                "api_endpoint": "/entity/review_access",
                "description": "Review access levels and permissions for this entity."
            },
            {
                "action_name": "Deactivate Entity",
                "api_endpoint": "/entity/deactivate",
                "description": "Deactivate this entity to restrict further access and operations."
            }
        ]
    }
    PROCESSING_ACTIVITY = {
        "label": 'Processing Activity',
        "actions": [
            {
                "action_name": "Initiate Data Minimization",
                "api_endpoint": "/processing_activity/data_minimization",
                "description": "Reduce the data processed in this activity to the minimum necessary for its purpose."
            },
            {
                "action_name": "Review Data Retention",
                "api_endpoint": "/processing_activity/review_retention",
                "description": "Evaluate the data retention policy for this activity to ensure compliance with regulations."
            }
        ]
    }
    CONTRACT = {
        "label": 'Contract',
        "actions": [
            {
                "action_name": "Amend Contract",
                "api_endpoint": "/contract/amend",
                "description": "Propose changes or amendments to the existing contract."
            },
            {
                "action_name": "Review Contract Terms",
                "api_endpoint": "/contract/review_terms",
                "description": "Review the current terms of the contract for compliance and risks."
            }
        ]
    }
    ENGAGEMENT = {
        "label": 'Engagement',
        "actions": [
            {
                "action_name": "End Engagement",
                "api_endpoint": "/engagement/end",
                "description": "End the engagement due to non-compliance or completion of terms."
            },
            {
                "action_name": "Assess Engagement Risks",
                "api_endpoint": "/engagement/assess_risk",
                "description": "Conduct a risk assessment for the current engagement."
            }
        ]
    }
    POLICY = {
        "label": 'Policy',
        "actions": [
            {
                "action_name": "Review Policy Compliance",
                "api_endpoint": "/policy/review_compliance",
                "description": "Review compliance with the policy across entities and assets."
            },
            {
                "action_name": "Amend Policy",
                "api_endpoint": "/policy/amend",
                "description": "Propose changes to the policy to address new risks or regulatory changes."
            }
        ]
    }
    EXCEPTION = {
        "label": 'Exception',
        "actions": [
            {
                "action_name": "Resolve Exception",
                "api_endpoint": "/exception/resolve",
                "description": "Resolve the exception by taking appropriate mitigation actions."
            },
            {
                "action_name": "Escalate Exception",
                "api_endpoint": "/exception/escalate",
                "description": "Escalate the exception for further review by senior management."
            }
        ]
    }
    CONTROL = {
        "label": 'Control',
        "actions": [
            {
                "action_name": "Review Control Effectiveness",
                "api_endpoint": "/control/review_effectiveness",
                "description": "Review how effective the control is in mitigating risks."
            },
            {
                "action_name": "Modify Control",
                "api_endpoint": "/control/modify",
                "description": "Modify the control to address new or emerging risks."
            }
        ]
    }
    EVIDENCE_TASK = {
        "label": 'Evidence Task',
        "actions": [
            {
                "action_name": "Submit Evidence",
                "api_endpoint": "/evidence_task/submit",
                "description": "Submit evidence for an audit or compliance task."
            },
            {
                "action_name": "Request Evidence Review",
                "api_endpoint": "/evidence_task/request_review",
                "description": "Request a review of the evidence submitted."
            }
        ]
    }
    RISK = {
        "label": 'Risk',
        "actions": [
            {
                "action_name": "Mitigate Risk",
                "api_endpoint": "/risk/mitigate",
                "description": "Initiate risk mitigation actions to reduce the risk level."
            },
            {
                "action_name": "Review Risk Impact",
                "api_endpoint": "/risk/review_impact",
                "description": "Review the impact and likelihood of the risk."
            }
        ]
    }
    PROJECT = {
        "label": "Project",
        "actions": [
            {
                "action_name": "End Project",
                "api_endpoint": "/project/end",
                "description": "End the project if objectives are met or if it's no longer viable."
            },
            {
                "action_name": "Evaluate Project Risks",
                "api_endpoint": "/project/evaluate_risks",
                "description": "Evaluate risks associated with the project and propose mitigation."
            }
        ]
    }
    MODEL = {
        "label": 'AI Model',
        "actions": [
            {
                "action_name": "Do Bias Scan",
                "api_endpoint": "/model/do_bias_scan",
                "description": "Initiate a bias scan on the AI model to assess fairness and ethical considerations."
            },
            {
                "action_name": "Review Model Risk",
                "api_endpoint": "/model/review_risk",
                "description": "Evaluate the model's privacy risk and compliance with regulations."
            },
            {
                "action_name": "Assess Model Impact",
                "api_endpoint": "/model/assess_impact",
                "description": "Assess the overall impact of the model in the context of risk and privacy."
            }
        ]
    }
    DATASET = {
        "label": 'Dataset',
        "actions": [
            {
                "action_name": "Review Dataset Privacy Risk",
                "api_endpoint": "/dataset/review_privacy_risk",
                "description": "Evaluate the dataset for privacy risks, including personal data exposure and sensitive information handling."
            },
            {
                "action_name": "Ensure Data Integrity",
                "api_endpoint": "/dataset/ensure_integrity",
                "description": "Check the dataset for integrity issues such as missing, corrupt, or inaccurate data."
            },
            {
                "action_name": "Review Dataset Compliance",
                "api_endpoint": "/dataset/review_compliance",
                "description": "Assess whether the dataset complies with relevant data privacy regulations such as GDPR or CCPA."
            }
        ]
    }

    @classmethod
    def from_value(cls, value):
        """
        Returns the corresponding enum member from the given value.

        :param value: The string representation of the enum value.
        :return: The corresponding EntityType member.
        :raises ValueError: If the value does not correspond to any EntityType.
        """
        for item in cls:
            if item.value["label"] == value:
                return item
        raise ValueError(f"'{value}' is not a valid {cls.__name__} value.")

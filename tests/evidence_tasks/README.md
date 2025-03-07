# Evidence Tasks Test Data

This directory contains sample test data for validating the EvidenceValidator component. Each subdirectory represents a different evidence task with corresponding test files.

## Directory Structure

```
evidence_tasks/
├── task1_security_policy/
│   ├── valid_security_policy.pdf     # Complete policy document
│   └── incomplete_policy.doc         # Policy missing key sections
├── task2_access_review/
│   ├── access_review_report.xlsx     # Complete review with signatures
│   └── user_access_logs.csv          # Raw logs without review
└── task3_incident_response/
    ├── incident_report.pdf           # Full incident report
    └── response_screenshots/         # Supporting screenshots
```

## Test Cases

### Task 1: Security Policy Review
**Description:** Validate the organization's security policy document. The policy should include sections on access control, data protection, incident response, and acceptable use policies.

**Test Files:**
- `valid_security_policy.pdf`: A complete policy document containing all required sections
- `incomplete_policy.doc`: A policy document missing key required sections

### Task 2: Access Review Documentation
**Description:** Provide quarterly access review reports showing user access levels, review dates, and approver signatures. The report should include all system users and their current permission levels.

**Test Files:**
- `access_review_report.xlsx`: Complete quarterly review with all required signatures
- `user_access_logs.csv`: Raw access logs without formal review documentation

### Task 3: Incident Response Documentation
**Description:** Submit evidence of incident response procedures being followed during the latest security incident, including timeline, actions taken, and resolution steps.

**Test Files:**
- `incident_report.pdf`: Complete incident response report
- `response_screenshots/`: Directory containing supporting visual evidence

## Usage

Use these test files with the EvidenceValidator component to verify:
1. File type handling (PDF, DOC, XLSX, CSV, images)
2. Content validation against task descriptions
3. Error handling for incomplete or invalid evidence
4. Multi-file evidence validation scenarios

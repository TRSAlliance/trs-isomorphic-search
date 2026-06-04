# trs-isomorphic-search

**TRS Alliance Structural Truth Layer** — Mathematical verification that systems remain isomorphic to high-trust reference architectures.

## Overview

The TRS Isomorphic Search engine performs structural integrity verification by validating that system graphs maintain isomorphism to reference templates. This ensures systems conform to vetted architectural patterns and high-trust design principles.

## Installation

```bash
pip install trs-isomorphic-search
```

## Usage

### Command Line Interface

```bash
trs-iso validate --graph input_graph.json --template agent_lattice
```

### Exit Codes
- `0` = PASS (Residual Risk Score = 0.00)
- `1` = FAIL (Residual Risk Score = 1.00)

### Python API

```python
from trs_isomorphic_search.validator import validate_isomorphism
from trs_isomorphic_search.models import SystemGraph

# Load your graphs
input_graph = SystemGraph.model_validate_json(input_data)
template = SystemGraph.model_validate_json(template_data)

# Validate
report = validate_isomorphism(input_graph, template)
print(f"Status: {report.status}")
print(f"Risk Score: {report.residual_risk_score}")
```

## Project Structure

```
trs-isomorphic-search/
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
├── src/
│   └── trs_isomorphic_search/
│       ├── __init__.py
│       ├── cli.py
│       ├── models.py
│       ├── templates.py
│       ├── validator.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_validator.py
│   └── test_data/
│       ├── reference_agent_lattice.json
│       └── sample_workflow.json
├── examples/
│   └── example_usage.py
└── logs/                  # gitignore'd
```

## Dependencies

- **networkx** >= 3.3 - Graph algorithms and data structures
- **rustworkx** >= 0.16 - High-performance graph operations (VF2 isomorphism)
- **pydantic** >= 2.8 - Data validation and serialization
- **typer** >= 0.12 - CLI framework
- **rich** >= 13.7 - Rich terminal output

## How It Works

The system mathematically proves that a runtime graph is structurally identical to a trusted template by:

1. Accepting input system graphs and reference templates
2. Comparing node counts and edge counts
3. Using the VF2 isomorphism algorithm to validate structural equivalence
4. Generating a `ValidationReport` with pass/fail status and residual risk score

Node matching is performed on `layer_type` attributes. Edge matching is performed on `relation_type` attributes. This allows flexible node/edge naming while enforcing structural integrity.

## Templates

### agent_lattice (default)

Standard agent coordination pattern with feedback loop:
- **coordinator** (orchestration tier) → delegates to decision_engine
- **decision_engine** (logic tier) → directs execution_layer
- **execution_layer** (operations tier) → reports to monitoring_agent
- **monitoring_agent** (observation tier) → feeds back to coordinator

## Exit Codes

```bash
trs-iso validate --graph input.json
echo $?  # 0 = PASS, 1 = FAIL
```

## License

MIT

## Author

TRS Alliance

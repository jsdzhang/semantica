# Reasoning Module

Perform logical inference and reasoning on knowledge graphs using rule-based and deductive reasoning engines with support for forward/backward chaining.

## Overview

- **Rule-Based Reasoning**: Apply logical rules to derive new facts
- **Deductive Reasoning**: Infer conclusions from premises
- **Forward Chaining**: Data-driven reasoning
- **Backward Chaining**: Goal-driven reasoning
- **SWRL Support**: Semantic Web Rule Language

---

## Algorithms Used

### Inference Algorithms
- **Forward Chaining (Rete Algorithm)**: Efficient pattern matching, O(RFP) complexity where R=rules, F=facts, P=patterns
- **Backward Chaining**: Goal-directed reasoning with SLD resolution
- **Tableau Algorithm**: Description Logic reasoning
- **Resolution**: First-order logic inference

### Rule Matching
- **Rete Network**: Compiled rule network for efficient matching
- **Pattern Matching**: Unification algorithm for variable binding
- **Conflict Resolution**: Priority-based rule selection

---

## Main Classes

### InferenceEngine


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `forward_chain(kg, rules)` | Forward chaining inference | Rete algorithm |
| `backward_chain(kg, goal)` | Backward chaining | SLD resolution |
| `infer(kg, rules)` | General inference | Auto-select forward/backward |
| `apply_rules(facts, rules)` | Apply rule set | Pattern matching + unification |
| `explain_inference(fact)` | Explain derivation | Proof tree generation |

**Example:**

```python
from semantica.reasoning import InferenceEngine, RuleManager

engine = InferenceEngine(
    strategy="forward",  # forward, backward, hybrid
    max_iterations=100,
    explain_inferences=True
)

rule_manager = RuleManager()
rule_manager.add_rule(
    "IF ?x foundedBy ?y THEN ?y founder_of ?x"
)

# Forward chaining
new_facts = engine.forward_chain(kg, rule_manager)
print(f"Inferred {len(new_facts)} new facts")

# Explain inference
for fact in new_facts[:5]:
    explanation = engine.explain_inference(fact)
    print(f"{fact}: {explanation}")
```

---

### RuleManager


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `add_rule(rule)` | Add inference rule | Rule parsing + validation |
| `remove_rule(rule_id)` | Remove rule | Rule deletion |
| `load_rules(filename)` | Load rules from file | SWRL/custom format parsing |
| `validate_rules()` | Validate rule set | Consistency checking |
| `compile_rules()` | Compile to Rete network | Rete compilation |

**Rule Syntax:**
```
IF <condition> THEN <conclusion>

Examples:
IF ?x type Person AND ?x worksFor ?y THEN ?y employs ?x
IF ?x foundedBy ?y AND ?y type Person THEN ?x type Organization
```

**Example:**

```python
from semantica.reasoning import RuleManager

rules = RuleManager()

# Add rules
rules.add_rule("IF ?x type Company AND ?x foundedBy ?y THEN ?y founder_of ?x")
rules.add_rule("IF ?x founder_of ?y AND ?y type Company THEN ?x type Entrepreneur")

# Load from file
rules.load_rules("rules.swrl")

# Validate
is_valid, errors = rules.validate_rules()
```

---

### DeductiveReasoner


**Methods:**

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `reason(kg, axioms)` | Perform deductive reasoning | Tableau algorithm |
| `check_entailment(kg, statement)` | Check if statement is entailed | Subsumption testing |
| `find_inconsistencies(kg)` | Find logical contradictions | Consistency checking |
| `classify(kg)` | Compute class hierarchy | Classification algorithm |

---

## Configuration

```yaml
# config.yaml - Reasoning Configuration

reasoning:
  inference:
    strategy: forward  # forward, backward, hybrid
    max_iterations: 100
    explain_inferences: true
    
  rules:
    format: swrl  # swrl, custom
    validate_on_load: true
    
  deductive:
    reasoner: hermit  # hermit, pellet
    check_consistency: true
```

---

## See Also

- [Knowledge Graph Module](kg.md)
- [Ontology Module](ontology.md)

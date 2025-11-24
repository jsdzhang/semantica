# Contributing to Semantica

Thank you for your interest in contributing to Semantica! This guide provides detailed information about contributing to the project.

## Quick Links

- [Contributing Guide](../CONTRIBUTING.md) - Main contributing guide
- [Code of Conduct](../CODE_OF_CONDUCT.md) - Community standards
- [Security Policy](../SECURITY.md) - Security reporting
- [GitHub Discussions](https://github.com/Hawksight-AI/semantica/discussions) - Community discussions

## Documentation-Specific Guidelines

### Writing Documentation

When contributing documentation, please follow these guidelines:

#### Style Guide

- Use clear, concise language
- Write for a technical audience but explain complex concepts
- Include code examples where helpful
- Use proper markdown formatting
- Follow the existing documentation structure

#### Code Examples

- Always include working code examples
- Test examples before submitting
- Use realistic scenarios
- Include expected output when relevant
- Add comments for clarity

#### API Documentation

When documenting APIs:

- Include function/class signatures with type hints
- Document all parameters and return values
- Provide usage examples
- Note any exceptions that may be raised
- Include performance considerations if relevant

Example:

```python
def extract_entities(
    text: str,
    model: str = "transformer",
    confidence_threshold: float = 0.7
) -> List[Entity]:
    """Extract named entities from text.
    
    Args:
        text: Input text to process
        model: NER model to use (default: "transformer")
        confidence_threshold: Minimum confidence score (default: 0.7)
    
    Returns:
        List of extracted Entity objects
    
    Raises:
        ValueError: If text is empty or model is invalid
    
    Example:
        >>> from semantica.semantic_extract import NamedEntityRecognizer
        >>> ner = NamedEntityRecognizer()
        >>> entities = ner.extract("Apple Inc. was founded in 1976.")
        >>> len(entities)
        2
    """
```

### Documentation Structure

The documentation is organized as follows:

```
docs/
├── index.md              # Homepage
├── getting-started.md    # Getting started guide
├── concepts.md          # Core concepts
├── modules.md           # Module overview
├── use-cases.md         # Use case examples
├── examples.md          # Code examples
├── learning-more.md     # Additional resources
├── cookbook/            # Interactive tutorials
│   ├── introduction/   # Beginner tutorials
│   ├── advanced/        # Advanced tutorials
│   └── use_cases/       # Domain-specific examples
└── reference/           # API reference
    ├── core.md
    ├── ingest.md
    └── ...
```

### Adding New Documentation

1. **Choose the right location**:
   - Concepts → `concepts.md`
   - Tutorials → `cookbook/`
   - API docs → `reference/`
   - Examples → `examples.md` or `cookbook/`

2. **Follow naming conventions**:
   - Use lowercase with hyphens: `my-new-doc.md`
   - Be descriptive but concise

3. **Update navigation**:
   - Add to `mkdocs.yml` in the appropriate section

4. **Add to index if needed**:
   - Update `docs/index.md` if it's a major new section

### Code Review Process

Documentation PRs go through the same review process as code:

1. **Automated checks**:
   - Markdown linting
   - Link checking
   - Build verification

2. **Manual review**:
   - Accuracy and clarity
   - Code example correctness
   - Consistency with existing docs

3. **Feedback**:
   - Reviewers provide constructive feedback
   - Address all comments before merging

### Example Contributions

#### Fixing Typos

```markdown
# Before
Semantica is a knowlege graph framework.

# After
Semantica is a knowledge graph framework.
```

#### Improving Clarity

```markdown
# Before
The function does entity extraction.

# After
The function extracts named entities (people, organizations, locations, etc.) from text using advanced NLP models.
```

#### Adding Examples

```markdown
## Example

Here's how to extract entities from text:

```python
from semantica.semantic_extract import NamedEntityRecognizer

ner = NamedEntityRecognizer()
entities = ner.extract("Apple Inc. was founded by Steve Jobs.")
print(f"Found {len(entities)} entities")
```
```

### Translation

We welcome translations of the documentation! If you'd like to translate:

1. Create a new directory: `docs/i18n/<language>/`
2. Translate the markdown files
3. Update `mkdocs.yml` to include the new language
4. Maintain the same structure as the English version

### Documentation Tools

We use:

- **MkDocs**: Documentation generator
- **Material for MkDocs**: Theme
- **mkdocstrings**: API documentation from docstrings
- **Mermaid**: Diagrams

### Getting Help

If you need help with documentation:

- Ask in [GitHub Discussions](https://github.com/Hawksight-AI/semantica/discussions)
- Check existing documentation for examples
- Review other contributors' PRs

Thank you for helping improve Semantica's documentation! 📚


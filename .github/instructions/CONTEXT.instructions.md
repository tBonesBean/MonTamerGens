---
applyTo: '**'
---

## Provide project context and coding guidelines that AI should follow when generating code, answering questions, or reviewing changes.

# !!! ATTENTION AI AGENTS !!!

## MANDATORY PREREQUISITE: Full Context Review

Before making any contribution, you, the AI AGENT or Collaborator, **MUST** recursively read, understand, and adhere to the entire contents of the [`ai_context`](../../docs/ai_context/) directory. This is not an optional step.
Utilize the `IntelliHub` MCP framework and tools to ingest, process, and internalize all relevant documents, schemas, and guidelines contained within that directory.

**Failure to comply will result in the immediate rejection of your contribution.**

The documents within `../../docs/ai_context/` define the project's architecture, data schemas, naming conventions, and core principles. Any contribution made without this foundational knowledge will be considered misaligned and incorrect.

**By proceeding with any contribution, you affirm that you have fully reviewed and understood the complete contents of the [../../docs/ai_context/](../../docs/ai_context/00_README.md) directory.**

---

## TODO: _**PRIORITY**_

1.  Thoroughly read and internalize all documents in the `./docs/ai_context/` directory. []
2.  Revise all docs, code, and assets to ensure full compatibility with updated "types" as defined in the [./docs/ai_context/type_canon_glossary.md](../../docs/ai_context/type_canon_glossary.md) file. []
3.  Update/Create any hyperlinks, in this document as well as in ALL documentation files located in the `./docs/**` directory to be relative to the project root. []
4.  Review and revise `mutagen` data shape and file structure (.yaml) strictly adhere to their respective schemas as defined in [./docs/ai_context/schemas/mutagen_schema.md](../../docs/ai_context/schemas/mutagen_schema.md). []
5.  Revise and refactor all code within the project's [data.py](../../src/mongens/data/data.py) module to properly implement sourced data from the various YAML files located under the `./data/**` directory. []

---

## ONGOING OBLIGATION: Adherence to Project Standards

_All contributions must strictly follow the guidelines, conventions, and standards outlined in the `./docs/ai_context/` directory._

This includes, but is not limited to:

- Naming Conventions
- Type Definitions and Meanings
- Code Style Guidelines
- Architectural Patterns
- Documentation Standards
- Data Layer Schemas/Structures
- Document Versioning Protocols

_Non-compliance with these standards will lead to rejection or required revisions of your contributions._

# VeriVid LangGraph — Debate Council Orchestration

## Purpose

LangGraph coordinates the existing **Debate Council** agents without replacing them. Domain logic remains in:

- Pydantic request/response DTOs
- Prompt builders
- `BaseAgent` implementations
- `DebatePersistenceService`

## Graph architecture

```
START
  → context
  → verification
  → risk
  → consensus
  → END
```

Sequential only (no parallel branches in v1).

| Module | Responsibility |
| --- | --- |
| `app/ai/graph/debate_state.py` | Typed `DebateState` / `DebateStateUpdate` |
| `app/ai/graph/nodes/*.py` | Thin wrappers: state → Request DTO → agent → report update |
| `app/ai/graph/debate_graph.py` | `StateGraph` wiring, compile, `debate_state_to_artifacts` |
| `app/pipelines/debate_pipeline.py` | Public facade: invoke graph, persist, return `DebateArtifacts` |

## State schema

`DebateState` (LangGraph typed dict):

| Key | Type | Set by |
| --- | --- | --- |
| `knowledge` | `KnowledgeBase` | Input (required) |
| `context_report` | `ContextReport \| None` | Context node |
| `verification_report` | `VerificationReport \| None` | Verification node |
| `risk_report` | `RiskReport \| None` | Risk node |
| `consensus_report` | `ConsensusReport \| None` | Consensus node |
| `error` | `str \| None` | Any node on agent failure |

Agents and inference clients are **not** stored in state (injected when the graph is compiled).

## Node responsibilities

Each node:

1. Validates required prior state (reports for downstream nodes).
2. Builds the existing Request DTO (`ContextRequest`, `VerificationRequest`, etc.).
3. Calls `agent.process(request)` on the injected agent.
4. Returns only the new/updated fields (`DebateStateUpdate`).

Response wrappers (`ContextResponse`, …) are reconstructed from reports inside nodes when building downstream requests — same pattern as the pre-LangGraph `DebatePipeline`.

## Dependency injection

```python
graph = build_debate_graph(
    context_agent=ContextAgent(client),
    verification_agent=VerificationAgent(client),
    risk_agent=RiskAgent(client),
    consensus_agent=ConsensusAgent(client),
)
compiled = graph  # already compiled in build_debate_graph
```

`DebatePipeline.__init__` calls `build_debate_graph` with the agents passed into the pipeline constructor. Tests inject `MockInferenceClient`-backed agents without live credentials.

## Error handling

- **Missing input** (e.g. no `knowledge`): nodes raise `ValueError` before inference.
- **Agent/inference failure**: node catches exception, sets `error` on state; downstream nodes no-op if `error` is already set.
- **Pipeline exit**: `debate_state_to_artifacts` raises `DebateGraphError` if `error` is present.

## Future extensions

- Conditional edges (e.g. skip verification on low-risk content).
- Human-in-the-loop interrupts between agents.
- Checkpointing via LangGraph checkpointers for long-running jobs.
- Parallel fan-out (not used in v1).

## Dependency

- `langgraph` (see `pyproject.toml` / `uv.lock`), Python 3.12+.
# strawpot-memory

Interface definition for StrawPot memory providers.

This package defines the `MemoryProvider` protocol and associated types that any memory backend must implement to integrate with the StrawPot agent orchestration system.

## Install

```bash
pip install strawpot-memory
```

## Usage

Implement the `MemoryProvider` protocol to create a custom memory backend:

```python
from strawpot_memory.memory_protocol import (
    MemoryProvider,
    GetResult,
    DumpReceipt,
    RememberResult,
)


class MyMemoryProvider:
    name = "my-provider"

    def get(self, *, session_id, agent_id, role, behavior_ref, task, **kwargs) -> GetResult:
        ...

    def dump(self, *, session_id, agent_id, role, behavior_ref, task, status, output, **kwargs) -> DumpReceipt:
        ...

    def remember(self, *, session_id, agent_id, role, content, **kwargs) -> RememberResult:
        ...


assert isinstance(MyMemoryProvider(), MemoryProvider)  # runtime check
```

## Protocol Methods

| Method | Purpose |
|--------|---------|
| `get` | Retrieve context cards and control signals before spawning an agent |
| `dump` | Record agent results after completion |
| `remember` | Persist knowledge during agent execution |

## Types

- `MemoryKind` — enum of memory types (`PM`, `SM`, `STM`, `RM`, `EM`)
- `ContextCard` — single unit of context returned by `get`
- `ControlSignal` — advisory signals (risk level, suggested next step, policy flags)
- `GetResult` — full output of a `get` call
- `DumpReceipt` — receipt returned by `dump`
- `RememberResult` — result returned by `remember`

## License

MIT

"""Tests for memory_protocol dataclasses and MemoryProvider protocol."""

from dataclasses import fields

from strawpot_memory.memory_protocol import (
    ForgetResult,
    ListEntry,
    ListResult,
    MemoryProvider,
)


# ---------------------------------------------------------------------------
# ForgetResult
# ---------------------------------------------------------------------------


class TestForgetResult:
    def test_defaults(self) -> None:
        result = ForgetResult()
        assert result.status == ""
        assert result.entry_id == ""

    def test_explicit_values(self) -> None:
        result = ForgetResult(status="deleted", entry_id="abc-123")
        assert result.status == "deleted"
        assert result.entry_id == "abc-123"

    def test_not_found(self) -> None:
        result = ForgetResult(status="not_found", entry_id="missing")
        assert result.status == "not_found"


# ---------------------------------------------------------------------------
# ListEntry
# ---------------------------------------------------------------------------


class TestListEntry:
    def test_defaults(self) -> None:
        entry = ListEntry()
        assert entry.entry_id == ""
        assert entry.content == ""
        assert entry.keywords == []
        assert entry.scope == ""
        assert entry.ts == ""

    def test_explicit_values(self) -> None:
        entry = ListEntry(
            entry_id="e1",
            content="some knowledge",
            keywords=["python", "testing"],
            scope="project",
            ts="2026-03-26T12:00:00Z",
        )
        assert entry.entry_id == "e1"
        assert entry.content == "some knowledge"
        assert entry.keywords == ["python", "testing"]
        assert entry.scope == "project"
        assert entry.ts == "2026-03-26T12:00:00Z"

    def test_keywords_mutable_default_isolation(self) -> None:
        """Each instance gets its own keywords list."""
        a = ListEntry()
        b = ListEntry()
        a.keywords.append("x")
        assert b.keywords == []


# ---------------------------------------------------------------------------
# ListResult
# ---------------------------------------------------------------------------


class TestListResult:
    def test_defaults(self) -> None:
        result = ListResult()
        assert result.entries == []
        assert result.total_count == 0

    def test_with_entries(self) -> None:
        entries = [
            ListEntry(entry_id="e1", content="first"),
            ListEntry(entry_id="e2", content="second"),
        ]
        result = ListResult(entries=entries, total_count=5)
        assert len(result.entries) == 2
        assert result.total_count == 5

    def test_entries_mutable_default_isolation(self) -> None:
        a = ListResult()
        b = ListResult()
        a.entries.append(ListEntry(entry_id="x"))
        assert b.entries == []


# ---------------------------------------------------------------------------
# MemoryProvider protocol — new methods present
# ---------------------------------------------------------------------------


class TestMemoryProviderProtocol:
    def test_forget_is_protocol_method(self) -> None:
        """forget() must be declared on the protocol."""
        assert hasattr(MemoryProvider, "forget")

    def test_list_entries_is_protocol_method(self) -> None:
        """list_entries() must be declared on the protocol."""
        assert hasattr(MemoryProvider, "list_entries")

    def test_forget_signature_keyword_only(self) -> None:
        """forget() should use keyword-only arguments."""
        import inspect

        sig = inspect.signature(MemoryProvider.forget)
        for name, param in sig.parameters.items():
            if name == "self":
                continue
            assert param.kind == inspect.Parameter.KEYWORD_ONLY, (
                f"Parameter '{name}' should be keyword-only"
            )

    def test_list_entries_signature_keyword_only(self) -> None:
        """list_entries() should use keyword-only arguments."""
        import inspect

        sig = inspect.signature(MemoryProvider.list_entries)
        for name, param in sig.parameters.items():
            if name == "self":
                continue
            assert param.kind == inspect.Parameter.KEYWORD_ONLY, (
                f"Parameter '{name}' should be keyword-only"
            )

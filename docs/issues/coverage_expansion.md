# Issue: Expand Test Coverage

**Status**: Backlog
**Created**: 2025-12-08
**Priority**: Medium

## Objective
Increase test coverage from ~78% to >90%, focusing on integration tests and edge cases that require mocking external dependencies or complex data structures.

## Tasks
- [ ] **Load Module**: Add tests for `quail.load` (loading from .mat, .json, CAAN datasets).
    - Requires mocking filesystem and potentially `scipy.io.loadmat`.
- [ ] **Plot Module**: Increase coverage for `plot.py` beyond basic smoke tests.
    - Verify plot content (ax limits, labels) more rigorously.
- [ ] **Decode Speech**: Refactor and test `decode_speech.py` (currently low coverage).
    - Mock Whisper API / local model.
- [ ] **LagCRP**: Add edge case tests for `lagcrp.py` (short lists, repeats).

## Notes
- Current coverage (78%) is considered stable for core functionality (`egg`, `clustering`).
- `lagcrp` optimization (Phase 5) might change the implementation, so tests should be added after that.

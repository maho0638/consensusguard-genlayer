# Preliminary full-suite attempt: temporary SDK cache missing

This attempt was not a test result. The final suite was rerun after restoring
the pinned archive.

- Preliminary outcome: 63 failed, 3 passed, 1 skipped.
- The failing tests stopped during GenLayer Testing Suite SDK path setup, before
  contract assertions, because its cached `v0.6.0-rc9` artifact was absent.
- The sandbox denied the SDK loader's network socket (`PermissionError: [Errno
  1] Operation not permitted`). The Direct Mode bundle had been in a temporary
  cache in an earlier run; it was no longer present.
- The official `v0.6.0-rc9` release asset was restored once and matched SHA-256
  `d3c6ba368dbd5cad01e484e19573906b4ffed41f46a48191bdc579c81cf801af`.
- The subsequent standalone full run is captured in `pytest.log`: 66 passed,
  1 skipped.

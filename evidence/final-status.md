# Final status evidence (2026-10-12)

- Local baseline before the final URL hardening change: 66 passed, 1 skipped. The final full run is captured in `evidence/final-local-tests.log` and supersedes this baseline count.
- Studio Dev: contract deployed at `0xBa84783D71d902c8BD3Ba63418Df172280249139`; `resolve(0)` transaction `0x26812cb24903f30c20dd07dc9de515d911eee98248eeed0c376175c36797a4b9` is `FINALIZED`, accepted. Explorer says five initial validators; votes are 3 agree and 2 idle. Stored decision read-back is `VERIFIED`, with two matching expected/observed hashes and two SUPPORTS labels.
- One earlier `open_case` transaction finalized but contract execution failed with duplicate source host; corrected operation succeeded. Failure is retained in `evidence/studio-dev-live-validation.md`.
- Explorer reports approximately 0.000097 GEN resolve fee. The Studio wallet UI's rounded `0 GEN` display is not evidence of no fee.
- Local opt-in Studio multi-validator integration remains skipped because the workspace has no local GenLayer node. Public testnet deployment was not performed. No Portal submission was made; Portal-ready status is pending outside assessment.
- GitHub publication and Actions status are to be recorded after the repository write and workflow run. No deployment beyond the evidenced Studio Dev contract is implied.

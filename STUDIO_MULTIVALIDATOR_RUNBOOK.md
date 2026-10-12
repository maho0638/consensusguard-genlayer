# Local Studio multi-validator integration runbook

This runbook executes the opt-in `tests/test_studio_multivalidator.py` test
against a local GenLayer Studio network. It uses five configured mock
validators and mocked HTTP/LLM results. It submits localnet deployment and
write transactions only; it does not use Studionet/testnet or GEN with real
value.

## Requirements

- Python 3.12 or newer.
- Node.js and npm.
- Docker Desktop running with Linux containers enabled.
- Enough memory/disk for the current GenLayer localnet. Check GenLayer's
  current setup guide for hardware and version requirements.

GenLayer's current CLI documentation describes `npm install -g genlayer`,
`genlayer init`, and `genlayer up --numValidators 5` for the local environment.
`genlayer init` defaults to five validators. Use the official documentation
links in `README.md` if those commands change.

## Windows PowerShell: prepare local Studio

From the project directory:

```powershell
npm install -g genlayer
genlayer init --numValidators 5
```

If initialization completes without leaving the localnet running, start it:

```powershell
genlayer up --numValidators 5
```

Keep the Studio/localnet process running. Confirm Docker is active:

```powershell
docker ps
```

The project `gltest.config.yaml` targets `http://127.0.0.1:4000/api` and has
`leader_only: false`. Do not pass `--leader-only`: it disables consensus and
would invalidate this test.

## Install project test tools

In a second PowerShell window, from the project directory:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-lock.txt
```

If PowerShell blocks venv activation, use Command Prompt and run
`.venv\Scripts\activate.bat` instead.

## Run the real Studio test

PowerShell:

```powershell
$env:CONSENSUSGUARD_RUN_STUDIO = "1"
gltest tests/test_studio_multivalidator.py -v -s --network localnet
```

Command Prompt:

```bat
set CONSENSUSGUARD_RUN_STUDIO=1
gltest tests/test_studio_multivalidator.py -v -s --network localnet
```

The contract and Direct Mode use the exact runner/SDK pair in `vendor/`; do
not override it with a different runner. This test deploys to the localnet
and sends write transactions. Obtain explicit user approval before running it.

The test deploys the contract to the local network, opens one case, then
resolves it with a five-validator transaction context. It does not contact a
live evidence host or paid model: every validator receives the exact same
mocked response bodies and JSON classification.

## Expected result

The test passes only if both localnet writes succeed and the contract state
contains one `DECIDED` case with a `VERIFIED` decision, two verified sources,
and two supporting labels. A successful result is evidence for this local
Studio configuration and contract version; it is not evidence of public
testnet deployment or consensus among live public validators.

The transaction receipt is passed to `tx_execution_succeeded`; the test also
reads back `get_case` and `get_latest_decision`. Preserve the full terminal
output and transaction IDs when reporting the run. A skipped test is not a
pass. If Studio reports an undetermined/failed transaction, record that
outcome and inspect the local node/validator logs before changing the test.

## Offline/default test behavior

The Studio integration is skipped unless `CONSENSUSGUARD_RUN_STUDIO=1` is set.
The normal suite remains:

```powershell
python -m compileall -q contracts tests
pytest -q
```

No public network, testnet, Portal, GitHub write, or paid call is required for
this local runbook.

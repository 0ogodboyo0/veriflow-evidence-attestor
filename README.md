# VeriFlow Evidence Attestor

VeriFlow Evidence Attestor is an **independent GenLayer Intelligent Contract** for consensus review of public collateral-evidence pages. It is designed as a reusable review primitive for collateral-backed lending, treasury, or verification workflows that need a shared decision about public evidence rather than a single operator’s judgment.

The project is inspired by common design challenges in collateralized finance—evidence quality, revocation signals, and transparent decision records—but it does **not** modify, depend on, integrate with, or claim affiliation with any other repository or product.

> This is a non-binding public-evidence review tool. It does not provide legal, investment, KYC, AML, sanctions, ownership, or valuation determinations. It must not be used as the sole basis for lending, transfers, or real-world claims.

## Problem

Traditional smart contracts can enforce numeric rules, but cannot independently assess whether a public evidence page is sufficiently specific, current, internally consistent, and connected to a stated subject. A centralized reviewer can make that call, but counterparties must trust that reviewer.

VeriFlow puts the consensus-critical part on GenLayer. Multiple validators independently retrieve the same public HTTPS evidence page, apply the same policy, and accept a structured result only when they agree on the decision.

## Structured decision

| Decision | Meaning |
|---|---|
| `VERIFIED` | The public page supports the stated policy with concrete, internally consistent facts and no material contradiction. |
| `INSUFFICIENT_EVIDENCE` | The page is missing required information, is vague, stale, inaccessible, or cannot be connected to the subject. |
| `REJECTED` | The page includes a material contradiction, clear revocation, or strong evidence that the policy is not satisfied. |

## How the contract reaches consensus

`review_public_collateral_evidence(subject, evidence_url)` runs a non-deterministic evaluation function. The leader and validators each fetch the public page independently and request a JSON response containing a decision, confidence score, and brief reason. Validators accept the leader result only if the independent decision matches and confidence differs by no more than 15 points.

Only the agreed decision, confidence, concise reason, subject, and URL are stored. The free-text rationale is not used as the consensus-critical field because reasonable model outputs can differ in wording. This follows GenLayer’s pattern of comparing stable structured decisions rather than unconstrained text.[1] [2]

## Public interface

| Method | Type | Purpose |
|---|---|---|
| `set_review_policy(review_policy)` | write | Changes the policy; callable only by the contract owner. |
| `review_public_collateral_evidence(subject, evidence_url)` | write | Performs independent public-evidence review and persists the accepted result. |
| `get_latest_review()` | view | Reads the latest review record and counter. |

## Deploy in GenLayer Studio

Open [GenLayer Studio](https://studio.genlayer.com), create a contract, paste `VeriFlowEvidenceAttestor.py`, and deploy with this constructor policy:

```text
Accept only public evidence that identifies the collateral asset or issuer, provides a verifiable date or document reference, links the evidence to the stated subject, and contains no explicit revocation or material contradiction. Return INSUFFICIENT_EVIDENCE when any required element is unavailable, ambiguous, stale, or not publicly verifiable.
```

After the project is pushed to a public repository, use the raw URL of `demo_evidence.md` as an execution input. Record the deployed address, execution reference, and readback state in `DEPLOYMENT.md`. A Studio deployment must be accurately described as a sandbox/Studio deployment, not as a production deployment.

## Validation

The current contract source passed the official linter:

```text
genvm-lint check VeriFlowEvidenceAttestor.py
Lint passed (3 checks)
Validation passed
Contract: VeriFlowEvidenceAttestor
Methods: 3 (1 view, 2 write)
```

## References

[1]: https://docs.genlayer.com/developers/intelligent-contracts/when-to-use-genlayer "When to Use GenLayer"
[2]: https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle "The Equivalence Principle"
[3]: https://docs.genlayer.com/developers/intelligent-contracts/crafting-prompts "Prompt & Data Techniques"

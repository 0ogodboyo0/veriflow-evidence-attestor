# Deployment Record — VeriFlow Evidence Attestor

> Complete this document only after a successful deployment and execution. Do not enter invented addresses, transaction hashes, or results.

| Field | Value |
|---|---|
| Environment | `PENDING_DEPLOYMENT` |
| Contract address | `PENDING_DEPLOYMENT` |
| Deployment reference | `PENDING_DEPLOYMENT` |
| Deployment date (UTC) | `PENDING_DEPLOYMENT` |

## Constructor policy

```text
Accept only public evidence that identifies the collateral asset or issuer, provides a verifiable date or document reference, links the evidence to the stated subject, and contains no explicit revocation or material contradiction. Return INSUFFICIENT_EVIDENCE when any required element is unavailable, ambiguous, stale, or not publicly verifiable.
```

## Demonstration transaction

| Field | Value |
|---|---|
| Method | `review_public_collateral_evidence` |
| Subject | `veriflow-demo-subject-001` |
| Evidence URL | `https://raw.githubusercontent.com/0ogodboyo0/veriflow-evidence-attestor/main/demo_evidence.md` |
| Expected decision | `VERIFIED` |
| Actual decision | `PENDING_EXECUTION` |
| Execution / consensus reference | `PENDING_EXECUTION` |

## Readback check

After the transaction finalizes, call `get_latest_review()` and paste the exact result here. It should identify the demo subject and the evidence URL, include a `VERIFIED` decision, a confidence value, a concise reason, and `review_count` equal to `1`.

## Scope statement

This deployment demonstrates a public-evidence review primitive. It does not perform token transfers, KYC/AML checks, legal adjudication, lending, liquidation, ownership confirmation, valuation, or contract-to-contract calls.

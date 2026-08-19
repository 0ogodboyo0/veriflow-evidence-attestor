# Deployment Record — VeriFlow Evidence Attestor

## Deployment

| Field | Value |
|---|---|
| Environment | `GenLayer Studio` |
| Contract | `VeriFlowEvidenceAttestor v2` |
| Contract address | [`0xcDCA93809595C12Ca887269F6f13FB05723FA6A3`](https://explorer-studio.genlayer.com/address/0xcDCA93809595C12Ca887269F6f13FB05723FA6A3) |
| Deployment transaction | [`0xdeca34c451b565613a77480883a3e2be20c8b1dec9546d353fb6cf7da088f8cb`](https://explorer-studio.genlayer.com/tx/0xdeca34c451b565613a77480883a3e2be20c8b1dec9546d353fb6cf7da088f8cb) |
| Created at | `2026-08-19 5:12:03 PM` (as displayed in Explorer) |
| Deployment status | `FINALIZED` |
| GenVM result | `SUCCESS` |
| Consensus result | `Accepted` |

The deployed v2 contract keeps its review policy in code, rather than depending on a constructor storage value. The source was linted and validated with `genvm-lint` before deployment.

## Public evidence input

| Field | Value |
|---|---|
| Method | `review_public_collateral_evidence` |
| Subject | `veriflow-demo-subject-001` |
| Evidence URL | `https://raw.githubusercontent.com/0ogodboyo0/veriflow-evidence-attestor/main/demo_evidence.md` |

## Accepted consensus review — VERIFIED

| Field | Value |
|---|---|
| Transaction | [`0x4a76288dd62796799dd601370edeccd3973dab7713e7215b81ab0b70d5e8086e`](https://explorer-studio.genlayer.com/tx/0x4a76288dd62796799dd601370edeccd3973dab7713e7215b81ab0b70d5e8086e) |
| Created at | `2026-08-19 5:15:06 PM` (as displayed in Explorer) |
| Status | `FINALIZED` |
| GenVM result | `SUCCESS` |
| Consensus result | `Accepted` |
| Return value | `VERIFIED` |
| Confidence | `100` |
| Reason | The source identified the subject, issuer, asset ID, document reference `VF-2026-001`, date `2026-08-19`, and an active status without revocation. |

## Subsequent conservative review — INSUFFICIENT_EVIDENCE

A later run against the same public demonstration source was also technically successful and accepted by consensus, but returned `INSUFFICIENT_EVIDENCE` with confidence `95`. The validators treated the source’s explicit synthetic/test demonstration disclaimer as insufficient proof of a real-world collateral record.

| Field | Value |
|---|---|
| Transaction | [`0x74fc33e6d5262dd29418b153a4c40cd04996a8cea47a4bbf41157cd255525bfe`](https://explorer-studio.genlayer.com/tx/0x74fc33e6d5262dd29418b153a4c40cd04996a8cea47a4bbf41157cd255525bfe) |
| Status | `FINALIZED` |
| GenVM result | `SUCCESS` |
| Consensus result | `Accepted` |
| Return value | `INSUFFICIENT_EVIDENCE` |
| Confidence | `95` |

> Both records are retained for transparency. The verified transaction demonstrates a complete accepted consensus review, while the later conservative result illustrates why public-evidence policies and disclaimers must be designed carefully.

## Scope and limitations

This is a GenLayer Studio sandbox deployment of an independent public-evidence review primitive. It does not perform token transfers, KYC/AML checks, legal adjudication, ownership confirmation, valuation, lending, liquidation, or contract-to-contract calls. The public source is synthetic and is not a real-world asset or collateral record.

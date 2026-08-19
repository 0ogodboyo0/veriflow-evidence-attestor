# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

"""
VeriFlow Evidence Attestor v2

An independent GenLayer Intelligent Contract for consensus review of public
collateral-evidence pages. This version keeps its review policy in code so a
Studio deployment does not depend on a constructor storage value.
"""

from genlayer import *


class VeriFlowEvidenceAttestor(gl.Contract):
    latest_subject: str
    latest_evidence_url: str
    latest_decision: str
    latest_confidence: u64
    latest_reason: str
    review_count: u64

    def __init__(self):
        self.latest_subject = ""
        self.latest_evidence_url = ""
        self.latest_decision = "UNREVIEWED"
        self.latest_confidence = u64(0)
        self.latest_reason = "No evidence has been reviewed."
        self.review_count = u64(0)

    @gl.public.write
    def review_public_collateral_evidence(self, subject: str, evidence_url: str) -> str:
        """Review an HTTPS public evidence page through validator consensus."""
        if len(subject.strip()) < 4:
            raise gl.vm.UserError("Subject identifier is required")
        if not evidence_url.startswith("https://"):
            raise gl.vm.UserError("Evidence URL must use HTTPS")

        policy = (
            "Accept only public evidence that identifies the collateral asset or issuer, "
            "provides a verifiable date or document reference, links the evidence to the "
            "stated subject, and contains no explicit revocation or material contradiction. "
            "Return INSUFFICIENT_EVIDENCE when any required element is unavailable, "
            "ambiguous, stale, or not publicly verifiable."
        )

        def evaluate_evidence():
            response = gl.nondet.web.get(evidence_url)
            evidence_text = response.body.decode("utf-8")[:12000]

            prompt = f"""
You are an evidence reviewer for a collateral-backed finance workflow.
You are not providing legal, investment, KYC, AML, sanctions, ownership, or
valuation advice.

Assess only whether this public evidence page supplies sufficient, internally
consistent evidence to support a non-binding collateral-attestation review.

Subject identifier: {subject}

Review policy:
{policy}

Public evidence page:
<evidence>
{evidence_text}
</evidence>

Use these rules:
1. Return VERIFIED only when the page directly supports the policy with concrete,
   internally consistent facts and no material contradiction.
2. Return INSUFFICIENT_EVIDENCE when information is missing, vague, inaccessible,
   stale, or cannot be connected to the stated subject.
3. Return REJECTED only when the page contains a clear material contradiction,
   explicit revocation, or strong evidence that the policy is not satisfied.
4. Never infer private KYC, AML, sanctions, accreditation, legal ownership, or
   real-world value from incomplete public information.
5. Keep the reason factual, source-grounded, and no more than 240 characters.

Return JSON exactly matching this schema:
{{
  "decision": "VERIFIED" | "INSUFFICIENT_EVIDENCE" | "REJECTED",
  "confidence": integer from 0 to 100,
  "reason": "brief source-grounded reason"
}}
"""
            result = gl.nondet.exec_prompt(prompt, response_format="json")

            decision = result.get("decision", "")
            confidence = result.get("confidence", -1)
            reason = result.get("reason", "").strip()

            if decision not in ["VERIFIED", "INSUFFICIENT_EVIDENCE", "REJECTED"]:
                raise gl.vm.UserError("Invalid decision returned by evidence review")
            if not isinstance(confidence, int) or confidence < 0 or confidence > 100:
                raise gl.vm.UserError("Invalid confidence returned by evidence review")
            if len(reason) == 0 or len(reason) > 240:
                raise gl.vm.UserError("Invalid reason returned by evidence review")

            return {
                "decision": decision,
                "confidence": confidence,
                "reason": reason,
            }

        def validator_fn(leader_result) -> bool:
            if not isinstance(leader_result, gl.vm.Return):
                return False

            validator_result = evaluate_evidence()
            leader_data = leader_result.calldata

            if leader_data["decision"] != validator_result["decision"]:
                return False
            return abs(leader_data["confidence"] - validator_result["confidence"]) <= 15

        accepted = gl.vm.run_nondet_unsafe(evaluate_evidence, validator_fn)

        self.latest_subject = subject
        self.latest_evidence_url = evidence_url
        self.latest_decision = accepted["decision"]
        self.latest_confidence = u64(accepted["confidence"])
        self.latest_reason = accepted["reason"]
        self.review_count += u64(1)

        return self.latest_decision

    @gl.public.view
    def get_latest_review(self) -> dict[str, str]:
        return {
            "subject": self.latest_subject,
            "evidence_url": self.latest_evidence_url,
            "decision": self.latest_decision,
            "confidence": str(self.latest_confidence),
            "reason": self.latest_reason,
            "review_count": str(self.review_count),
        }

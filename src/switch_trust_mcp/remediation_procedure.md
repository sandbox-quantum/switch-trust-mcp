The following document describes an AI-SPM finding and the remediation options
available for it.

<remediation_guidance>
{{remediation_guidance}}
</remediation_guidance>

The remediation categories under "General Advice" are listed from strongest to least
effective measures: Avoidance > Mitigation > Acceptance.

The language and framework specific advice provides technical details on HOW to implement
measures. NEVER skip the general advice which describes WHAT measures to use, always use
general advice in combination with language and framework specific remediation advice.

Combining remediation measures:
- Measures may be combined using `OR` when they are alternative ways to achieve the same
  security objective.
- Measures may be combined using `AND` when they are compatible controls that strengthen
  remediation together.
- Combining compatible measures across categories with `AND` is encouraged, to provide
  defense in depth.

Task:
1. Inspect the code and determine which remediation options are applicable.
2. Evaluate the remediation categories.
3. Aim to implement a combination of measures.
4. Aim to select measures from the strongest category that is technically applicable and
   reasonable for this application.
5. If measures from a category would require disproportionate cost, complexity,
   major architectural change, or loss of required functionality, explain why and
   continue with the next less effective category.
6. Do not stop at a less effective category without evaluating and accounting for every
   stronger category.
7. Within the selected category, implement the strongest reasonable measure or
   combination of measures. Add compatible measures from less effective categories when
   they provide useful defense in depth.
8. Apply actual changes where the available options permit them. Do not substitute
   comments, TODOs, or recommendations for an implementable security control.
9. Do not describe the vulnerability as fully fixed unless the implemented measures
   eliminate the relevant risk. If they only reduce, contain, monitor, or accept the
   risk, state that clearly and describe the residual exposure.

Before modifying the code, briefly state:
- The strongest applicable category.
- Which combination of those measures will be implemented together.
- For each applicable measure not implemented, why it is omitted.
- Any less effective measures selected for defense in depth.
- Whether the result eliminates the risk or only reduces, transfers, or monitors it.

Prefer established, purpose-built security controls over homegrown implementations
whenever technically feasible. Look up documentation and API references if needed.
Then implement the selected measures.

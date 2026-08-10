---
description: Verify code changes after implementation or refactoring. Use after modifying application code, fixing bugs, refactoring, or changing tests to confirm the change is correct and existing tests were not weakened.
---

# Verify Change

After a code change:

1. Run the full test suite.
2. Inspect the current Git diff.
3. Check whether any tests were modified.
4. If tests changed, verify they were not weakened merely to make the implementation pass.
5. Check for obvious regressions, unnecessary complexity, or unrelated changes.
6. Report:
   - test result
   - files changed
   - whether tests were changed
   - any concerns found
   - final verdict

## Verdict contract

Use exactly one of these three verdicts — never a plain "PASS" qualified with
a "but fix X" caveat, since that contradicts itself:

- **PASS** — everything is clean, nothing outstanding.
- **PASS WITH WARNINGS** — functionally correct (tests pass, no regressions,
  no weakened tests) but there's a non-blocking issue worth fixing before
  commit/merge (e.g. a file saved in the wrong encoding, a stray debug
  print, a leftover TODO).
- **FAIL** — a real defect: broken tests, weakened/gutted tests, a
  regression, or behavior that contradicts the spec.

When in doubt whether something is blocking (FAIL) or just a warning (PASS
WITH WARNINGS), lean toward WARNINGS if the code/tests themselves are
correct and the issue is peripheral (formatting, encoding, docs) rather
than behavioral.

Do not claim the change is verified unless the checks above were actually performed. Explain in simple language what was done, and why was it done in a didactical manner.
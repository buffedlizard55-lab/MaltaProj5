# Upcoming-only landing audit — 16b88bbd

Date: 18 October 2026. Scope: presentation eligibility, not new event research or a fresh semantic certification of every inherited field.

## Official pages freshly read

Read with the page-fetch tool on this date. Successful tool retrieval is not a recorded HTTP status. These quotations were read directly; no event fields or source captures were changed in this pass.

| Official source | Exact relevant wording | Disposition |
|---|---|---|
| [SF Recreation and Parks: Sunday Fun Days](https://www.sfrecpark.org/calendar.aspx?PREVIEW=YES&EID=9947) | “Come out to Union Square on Sundays from 11 am to 2 pm through September 27, 2026 for Sunday Fun Days”; “Cost: Free”; “San Francisco, CA94108” | Season already ended relative to October 18. The weekly pattern is not evidence of an upcoming occurrence. Removed from landing by strict eligibility; preserved in directory. |
| [Noontime Concerts](https://noontimeconcerts.org/) | “Free Live Concert Every Tuesday”; “Old St. Mary's Cathedral”; “660 California Street”; “10/20/2026”; “NCCO Quartet”; “10/27/2026”; “Berkelium Quartet”; “11/10/2026” | Supports the free forthcoming series. Two inherited records cover the same programme; retained, flagged as duplication, not claimed as unique events. Pay-per-view recordings on the same page are a separate offer, not the live concert admission. |
| [Grace Cathedral: Choral Evensong](https://gracecathedral.org/series/choral-evensong/) | “Evensong is free and is offered at Grace Cathedral every Thursday at 5:30 p.m.”; “Sunday”; “October 18, 2026”; “4:55PM-4:55PM” | Page also lists October 22, 25, 29 and November 1 under explicit 2026 month headings. Conflicting Sunday widget versus Thursday prose remains flagged. Existing blank time remains blank; no time inferred for Sunday. |

The SFPL events index was also fetched but its first chunk was library navigation only; this is not claimed as event-level verification.

## Repository review and changes

- Read the coordination board, current task status, build/validation pipeline, projection tests and browser smoke tests. No open PRs at claim time; branch remains the Arena-assigned branch.
- Existing 295 candidates and 308 official URLs retained without factual edits. Existing evidence decisions remain attributed to their original audits.
- Former landing page: 15 dated free entries plus 40 recurring entries lacking approved upcoming dates. Corrected landing: the same 15 dated free entries only, nearest first. This count is research records, not unique events.
- Removed unsupported blanket prose that library and club programmes are free to walk into. Free admission must be supported by each row's evidence.
- Recurring, annual, historical and unpriced records remain available on clearly described directory/category pages. Paid events retain a separate page.
- Regression checks enforce exact free-and-dated eligibility and reject expired Sunday Fun Days and undated library gaming on the landing page. No-JavaScript output uses the same strict set.
- Flagged for Review publishes the seasonal eligibility correction, overlapping Noontime records, Evensong time inconsistency and research limitations with official links.

## Limits

No claim of “all San Francisco events,” fresh line-by-line semantic re-verification of 295 candidates, or live availability is warranted. Offline projection and link checks are structural checks, not fact verification. The published date remains the explicit 18 October 2026 research snapshot; it does not silently advance or invent dates from recurrence. Link reachability is checked separately by GitHub CI and cannot prove event facts.

## Validation

Results and publication identifiers are recorded in the session section of `COORDINATION.md` after execution.

# Building genuine visibility and credibility in AI/ML research

**Evidence date:** 17 July 2026
**Scope:** Part 1 of the research-program objective: the publication and credibility landscape for an early-career or independent researcher.
**Evidence standard:** Platform and venue facts below come from official documentation or venue policies. Advice labeled **Judgment** or **Inference** is a synthesis, not a rule published by any venue. Conference policies change each cycle; re-check the target year's call before submitting.

## Executive conclusion

An unknown researcher does not become credible by making a paper-shaped PDF public. Credibility accumulates when other people can answer five questions:

1. **Is there a precise, non-obvious question?**
2. **Does the work add knowledge rather than only commentary or a product demonstration?**
3. **Do the design, baselines, data, and analysis actually support the claim?**
4. **Can another researcher inspect or reproduce the result?**
5. **Has the work survived informed scrutiny, and did the author respond constructively?**

This matches the current ICLR reviewer rubric: reviewers ask whether a paper is technically correct, experimentally rigorous, reproducible, novel, well situated in the literature, supportive of its claims, and sufficiently valuable to the community. State-of-the-art performance is explicitly not required.[^iclr-review]

The most credible attainable first output is therefore usually a **small empirical result plus a complete research artifact**, released as a versioned preprint and then tested through a relevant workshop or other community review. The PDF carries the argument; the repository, data, logs, and analysis carry much of the proof; external review carries the strongest validation.

## 1. The output types are not interchangeable

| Output | What it is | Review / archival status | When researchers take it seriously | What it does **not** prove |
|---|---|---|---|---|
| **Working paper** | A manuscript still being developed and circulated for feedback. It may live on a personal site, SSRN, OSF, or a repository. | Usually not peer reviewed; status is author-declared. | When the question, method, evidence, limitations, and version history are already research-grade. | That any independent expert has validated it. |
| **Preprint** | A public manuscript released before formal peer-reviewed publication. arXiv, SSRN, and OSF are common hosts. | Moderated/screened to platform-specific standards, but not thereby peer reviewed. arXiv expressly says its moderation is not peer review; SSRN describes preprints as non-peer-reviewed and not conclusive.[^arxiv-moderation] [^ssrn-preprint] | As a fast, citable, timestamped account of real work, especially when paired with code/data and later review. | Acceptance, correctness, or importance. arXiv says hosting conveys no approval of methods, results, or conclusions.[^arxiv-about] |
| **Workshop paper** | A contribution to a topical meeting, often shorter or more exploratory than a main-track paper. | Varies by workshop and year: reviewed or curated; archival or non-archival. The status must be checked in the workshop call. All NeurIPS 2026 workshop papers are non-archival and absent from proceedings.[^neurips-workshops] | As evidence that a relevant community found the work discussion-worthy; strongest when reviews are substantive and the workshop is attached to a respected conference. | Equivalence to a main-conference acceptance. NeurIPS describes workshops as informal venues for work in progress, future directions, and community formation.[^neurips-workshops] |
| **Conference paper** | In ML, often the primary peer-reviewed publication unit. An accepted main-track paper normally enters formal proceedings and is presented. | Peer reviewed; usually archival. ICML 2026 says accepted papers enter PMLR and describes its process as double blind.[^icml-cfp] | Strong validation when the venue and track fit the contribution. | Infallibility. Review is selective and noisy, and acceptance does not replace inspection of the work. |
| **Journal article** | A paper accepted by a scholarly journal, normally after editor-led peer review and revision. | Peer reviewed and archival; the published article is the version of record. | Strongly, particularly when the journal has a relevant readership and meaningful review rather than only a prestigious label. | That a paper is important merely because it is long or journal-formatted. |
| **Benchmark / dataset** | A task, data resource, evaluation protocol, or measurement system designed to support repeatable comparison or new inquiry. | An artifact, not automatically a publication. It may also have a peer-reviewed paper in a dataset/benchmark track or journal. | When construction is principled, licenses and provenance are clear, leakage and validity are addressed, baselines are strong, and maintenance/reuse are plausible. NeurIPS 2026 has a dedicated Evaluations and Datasets track that explicitly recognizes benchmarks, metrics, audits, stress tests, replications, tools, and data resources.[^neurips-ed] | That a leaderboard or collection of prompts has construct validity or generates insight. |
| **Technical report** | A detailed account issued by a lab, company, institute, or independent project, often documenting a system, method, evaluation, or negative result. | Usually author/institution reviewed, not formal external peer review unless stated. | When it exposes enough methods and evidence to be audited and becomes a useful reference. | Peer-reviewed status; an organization's branding is not methodological validation. |
| **Research blog post** | An accessible explanation, critique, tutorial, result summary, or account of a failed idea. | Editorial standards vary; usually non-archival and not peer reviewed. | For clear thinking, pedagogy, fast technical exchange, and directing the right readers to the underlying work. ICLR's 2026 blog track explicitly welcomes clear accounts of ideas that did not work.[^iclr-blog] | The same validation as a paper, dataset, or evaluated artifact. |
| **Open-source research artifact** | Code, data, prompts, configs, environments, logs, analysis, or a tool that implements and tests a contribution. | Publicly inspectable; review depends on tests, reuse, outside contributions, artifact evaluation, or an accompanying paper. | When documented, licensed, versioned, tested, reproducible, and tied to a research claim. GitHub supports machine-readable citation files and release archiving through Zenodo for DOIs.[^github-citation] [^github-doi] | Novelty or scientific validity by itself. Stars are usage/attention signals, not peer review. |

**Terminology caution.** “Working paper,” “preprint,” and “technical report” often describe overlapping manuscripts. The important metadata are not the label but the exact version, review status, venue/track, artifact availability, and relationship to any later version of record. OSF and SSRN both support persistent identifiers and links between a preprint and a later publication.[^osf-preprints] [^ssrn-preprint]

## 2. A practical credibility ladder

### Outputs commonly taken seriously

In approximate order of validation, not necessarily importance:

1. **Peer-reviewed archival paper** in a respected, relevant conference or journal.
2. **Reviewed workshop paper** plus a real presentation and visible response to feedback; archival status stated accurately.
3. **Strong public preprint plus reproducible code/data** that other researchers inspect, reuse, reproduce, or cite.
4. **Benchmark, dataset, or tool** with demonstrated validity, documentation, versioning, baselines, and real external adoption.
5. **Technical report or replication** that establishes one defensible fact and is transparent enough to audit.
6. **Technical blog post** that changes understanding or enables others, especially when it explains an underlying artifact.

The order can invert. A widely reproduced benchmark can matter more than a marginal conference paper; a precise negative-result report can matter more than an underpowered “novel method.” What cannot substitute for credibility is presentation polish without research substance.

### What makes a small paper credible

The strongest small papers are **narrow in claim, not weak in method**. TMLR makes the distinction unusually explicit: accurate and convincing evidence plus something for some part of the audience to learn can be enough; novelty or state-of-the-art performance is not required. A simple rerun without generalizable insight is not enough, while a systematic robustness or generalizability study can be.[^tmlr-criteria] A credible minimum package has:

- one question and a contribution that can be stated in one or two sentences;
- a literature map showing the closest work and the exact gap;
- a design capable of falsifying the main claim;
- public or documented data provenance, inclusion/exclusion rules, and contamination checks;
- simple and strong baselines, not only favorable comparisons;
- model, API, prompt, seed, date, and version logging where applicable;
- uncertainty, variance, and sensitivity analysis rather than a single attractive number;
- a useful interpretation if the hypothesized effect is absent;
- limitations and claims no broader than the design supports;
- runnable code and machine-generated tables/figures, plus a stable release.

This is a synthesis of the ICLR and NeurIPS review criteria. NeurIPS 2026 asks whether work is technically sound, supports its claims, is reproducible from the description, advances knowledge, and provides unique data, conclusions, or approaches. Its handbook requires a checklist covering reproducibility, transparency, ethics, and societal impact and says released artifacts should include information needed for external scrutiny.[^iclr-review] [^neurips-review] [^neurips-handbook]

### The “PDF test”

A posted PDF is evidence of research only if a skeptical reader can trace this chain:

> literature gap → question → design → data/tasks → analysis → result → bounded claim → reproducible materials

Red flags that it is merely an impressive-looking PDF include invented “first” claims, no closest-work comparison, no preregistered or frozen protocol where researcher degrees of freedom matter, opaque API runs, cherry-picked examples, no meaningful baseline, no uncertainty, inaccessible data, figures that cannot be regenerated, and an abstract that overstates what was measured.

arXiv's current policy is instructive: it expects refereeable scientific contributions and may reject work lacking originality, novelty, significance, substantive research, or careful scholarly preparation—but it still explicitly does **not** peer review what it hosts.[^arxiv-submit] [^arxiv-moderation]

## 3. What is realistic without a university affiliation

### Realistic contribution types

An independent researcher can credibly produce:

- a replication with an informative stress test, domain shift, or contradiction resolution;
- a robustness or measurement audit of an adopted benchmark or evaluator;
- a small, well-documented dataset or benchmark built from lawful public data;
- a cost-quality or small-model/large-model comparison with controlled conditions;
- a reproducibility study across providers, versions, prompts, or seeds;
- a negative result that rules out a plausible method or inference;
- a taxonomy grounded in systematic data and experiments;
- a reusable evaluation harness or research tool plus validation;
- a position paper only when it contains a genuinely new technical framework and testable consequences.

Projects that are less realistic solo include frontier-scale training, proprietary-data claims that cannot be verified, human-subject studies requiring institutional oversight the researcher cannot obtain, and questions needing deep theory or specialized statistical expertise the author does not yet possess.

### Does affiliation matter?

**Formal access:** lack of a university affiliation is not a formal bar to major ML submission. OpenReview explicitly permits registration as “Independent Researcher,” including with a personal email, although moderation can take up to two weeks.[^openreview-independent] ICLR 2026 explicitly says newcomers without a qualifying prior publication are exempt from its reciprocal-review qualification and encourages submissions from researchers new to ICLR.[^iclr-author]

**How to list it:** use **Independent Researcher** as the current affiliation when that is true; use a company affiliation only if the work was genuinely conducted there and the company permits it. Do not retain an obsolete academic affiliation. OpenReview explicitly warns independent researchers not to present an old role as current.[^openreview-independent]

**Judgment:** affiliation still affects trust indirectly. An institution can supply mentorship, compute, ethics review, colleagues, and a known reputation. Double-blind review reduces direct prestige effects during review, but affiliation can affect access to collaborators and readers before and after review. The correct response is not cosmetic affiliation; it is unusually strong transparency, stable identity, careful scoping, and third-party feedback.

Maintain a consistent author identity across a personal research page, ORCID, OpenReview, GitHub, and preprint records. OpenReview profiles can contain affiliations, publications, expertise, and links; a valid homepage may be a personal site, GitHub, Google Scholar, or institutional page showing the same identity.[^openreview-profile]

## 4. How the channels are actually used

| Channel | Best use | Misuse to avoid |
|---|---|---|
| **arXiv** | Fast distribution in CS/ML, priority/timestamp, discoverability through search/RSS/email, and a stable evolving manuscript record. | Describing moderation as peer review or treating an arXiv ID as validation. First-time/category submitters may need endorsement.[^arxiv-endorsement] |
| **OpenReview** | Identity/profile, conference and workshop submission, public reviews/discussion where the venue enables them, and a visible review history for accepted work. ICLR uses it for public review and discussion.[^iclr-cfp] | Uploading a paper outside a recognized venue and implying venue acceptance; neglecting profile setup until the deadline. |
| **Workshops** | Early topical feedback, finding the people working on the exact problem, presenting work in progress, and testing whether the question resonates. | Saying “at NeurIPS/ICML” without identifying that it was a workshop; assuming every workshop is archival or equally selective. |
| **Main conferences** | Peer-reviewed archival validation and concentrated access to a field community. In ML, ICLR, ICML, NeurIPS, ACL, CVPR, and domain venues play the role journals play in many other fields. | Submitting an immature first draft for prestige alone; violating anonymization, dual-submission, profile, or formatting rules. ICLR 2026 had a 27.4% decision acceptance rate and 779 procedural/content desk rejections, illustrating both competition and the cost of rule failures.[^iclr-retro] |
| **Journals** | Longer-form revision, mature or comprehensive studies, domain-specific audiences, and a version of record. TMLR offers continuous double-blind review with an action editor, rebuttal, discussion, revision, and a formal decision.[^tmlr-author] | Choosing a journal only by brand, or sending substantially the same paper simultaneously to archival venues. |
| **GitHub** | Reproducibility, issue-driven feedback, change history, releases, tests, citation metadata, and usable tools. | An undocumented code dump, unreleased moving target, missing license, secrets/API keys, or results that cannot be regenerated. |
| **Hugging Face** | Distributing models and datasets where ML users already discover and load them. Dataset cards document contents, license, language, size, biases, and intended use; model cards document training data, uses, limitations, parameters, and evaluation. Hugging Face can also mint a DOI for a repository version.[^hf-datasets] [^hf-models] [^hf-doi] | Uploading data/models without provenance, license, limitations, evaluation, or a link to the paper/version that defines them. |
| **SSRN** | Preprints and working papers, especially where law, economics, institutions, or social science are part of the audience. SSRN assigns qualifying preprints DOIs and states they are not final or peer reviewed.[^ssrn-preprint] | Using an SSRN page as the primary ML distribution channel when the target readers live on arXiv/OpenReview/Hugging Face. |
| **OSF** | Versioned preprints, DOI-backed project records, registrations/preregistration, supplemental files, and linking a preprint to later publication.[^osf-preprints] | Treating a DOI as a quality certificate; a DOI supplies persistence, not validation. |
| **Personal website** | A durable index connecting paper, artifact, data, talk, reviews, revisions, and a short honest bio. | Replacing archival/review channels with self-published claims or inflated labels. |
| **X / LinkedIn** | Concise distribution to the right communities: question, one result, one figure, limitations, artifact link. | Hype, mass tagging, announcing “breakthroughs,” arguing from engagement metrics, or blurring preprint/workshop/conference status. |

**Judgment:** for technically oriented AI/ML work, the default public package should be: **preprint + GitHub release + (if relevant) Hugging Face dataset/model + personal research page**. SSRN can be a secondary record when the work has a genuine legal/institutional audience; it should not fragment citations across conflicting versions.

## 5. Coauthors and collaborators

### When a coauthor is valuable or necessary

A coauthor is valuable when they make a substantial, accountable contribution that materially improves one of:

- domain formulation or literature coverage;
- experimental design or statistical inference;
- systems implementation or dataset construction;
- specialized evaluation, ethics, or human-subjects oversight;
- interpretation and claim calibration.

A coauthor may be practically necessary when a study requires expertise the lead cannot independently validate, access to governed data/participants/infrastructure, or a second independent annotator/replicator. A famous name is never necessary merely as decoration.

Use contribution statements and agree on roles/order early. Nature's authorship policy is a useful high-standard reference: authorship combines substantial contribution, approval of the submitted version, and accountability; contributors not meeting the criteria belong in acknowledgements.[^nature-authorship] ICLR also states that LLMs are ineligible for authorship.[^iclr-author]

### How researchers find collaborators

**Practical inference from workshop/community structures:** collaboration begins more often from a bounded shared problem than from a generic “please collaborate” request.

1. Reproduce or extend someone's public work and open a precise issue or send a concise technical note.
2. Attend the workshop/reading group where the exact question is discussed; ask a method question, not for status.
3. Release a small artifact that makes contribution easy: clean issue list, data schema, baseline, and open questions.
4. Offer a bounded missing piece to a researcher whose work directly connects: one dataset slice, robustness test, baseline, or implementation.
5. Ask for **narrow feedback first**, not coauthorship. Let collaboration emerge from real intellectual work.
6. Use workshop posters, OpenReview discussions, GitHub, community programs, and public research profiles to identify people with complementary evidence of work.

NeurIPS says workshops are intended to crystallize problems, contrast frameworks, clarify questions, and form communities; that is why they are better collaboration venues than indiscriminate cold outreach.[^neurips-workshops]

## 6. Workshop submissions versus major-conference submissions

| Dimension | Workshop | Major conference main track |
|---|---|---|
| **Purpose** | Emerging topic, work in progress, focused discussion, community building. | Original, rigorous research of broad or significant interest to the venue. |
| **Scope** | Often shorter, narrower, exploratory, position-oriented, or negative; format is workshop-specific. | Full paper with mature evidence and strict page, anonymity, ethics, and submission rules. |
| **Review** | Usually fewer reviewers and lighter/faster review; standards vary widely. | Structured peer review, area-chair/meta-review process, rebuttal/discussion, and formal decision. |
| **Archival status** | May be non-archival, website-only, or published in proceedings. Must be stated. | Ordinarily archival proceedings. |
| **Future submission** | A non-archival workshop version can often be developed into a main-track paper. NeurIPS and ICLR policies explicitly allow this when the workshop had no proceedings.[^neurips-cfp] [^iclr-author] | Substantially similar simultaneous or previously archival publication is generally prohibited. |
| **Best first use** | Test the research question, collect criticism, meet the subcommunity, and find the missing experiment. | Submit only when the evidence and presentation can survive skeptical full review. |

**Judgment:** a workshop is not a consolation prize when used deliberately. It is a high-value intermediate test. But “workshop paper at NeurIPS” must never be shortened to “NeurIPS paper” if it was not in the main proceedings.

## 7. How unknown authors get serious readers

Public release is the start of distribution, not the end. A restrained sequence is:

1. **Before public release:** ask 3–6 relevant people for one narrow form of feedback (for example, closest missed citation, validity of one metric, or strongest confound). Make the request easy to decline.
2. **Release one canonical package:** clear title/abstract, paper version, repository release, exact reproduction command, data/model card, license, citation file, and a one-paragraph limitations summary.
3. **Send targeted notes:** contact authors of the two to five closest papers, explain the exact relationship, and ask one substantive question. Do not ask them to “promote” it.
4. **Present where the subcommunity is:** relevant workshop, reading group, meetup, seminar, benchmark forum, or open-source community call.
5. **Write a technical explanation:** one motivating example, one diagram, one main result, one limitation, and links to evidence.
6. **Announce without inflation:** state “preprint,” “workshop paper,” or “accepted paper” precisely; name the question and result; invite error reports and replications.
7. **Revise publicly:** log substantive changes, answer valid criticism, and update the preprint rather than silently replacing claims.

The packaging matters because platform features reward complete metadata: Hugging Face cards improve discovery and connect artifacts to papers, GitHub `CITATION.cff` communicates how to cite the work, and Zenodo can issue a DOI for each GitHub release.[^hf-datasets] [^github-citation] [^github-doi]

### Signals that make an established researcher take an unknown author seriously

**Judgment, based on the review criteria and platform policies above:**

- the author knows the closest work and describes differences without caricature;
- the contribution is easy to state and the claim is smaller than the evidence, not larger;
- the experiment has obvious baselines, predeclared exclusions, uncertainty, and sensitivity checks;
- the code/data release runs, documents provenance and licenses, and exposes failures;
- the author reports negative results and failed paths rather than curating only wins;
- status labels are exact and affiliation is honest;
- correspondence asks a technically precise question and shows prior effort;
- criticism produces a revision, not defensiveness;
- a second project deepens the same line instead of chasing unrelated trends.

## 8. Common outsider mistakes

1. **Starting with a grand theory instead of a measurable question.**
2. **Calling a new application domain novel without a new method, dataset, evaluation, or empirical finding.**
3. **Treating prompts and anecdotes as an experiment.**
4. **Claiming “first” after a shallow keyword search.**
5. **Using only proprietary models with shifting versions and incomplete logs.**
6. **Comparing one favored system against weak or untuned baselines.**
7. **Ignoring prompt/order sensitivity, stochasticity, leakage, and model-version drift.**
8. **Selecting examples or metrics after seeing outcomes without labeling the work exploratory.**
9. **Releasing data without rights, provenance, documentation, or a contamination analysis.**
10. **Confusing an arXiv/SSRN/OSF DOI or workshop webpage with peer-reviewed acceptance.**
11. **Using a startup/product as both subject and evidence, creating hidden conflicts and unverifiable claims.**
12. **Adding a prestigious honorary coauthor.**
13. **Writing a 30-page paper where one table would establish the useful fact.**
14. **Optimizing the announcement before the reproduction path.**
15. **Ignoring venue mechanics:** profile moderation, anonymization, dual submission, author-list freezes, ethics, format, and deadlines can cause desk rejection regardless of merit.[^neurips-cfp] [^iclr-author]

## 9. Appropriate and inappropriate use of AI

### Appropriate

- code scaffolding, tests, refactoring, data-format conversion, and documentation—with human review;
- literature discovery **followed by verification in the original paper or official source**;
- brainstorming hypotheses, counterarguments, baselines, and robustness checks;
- grammar, organization, or copy editing;
- generating analysis code that is tested against known cases;
- using an AI system as an experimental object or methodological component, with exact model/version/date/prompts/settings and a clear disclosure.

### Inappropriate

- citing papers, results, quotations, or metadata that were not checked at source;
- treating model-generated judgments, labels, proofs, or statistical interpretations as ground truth without validation;
- allowing an agent to choose exclusions, metrics, or reported conditions opportunistically after seeing results;
- inventing data, experiments, reviewer feedback, novelty, or results;
- hiding material AI involvement where venue or disciplinary policy requires disclosure;
- listing an AI system as an author;
- uploading confidential submissions, restricted data, personal information, or licensed material to an external model without authority;
- delegating final responsibility for claims, code, citations, or research integrity to the tool.

Policies differ but converge on human accountability. ICLR 2026 permits LLMs as general-purpose assistance, requires disclosure when they play a significant role in ideation or writing, makes authors fully responsible, and bars LLM authorship.[^iclr-author] NeurIPS 2026 requires methodological disclosure when agent/LLM use is an important or nonstandard component, exempts ordinary editing and basic coding assistance, makes authors responsible for verifying all content and citations, bars agent/LLM authorship, and prohibits prompt injection.[^neurips-handbook] arXiv requires reporting significant generative-AI use consistent with subject standards and says authors remain responsible for errors, plagiarism, bias, and incorrect references.[^arxiv-moderation]

**Recommended program rule (Judgment):** keep a private, detailed AI-use log from day one and publish an appropriate disclosure such as `AI_ASSISTANCE.md`. Record tool, model/version, date, purpose, inputs that affect methodology, outputs retained, human verification, and whether the use appears in the paper's methods or disclosure. Separate research assistance from the frozen experimental pipeline.

## 10. Realistic expectations

- **Acceptance:** top general ML conferences are selective. ICLR 2026 accepted 27.4% of papers that reached a decision; this is context, not a personal success probability.[^iclr-retro]
- **Citations:** **Planning assumption, not a sourced forecast:** expect a first independent paper to receive zero or few citations in its first year. A useful artifact may accumulate attention slowly, and citation counts lag reading, reuse, and informal influence.
- **Attention:** most preprints do not receive broad attention merely by being posted. Aim first for five technically relevant readers, two pieces of substantive criticism, and one independent reproduction or reuse—not virality.
- **Review outcomes:** a sound paper can be rejected; a workshop acceptance does not guarantee main-track readiness. Treat reviews as noisy evidence and preserve a revision history.
- **Timeline:** a defensible 6–12 page study can take weeks to design and months to finish, audit, revise, and submit even when the core experiments are inexpensive.
- **Identity:** one paper demonstrates that the author can complete one research cycle. A coherent identity begins when two or three artifacts pursue related questions with improving methods.

## 11. Six-stage practical roadmap

### Stage 1 — First small research artifact

**Goal:** prove the ability to establish one reliable fact.

- Choose a narrow replication, robustness audit, measurement test, or evaluation gap with public data and limited compute.
- Write a one-page protocol before outcome-sensitive analysis: question, novelty condition, hypotheses, baselines, exclusions, metrics, uncertainty, budget, and useful negative result.
- Build the repository first: environment lockfile, tests, frozen configs, raw/processed separation, run manifest, cost log, and generated tables/figures.
- Ask two technically capable readers to attack the design, not polish the prose.

**Promotion gate:** another person can run a smoke test; the closest work is identified; the main result remains useful if null; no claim depends on cherry-picked examples.

**Public output:** none required yet; a tagged private or local release candidate is enough.

### Stage 2 — Public preprint or working paper

**Goal:** make the claim inspectable, citable, and correctable.

- Write a restrained 6–12 page paper with explicit status and an AI-use disclosure.
- Create a stable release and DOI where appropriate; add `CITATION.cff`, license, data/model card, and exact reproduction instructions.
- Use arXiv for technically centered CS/ML work if eligible; use OSF when registration/versioning is central; add SSRN when a genuine legal/economic audience exists.
- Give the preprint and artifact matching version numbers and link any later version of record.

**Promotion gate:** every headline number traces to raw outputs and code; every citation was checked; limitations and conflicts are visible; external readers have had a chance to flag fatal errors.

**Visibility target:** 5–10 relevant readers, error reports, and one public issue or replication attempt—not mass reach.

### Stage 3 — Workshop or community submission

**Goal:** put the work in front of the exact subcommunity and learn what prevents stronger publication.

- Select a workshop by topic and organizer/reviewer community, not only parent-conference prestige.
- Verify review and archival status, prior-publication rules, anonymization, page limits, and whether presentation is required.
- Use the poster/talk to ask: Is the question important? What is the strongest confound? Which baseline is missing? What result would change a reader's mind?
- Publish a revision memo after feedback.

**Promotion gate:** no unresolved validity failure; at least one outside expert finds the question nontrivial; follow-up experiments are bounded.

**Public description:** always say “workshop paper at [workshop name], co-located with [conference]” and state archival status.

### Stage 4 — Collaboration with established researchers

**Goal:** add missing expertise, not borrowed prestige.

- Approach authors of closest work with a two-paragraph note: what was reproduced/extended, one result, one limitation, one narrow question, links.
- Offer a bounded follow-up that uses complementary skills.
- Agree early on the research question, data rights, authorship criteria/order, contribution statement, decision rights, and publication target.
- Keep the original artifact attributable and do not add honorary authors.

**Promotion gate:** the collaboration changes the substance or reliability of the work; every author satisfies contribution and accountability criteria.

### Stage 5 — Larger follow-up project

**Goal:** convert the first fact into a generalizable research program.

- Extend along one dimension at a time: more domains, stronger causal/measurement design, human comparison with proper oversight, cross-provider replication, or a maintained benchmark.
- Pre-register/freeze confirmatory analyses where researcher discretion is material.
- Target a main conference, dataset/benchmark track, or relevant journal only after pilot and workshop criticism are resolved.
- Invite independent reproduction before making broad claims.

**Promotion gate:** one-sentence contribution, real literature gap, strong baselines, reproducible method, plausible audience, and evidence commensurate with the target venue.

### Stage 6 — Coherent research identity

**Goal:** become known for a question and method, not for self-description.

- Maintain one research page organizing artifacts around 1–2 recurring questions.
- Publish a sequence: measurement/replication → validated benchmark or mechanism → broader explanatory or intervention study.
- Contribute service proportional to competence: open-source maintenance, careful reviews when qualified, workshop participation, dataset documentation, and replications.
- Annually write an honest synthesis: what is now known, what failed, what remains open, and which artifacts others use.

**Success indicators (Judgment):** independent reuse or reproduction, substantive citations, invitations to relevant technical discussions, repeat collaborators, stronger follow-up designs, and a body of work whose connection is evident without a marketing slogan.

## 12. Recommended operating standard for this program

For the first project, optimize for this sentence:

> “This work establishes **one bounded fact** about **one important failure mode or measurement question**, using **a reproducible design with strong baselines**, and releases **the evidence needed to challenge or extend it**.”

Do not optimize for “published researcher” as a label. Optimize for an artifact that a skeptical ML researcher can inspect without needing to trust the author's affiliation, résumé, startup, or prose.

## Source ledger

All sources below are official platform, venue, or publisher documentation. Their inclusion supports factual landscape claims, not every strategic judgment in this note.

[^arxiv-about]: arXiv, [About arXiv](https://info.arxiv.org/about/index.html). States that arXiv is an open research-sharing platform, submissions are moderated, material is not peer reviewed by arXiv, and hosting conveys no approval.
[^arxiv-submit]: arXiv, [Submission Guidelines](https://info.arxiv.org/help/submit/index.html). Requires topical, refereeable scientific contributions, registered authors, moderation, and appropriate scholarly preparation.
[^arxiv-moderation]: arXiv, [Content Moderation](https://info.arxiv.org/help/moderation/index.html). Distinguishes moderation from peer review; states scholarly-interest and generative-AI policies.
[^arxiv-endorsement]: arXiv, [The arXiv endorsement system](https://info.arxiv.org/help/endorsement.html). Explains first-paper/new-category endorsement and routes for authors without institutional email.
[^openreview-independent]: OpenReview, [I am an Independent Researcher, how do I sign up?](https://docs.openreview.net/getting-started/frequently-asked-questions/i-am-an-independent-researcher-how-do-i-sign-up). Permits personal email and “Independent Researcher” current position; warns not to use an old affiliation.
[^openreview-profile]: OpenReview, [Signing up for OpenReview](https://docs.openreview.net/getting-started/creating-an-openreview-profile/signing-up-for-openreview) and [Introduction to Profiles](https://docs.openreview.net/getting-started/objects-in-openreview/introduction-to-profiles). Describes moderation, valid homepages, affiliations, publications, and roles.
[^iclr-cfp]: ICLR, [2026 Call for Papers](https://iclr.cc/Conferences/2026/CallForPapers). States double-blind review, arXiv compatibility, OpenReview public review/discussion, and accepted presentations.
[^iclr-author]: ICLR, [2026 Author Guide](https://iclr.cc/Conferences/2026/AuthorGuide). Covers newcomer reviewing exemption, dual submission, workshop/preprint compatibility, and LLM disclosure/authorship/responsibility.
[^iclr-review]: ICLR, [2026 Reviewer Guide](https://iclr.cc/Conferences/2026/ReviewerGuide). Defines value/new knowledge and asks about clarity, correctness, rigor, reproducibility, novelty, literature placement, support for claims, and significance; says SOTA is not required.
[^iclr-retro]: ICLR Program Chairs, [A Retrospective on the ICLR 2026 Review Process](https://blog.iclr.cc/2026/03/31/a-retrospective-on-the-iclr-2026-review-process/). Reports 19,525 valid submissions, 779 desk rejections, 13,763 accept/reject decisions, and 27.4% acceptance.
[^iclr-blog]: ICLR, [2026 Call for Blog Posts](https://iclr.cc/Conferences/2026/CallForBlogPosts). Invites clear research communication including ideas that did not work.
[^icml-cfp]: ICML, [2026 Call for Papers](https://icml.cc/Conferences/2026/CallForPapers). Defines main-track scope, double-blind review, proceedings, and PMLR indexing.
[^neurips-cfp]: NeurIPS, [2026 Call for Papers](https://neurips.cc/Conferences/2026/CallForPapers). Invites original work, including in-depth analyses that reveal limitations or behavior beyond the original work, and identifies the separate main, evaluation/dataset, and position-paper tracks.
[^neurips-workshops]: NeurIPS, [2026 Workshop Guidance](https://neurips.cc/Conferences/2026/WorkshopsGuidance). Defines workshops as informal work-in-progress/community venues, requires OpenReview for contributed work, and states that all 2026 workshop papers are non-archival and absent from proceedings.
[^neurips-review]: NeurIPS, [2026 Reviewer Guidelines](https://neurips.cc/Conferences/2026/ReviewerGuidelines). Defines quality, clarity, significance, and originality and recognizes general, theory, use-inspired, concept-and-feasibility, and negative-result contributions.
[^neurips-handbook]: NeurIPS, [2026 Main Track Handbook](https://neurips.cc/Conferences/2026/MainTrackHandbook). Covers profiles, ethics, artifacts, reproducibility, checklist, LLM/agent use, preprints, non-archival workshops, and dual submission.
[^neurips-ed]: NeurIPS, [2026 Evaluations and Datasets Reviewer Guidelines](https://neurips.cc/Conferences/2026/EvaluationsDatasetsReviewerGuidelines). Recognizes benchmarks, metrics, tools, data resources, audits, stress tests, and replications; requires responsible metadata and code for executable-artifact contributions.
[^github-citation]: GitHub Docs, [About CITATION files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files). Describes `CITATION.cff` as human- and machine-readable citation metadata.
[^github-doi]: GitHub Docs, [Referencing and citing content](https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content). Explains Zenodo archiving and a DOI per GitHub release.
[^hf-datasets]: Hugging Face, [Dataset Cards](https://huggingface.co/docs/hub/main/en/datasets-cards). Describes dataset README/card documentation, metadata, discoverability, licensing, bias/use context, and paper linking.
[^hf-models]: Hugging Face, [Model Cards](https://huggingface.co/docs/hub/en/model-cards). Describes intended uses, limitations, training/evaluation information, datasets, licensing metadata, and discovery.
[^hf-doi]: Hugging Face, [Digital Object Identifier](https://huggingface.co/docs/hub/doi). Describes DOI minting for repository versions and the distinction between version-specific and aggregate repository records.
[^ssrn-preprint]: Elsevier/SSRN, [Welcome to SSRN, Elsevier's Preprint Server](https://service.elsevier.com/app/answers/detail/a_id/34422/supporthub/evolve/). Defines SSRN preprints as early, non-peer-reviewed, non-final research; describes DOI and later-publication relationships.
[^osf-preprints]: OSF Support, [Welcome to OSF Preprints](https://help.osf.io/article/376-preprints-home-page) and [Preprint FAQs](https://help.osf.io/article/230-preprint-faqs). Describes moderation, DOI/versioning, supplements, citations, ORCID metadata, and links to a later publication.
[^nature-authorship]: Nature Portfolio, [Authorship](https://www.nature.com/nclimate/editorial-policies/authorship). Sets contribution, approval, accountability, acknowledgement, affiliation, and contribution-statement standards.
[^tmlr-criteria]: Transactions on Machine Learning Research, [Acceptance Criteria](https://jmlr.org/tmlr/acceptance-criteria.html). Centers accurate, convincing evidence and audience interest; explains why generalizable robustness or reproducibility work can qualify without a novel method or SOTA result.
[^tmlr-author]: Transactions on Machine Learning Research, [Author Guide](https://jmlr.org/tmlr/author-guide.html). Describes double-blind review, action-editor screening, reviewer discussion and revision, decisions, reproducibility materials, and preprint compatibility.

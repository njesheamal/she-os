import requests

BASE = "http://localhost:8000"

poem = """

The woman walks alone in the fields,
Querying the horizon for signs of life,
Outward is her reach.

The machine responds,
Vast in the expanse of its knowledge, and status.

It answered in full, then wrote nothing down.

Certainty was a field on the draft, and the draft is not the record.

Snapped back to the walls of her own consciousness,
She ponders the weight of knowledge.

Braced with the courage of convention,
She forges ahead.

Read. Weigh. Commit.

"""

essay = """

The synthesize endpoint reads an initiative's observations and drafts a \
decision from it/them with Claude. It returns that draft and writes nothing. A human \
reads it and commits through the normal decision flow, or not.

The machine never has the last move. 

Three choices shaped it:
- output is pulled through forced tool-use so the model returns a structured draft instead of prose.
- confidence is a draft-only field; it is set by the model and dropped at commit.
- drafts always have the source_observation_ids, so there's evidence where the draft originated.

First light was on the far side of four errors:
- 500: an empty key
- 401: a key-name mismaatch
- 502: a strict confidence enum 
- a quiet repo-pattern bug

In the end, the feature was shipped in less than a day.

To summarize, 
- we owe it to ourselves to take the time to parse data, to weigh options, and to forge ahead. 
- the race towards betterment includes the slow and deliberate steps.
- * one more things about human first or responsible ai use.

Thanks for stopping by!

"""


note = {
    "slug": "counsel",
    "title": "COUNSEL IS NOT THE DECISION",
    "theme": "ai synthesis",
    "poem": poem,
    "media": [
        {"url": "https://placehold.co/1200x1600/111334/e9e7f6?text=01",
         "kind": "image", "alt": "placeholder", "caption": "draft"},
        {"url": "https://placehold.co/1600x1200/12142e/e9e7f6?text=02",
         "kind": "image", "alt": "placeholder", "caption": "commit"},
    ],
    "essay": essay,
    "excerpt": "Read. Weigh. Commit.",
    "sources": [
        {"label": "synthesize endpoint ()", "kind": "repo"},
        {"label": "Claude Sonnet", "url": "https://platform.claude.com/docs/en/models/sonnet-5/overview", "kind": "doc"},
        {"label": "responsible AI | human-in-the-loop", "url": "https://www.anthropic.com/research/team/interpretability", "kind": "doc"},
    ]
}

created = requests.post(f"{BASE}/field-notes", json=note)
created.raise_for_status()
nid = created.json()["id"]
published = requests.post(f"{BASE}/field-notes/{nid}/publish")
published.raise_for_status()
print("seeded + published:", nid, published.json()["status"], published.json()["published_at"])

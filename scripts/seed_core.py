"""Seed the core celestial-layer entities for SHÉ OS.

Idempotent: safe to re-run. Each entity is POSTed; an existing slug (409)
counts as already-seeded and is skipped. Start the API on :8000 first, then:

    python scripts/seed_core.py

The SUMA description is the original. TUFA / GIDA / the tech brand / SHÉRocks
descriptions are reconstructions — replace with your real copy.
Initiative-type IDs are the stable UUIDs seeded by the Alembic lookup migrations.
"""
import sys
import requests

BASE = "http://localhost:8000"

TYPE_PUBLISHING = "33333333-0000-4000-8000-000000000004"      # "publishing"
TYPE_SOCIAL_IMPACT = "33333333-0000-4000-8000-000000000003"   # "social_impact_program"

BRANDS = [
    {
        "name": "SUMA",
        "slug": "suma",
        "status": "active",
        "description": "Hair and care brand rooted in the principles of sustainability, wellness, and culturally significant beautification. It is a brand that celebrates the beauty of Black hair and skin, bringing centuries old traditions into modern formulations and applications. SUMA is committed to helping create a world that feels confident, imaginative, and grounded. The brand prioritizes safe, effective ingredients, as well as ethical production practices, thoughtful construction, and reliable hair solutions. This brand is very eager to make breakthroughs and contributions in the automation and beauty tech space, and is always looking for ways to improve the haircare experience. As a flagship brand within SHÉ Estate, SUMA combines product innovation with an emphasis on quality, longevity, and intentional production.",
    },
    {
        "name": "TUFA",
        "slug": "tufa",
        "status": "active",
        "description": "Fashion brand rooted in cultural expression, intentional design, enduring craftsmanship, and sustainability. It approaches fashion as a way to communicate sense of self, creating pieces that deserve to be worn, kept, and passsed down. TUFA is helping create a world that feels connected, introspective, and forward-looking. The brand prioritizes natural, durable fabrics, and ethical production practices, while also exploring new technologies and materials. TUFA is about fashion as identity, expression, and possibility: honoring where we came from while imagining where we can go. As with many brands within the Estate, TUFA favors made-to-order, small batch, and limited-run production over mass production.",
    },
    {
        "name": "GIDA",
        "slug": "gida",
        "status": "active",
        "description": "Home and lifestyle brand rooted in intentional living, considered design, enduring craftsmanship, and sustainability. It approaches the home as an expression of belonging, taste, and comforts. GIDA is helping create a world that harmonious, timeless, and efficient. The brand prioritizes durability and indegenous materials and production, while exploring method improvements and sustainable practices. GIDA is about the home as a place of recalibration, being recharged by the things that help us function at our best and see the beauty in the world around us. As with many brands within the Estate, GIDA favors made-to-order, small batch, and limited-run production over mass production. Enduring over disposable.",
    },
    {
        "name": "AMSA",
        "slug": "amsa",
        "status": "active",
        "description": "Technology and creative studio: software, SEO, AI automation, "
                       "design, social. An answer. A response. A way forward. AMSA provides consulting, contract engineering, software development, systems integration, automation, technical implementation, and new product development. It is a flexible technical partner that can advise, design, troubleshoot, build, integrate, and deliver through contracted expertise. To whatever comes next.",
    },
]

INITIATIVES = [
    {
        "initiative_type_id": TYPE_PUBLISHING,
        "name": "Editions",
        "slug": "editions",
        "status": "active",
        "description": "The library of media. Houses field notes and published media, of varied formats, across the estate.",
    },
    {
        "initiative_type_id": TYPE_SOCIAL_IMPACT,
        "name": "SHÉRocks",
        "slug": "she_rocks",
        "status": "active",
        "description": "Social impact program to support Black girls/women in STEAM. It aims to act as a gateway to scientific discovery, cultural appreciation, creative exploration, and technical skill-building. The initiative supports girls through fundraising, educational resources, mentorship, and community-building. As an initiative, SHÉRocks leverages the Estate's resouces, relationships, and ecosystem to turn awareness into action, and create lasting community value.",
    },
]


def seed(path: str, items: list[dict], label: str) -> None:
    for item in items:
        res = requests.post(f"{BASE}{path}", json=item)
        if res.status_code == 201:
            print(f"  created {label}: {item['slug']}")
        elif res.status_code == 409:
            print(f"  exists  {label}: {item['slug']} (skipped)")
        else:
            print(f"  FAILED  {label}: {item['slug']} -> {res.status_code} {res.text}")


def main() -> None:
    try:
        requests.get(f"{BASE}/brands", timeout=5).raise_for_status()
    except Exception as exc:
        sys.exit(f"API not reachable at {BASE} ({exc}). Start the backend first.")
    print("Seeding brands...")
    seed("/brands", BRANDS, "brand")
    print("Seeding initiatives...")
    seed("/initiatives", INITIATIVES, "initiative")
    print("Done.")


if __name__ == "__main__":
    main()




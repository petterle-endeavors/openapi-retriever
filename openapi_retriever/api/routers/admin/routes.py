"""Define routes for health checks."""
from fastapi import APIRouter


ROUTER = APIRouter()


@ROUTER.get("/status", include_in_schema=False)
def health():
    """Return a 200 response."""
    return {"status": "ok"}


PRIVACY_POLICY = """\
### Privacy Policy for Petterle Endeavors API

**Effective date: January 1, 2023**

We at Petterle Endeavors ("we", "us") respect your privacy and are committed to protecting your personal data. This privacy policy informs you about how your personal data is handled when you use our API services. Please read it carefully.

**1. Information We Collect**

When interacting with our API, we might collect information, which could include your IP address and any other information you may provide when making API requests.

**2. How We Use Your Information**

We use the data we collect mainly to provide, maintain, protect and improve our API service, develop new ones, and protect us and our users. We do not share personal data with companies, organizations, or individuals outside Petterle Endeavors unless one of the following circumstances applies:

- **With your consent**: We will share personal data when we have your consent.
- **For legal reasons**: We will share personal data if it's reasonably necessary to meet any applicable law, regulation, legal process, enforceable governmental request or otherwise required by law.

**3. Security**

We work hard to protect the data we handle from unauthorized access, modification, disclosure, or destruction.

**4. Privacy Policy Changes**

We may update our Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page. 
You are advised to review this page periodically for any changes. Changes to this Privacy Policy are effective when they are posted on this page.

**5. Contact Us**

If you have any questions or concerns about this privacy policy, please contact us at info@tai-tutor.team.
"""
@ROUTER.get("/privacy-policy", include_in_schema=False)
def privacy_policy():
    """Return the privacy policy."""
    return PRIVACY_POLICY

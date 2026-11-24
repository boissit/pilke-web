import os
import secrets
from datetime import datetime
from zoneinfo import ZoneInfo

from django.utils.timezone import now

from treffit_backend.identity.models import UserVerification
from treffit_backend.identity.providers.base import SubjectKind
from treffit_backend.testers.services.forcing import force_agreed_date
from treffit_backend.users.models import User
from treffit_backend.venues.models import Venue

SCENARIO = os.environ["SCENARIO"]
HKI = ZoneInfo("Europe/Helsinki")
viewer = User.objects.get(nickname="Vieno")


def verify(user):
    UserVerification.objects.update_or_create(
        user=user,
        defaults=dict(
            verified_at=now(),
            provider="didit",
            is_adult=True,
            identity_hash=secrets.token_bytes(32),
            hash_key_id="dev",
            subject_kind=SubjectKind.PROVIDER_SUB,
            badge_removed_at=None,
        ),
    )


if SCENARIO == "verify":
    # Everybody in the cast verified, so any platter shows three badges.
    for user in User.objects.exclude(pk=1):
        verify(user)
    print("verified", UserVerification.objects.count())

if SCENARIO == "dates":
    riikka = User.objects.get(nickname="Riikka")
    henri = User.objects.get(nickname="Henri")
    aalto = Venue.objects.get(name="Café Aalto")
    espa = Venue.objects.get(name="Esplanadin puisto")
    print(force_agreed_date(riikka, viewer, [aalto], [datetime(2026, 11, 27, 17, tzinfo=HKI)], notify=False))
    print(force_agreed_date(henri, viewer, [espa], [datetime(2026, 11, 28, 13, tzinfo=HKI)], notify=False))

if SCENARIO.startswith("lang-"):
    viewer.language = SCENARIO[5:]
    viewer.save(update_fields=["language"])
    print("language", viewer.language)

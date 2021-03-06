from datetime import date
from uuid import UUID

from atlas import factories
from atlas.root_schema import schema
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
import graphene.test
import pytest


def pytest_configure(config):
    settings.GOOGLE_CLIENT_ID = "google-client-id"
    settings.GOOGLE_CLIENT_SECRET = "google-client-secret"


class Context(object):
    user = AnonymousUser()


class GqlClient(graphene.test.Client):
    def execute(self, query, variables=None, user=None, files=None):
        context = Context()
        if user:
            context.user = user
        context.FILES = files or {}
        return super().execute(query, variables=variables, context=context)


@pytest.fixture
def gql_client(db):
    return GqlClient(schema)


@pytest.fixture
def default_office(db):
    return factories.OfficeFactory.create(
        id=UUID("d2b00771-086f-4fc1-b24c-f5cc7bcd2c78"), name="SFO", external_id="SFO"
    )


@pytest.fixture
def design_department(db):
    return factories.DepartmentFactory.create(
        id=UUID("624f950b-a57e-4d81-83bf-f50ea0ff2545"), name="Design", cost_center=200
    )


@pytest.fixture
def default_team(db):
    return factories.TeamFactory.create(
        id=UUID("20a2cfc3-8f6a-47d1-9ad1-44e7e2fed32b"), name="Workflow"
    )


@pytest.fixture
def performance_team(db):
    return factories.TeamFactory.create(
        id=UUID("f33ebcbf-3fd5-4e0b-9786-a64807c1d232"), name="Performance"
    )


@pytest.fixture
def creative_department(design_department):
    return factories.DepartmentFactory(
        id=UUID("955ed539-750a-400c-8e88-cf60f471f16b"),
        name="Creative",
        parent=design_department,
        tree=(design_department.tree or []) + [design_department.id],
        cost_center=220,
    )


@pytest.fixture
def ga_department(db):
    return factories.DepartmentFactory.create(
        id=UUID("12a1120e-07a8-4d4b-aa94-a74694aa0b85"), name="G&A", cost_center=100
    )


@pytest.fixture
def default_user(db, design_department, default_team):
    user = factories.UserFactory(
        id=UUID("449c76aa-ad6a-46a8-b32b-91d965e3f462"),
        name="Jane Doe",
        email="jane@example.com",
    )
    user.set_password("phish.reel.big")
    user.save()

    factories.ProfileFactory.create(
        user=user,
        title="Dummy",
        date_started=date(2010, 4, 26),
        date_of_birth=date(1920, 8, 12),
        department=design_department,
        team=default_team,
        office=None,
        reports_to=None,
        referred_by=None,
        employee_type="FULL_TIME",
        has_onboarded=True,
    )
    return user


@pytest.fixture
def default_identity(db, default_user):
    return factories.IdentityFactory.create(user=default_user, external_id="100000000")


@pytest.fixture
def default_superuser(db, ga_department, default_team):
    user = factories.UserFactory(
        id=UUID("559c76aa-ad6a-46a8-b32b-91d965e3f462"),
        name="Captain Planet",
        email="captain.planet@example.com",
        is_superuser=True,
    )
    user.set_password("planet.captain")
    user.save()

    factories.ProfileFactory.create(
        user=user,
        title="Super Dummy",
        date_started=date(2010, 5, 26),
        date_of_birth=date(1900, 2, 13),
        department=ga_department,
        team=default_team,
        office=None,
        employee_type="FULL_TIME",
        reports_to=None,
        referred_by=None,
        has_onboarded=True,
    )
    return user


@pytest.fixture
def default_superuser_identity(db, default_superuser):
    return factories.IdentityFactory.create(
        user=default_superuser, admin=True, external_id="100000001"
    )

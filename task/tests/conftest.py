import base64

import pytest

from user.models import User
from rest_framework.test import APIClient

from task.models import Task as Todo


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="anshu",
        email="anshu@example.com",
        password="test-password"
    )


@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        username="rahul",
        email="rahul@example.com",
        password="test-password"
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):

    credentials = base64.b64encode(
        b"anshu:test-password"
    ).decode("utf-8")

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Basic {credentials}"
    )

    return api_client


@pytest.fixture
def todo(user):

    return Todo.objects.create(
        user=user,
        title="Learn Django REST Framework",
        description="Learn APIView",
        status=Todo.Status.PENDING
    )


@pytest.fixture
def another_user_todo(another_user):

    return Todo.objects.create(
        user=another_user,
        title="Private task",
        description="This belongs to another user",
        status=Todo.Status.PENDING
    )
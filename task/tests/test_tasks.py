import pytest

from django.contrib.auth.models import User

from rest_framework import status

from task.models import Task as Todo


BASE_URL = "/api/v1/todos/"


# ------------------------------------------------
# Authentication Tests
# ------------------------------------------------

@pytest.mark.django_db
def test_unauthenticated_user_cannot_list_tasks(api_client):

    response = api_client.get(BASE_URL)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_invalid_credentials_are_rejected(api_client):

    api_client.credentials(
        HTTP_AUTHORIZATION="Basic aW52YWxpZDppbnZhbGlk"
    )

    response = api_client.get(BASE_URL)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ------------------------------------------------
# CREATE Tests
# ------------------------------------------------

@pytest.mark.django_db
def test_user_can_create_task(authenticated_client, user):

    payload = {
        "title": "Learn pytest",
        "description": "Write automated tests",
        "status": "pending"
    }

    response = authenticated_client.post(
        BASE_URL,
        payload,
        format="json"
    )

    assert response.status_code == status.HTTP_201_CREATED

    assert response.data["title"] == "Learn pytest"

    task = Todo.objects.get(title="Learn pytest")

    assert task.user == user
    assert task.status == Todo.Status.PENDING


@pytest.mark.django_db
def test_task_owner_is_taken_from_authenticated_user(
    authenticated_client,
    user,
    another_user
):

    payload = {
        "title": "My task",
        "user": another_user.id
    }

    response = authenticated_client.post(
        BASE_URL,
        payload,
        format="json"
    )

    assert response.status_code == status.HTTP_201_CREATED

    task = Todo.objects.get(title="My task")

    assert task.user == user
    assert task.user != another_user


@pytest.mark.django_db
def test_task_creation_requires_title(authenticated_client):

    response = authenticated_client.post(
        BASE_URL,
        {
            "description": "Task without title"
        },
        format="json"
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_task_creation_rejects_invalid_status(authenticated_client):

    response = authenticated_client.post(
        BASE_URL,
        {
            "title": "Invalid task",
            "status": "invalid"
        },
        format="json"
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_task_creation_rejects_blank_title(authenticated_client):

    response = authenticated_client.post(
        BASE_URL,
        {
            "title": "   "
        },
        format="json"
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


# ------------------------------------------------
# LIST Tests
# ------------------------------------------------

@pytest.mark.django_db
def test_user_can_list_own_tasks(
    authenticated_client,
    user,
    another_user
):

    Todo.objects.create(
        user=user,
        title="My task"
    )

    Todo.objects.create(
        user=another_user,
        title="Other user task"
    )

    response = authenticated_client.get(BASE_URL)

    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 1

    assert response.data[0]["title"] == "My task"


@pytest.mark.django_db
def test_user_gets_empty_list_without_tasks(authenticated_client):

    response = authenticated_client.get(BASE_URL)

    assert response.status_code == status.HTTP_200_OK

    assert response.data == []


# ------------------------------------------------
# RETRIEVE Tests
# ------------------------------------------------

@pytest.mark.django_db
def test_user_can_retrieve_own_task(
    authenticated_client,
    todo
):

    response = authenticated_client.get(
        f"{BASE_URL}{todo.id}/"
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.data["id"] == todo.id
    assert response.data["title"] == todo.title


@pytest.mark.django_db
def test_user_cannot_retrieve_other_users_task(
    authenticated_client,
    another_user_todo
):

    response = authenticated_client.get(
        f"{BASE_URL}{another_user_todo.id}/"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_retrieve_nonexistent_task_returns_404(authenticated_client):

    response = authenticated_client.get(
        f"{BASE_URL}9999/"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


# ------------------------------------------------
# PUT Tests
# ------------------------------------------------

@pytest.mark.django_db
def test_user_can_update_task(
    authenticated_client,
    todo
):

    payload = {
        "title": "Updated task",
        "description": "Updated description",
        "status": "in_progress"
    }

    response = authenticated_client.put(
        f"{BASE_URL}{todo.id}/",
        payload,
        format="json"
    )

    assert response.status_code == status.HTTP_200_OK

    todo.refresh_from_db()

    assert todo.title == "Updated task"
    assert todo.description == "Updated description"
    assert todo.status == Todo.Status.IN_PROGRESS


@pytest.mark.django_db
def test_put_requires_all_required_fields(
    authenticated_client,
    todo
):

    response = authenticated_client.put(
        f"{BASE_URL}{todo.id}/",
        {
            "title": "Only title"
        },
        format="json"
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


# ------------------------------------------------
# PATCH Tests
# ------------------------------------------------

@pytest.mark.django_db
def test_user_can_partially_update_task(
    authenticated_client,
    todo
):

    response = authenticated_client.patch(
        f"{BASE_URL}{todo.id}/",
        {
            "status": "completed"
        },
        format="json"
    )

    assert response.status_code == status.HTTP_200_OK

    todo.refresh_from_db()

    assert todo.status == Todo.Status.COMPLETED

    assert todo.title == "Learn Django REST Framework"


@pytest.mark.django_db
def test_patch_rejects_invalid_status(
    authenticated_client,
    todo
):

    response = authenticated_client.patch(
        f"{BASE_URL}{todo.id}/",
        {
            "status": "unknown"
        },
        format="json"
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


# ------------------------------------------------
# DELETE Tests
# ------------------------------------------------

@pytest.mark.django_db
def test_user_can_delete_own_task(
    authenticated_client,
    todo
):

    response = authenticated_client.delete(
        f"{BASE_URL}{todo.id}/"
    )

    assert response.status_code == status.HTTP_200_OK

    assert not Todo.objects.filter(
        id=todo.id
    ).exists()


@pytest.mark.django_db
def test_user_cannot_delete_other_users_task(
    authenticated_client,
    another_user_todo
):

    response = authenticated_client.delete(
        f"{BASE_URL}{another_user_todo.id}/"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    assert Todo.objects.filter(
        id=another_user_todo.id
    ).exists()
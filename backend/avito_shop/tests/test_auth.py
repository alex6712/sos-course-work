import pytest


@pytest.mark.asyncio
async def test_sign_up_success(async_client):
    response = await async_client.post(
        "/auth/sign_up",
        json={
            "username": "test_user",
            "email": "test@example.com",
            "phone": "+7 910 000-00-01",
            "password": "SignUpPass",
        },
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Employee created successfully."


@pytest.mark.asyncio
async def test_sign_up_duplicate(async_client):
    await async_client.post(
        "/auth/sign_up",
        json={
            "username": "duplicate_user",
            "email": "duplicate@example.com",
            "phone": "+7 910 000-00-02",
            "password": "DuplicatePass",
        },
    )

    response = await async_client.post(
        "/auth/sign_up",
        json={
            "username": "duplicate_user",
            "email": "duplicate@example.com",
            "phone": "+7 910 000-00-02",
            "password": "DuplicatePass",
        },
    )

    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_sign_in_success(async_client):
    await async_client.post(
        "/auth/sign_up",
        json={
            "username": "sign_in_user",
            "email": "sign_in@example.com",
            "phone": "+7 910 000-00-03",
            "password": "SignInPass",
        },
    )

    response = await async_client.post(
        "/auth/sign_in",
        data={
            "username": "sign_in_user",
            "password": "SignInPass",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_sign_in_wrong_password(async_client):
    await async_client.post(
        "/auth/sign_up",
        json={
            "username": "wrong_pass_user",
            "email": "wrong_pass@example.com",
            "phone": "+7 910 000-00-04",
            "password": "CorrectPass",
        },
    )

    response = await async_client.post(
        "/auth/sign_in",
        data={
            "username": "wrong_pass_user",
            "password": "WrongPass",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token_success(async_client):
    await async_client.post(
        "/auth/sign_up",
        json={
            "username": "refresh_user",
            "email": "refresh@example.com",
            "phone": "+7 910 000-00-05",
            "password": "RefreshPass",
        },
    )
    sign_in = await async_client.post(
        "/auth/sign_in", data={"username": "refresh_user", "password": "RefreshPass"}
    )

    refresh_token = sign_in.json()["refresh_token"]

    response = await async_client.get(
        "/auth/refresh", headers={"Authorization": f"Bearer {refresh_token}"}
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_refresh_token_invalid(async_client):
    response = await async_client.get(
        "/auth/refresh", headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 401

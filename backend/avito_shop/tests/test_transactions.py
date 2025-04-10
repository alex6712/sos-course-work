import pytest


@pytest.mark.asyncio
async def test_send_coins_success(async_client):
    await async_client.post(
        "/auth/sign_up",
        json={
            "username": "sender_success",
            "email": "sender_success@example.com",
            "phone": "+7 911 000-00-01",
            "password": "SenderSuccessPass",
        },
    )

    sign_in_response = await async_client.post(
        "/auth/sign_in",
        data={
            "username": "sender_success",
            "password": "SenderSuccessPass",
        },
    )
    access_token: str = sign_in_response.json()["access_token"]

    gainer_username: str = "gainer_success"

    await async_client.post(
        "/auth/sign_up",
        json={
            "username": gainer_username,
            "email": "gainer_success@example.com",
            "phone": "+7 911 000-00-02",
            "password": "GainerSuccessPass",
        },
    )

    response = await async_client.post(
        "/transactions/send_coins",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "gainer_username": gainer_username,
            "coins_amount": 100.0,
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Монеты успешно отправлены."


@pytest.mark.asyncio
async def test_send_coins_negative(async_client):
    await async_client.post(
        "/auth/sign_up",
        json={
            "username": "sender_negative",
            "email": "sender_negative@example.com",
            "phone": "+7 911 000-00-03",
            "password": "SenderNegativePass",
        },
    )

    sign_in_response = await async_client.post(
        "/auth/sign_in",
        data={
            "username": "sender_negative",
            "password": "SenderNegativePass",
        },
    )
    access_token: str = sign_in_response.json()["access_token"]

    gainer_username: str = "gainer_negative"

    await async_client.post(
        "/auth/sign_up",
        json={
            "username": gainer_username,
            "email": "gainer_negative@example.com",
            "phone": "+7 911 000-00-04",
            "password": "GainerNegativePass",
        },
    )

    response = await async_client.post(
        "/transactions/send_coins",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "gainer_username": gainer_username,
            "coins_amount": -1.0,
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Количество монет не может быть отрицательным или равным нулю."
    )


@pytest.mark.asyncio
async def test_send_coins_not_enough(async_client):
    await async_client.post(
        "/auth/sign_up",
        json={
            "username": "sender_not_enough",
            "email": "sender_not_enough@example.com",
            "phone": "+7 911 000-00-05",
            "password": "SenderNotEnoughPass",
        },
    )

    sign_in_response = await async_client.post(
        "/auth/sign_in",
        data={
            "username": "sender_not_enough",
            "password": "SenderNotEnoughPass",
        },
    )
    access_token: str = sign_in_response.json()["access_token"]

    gainer_username: str = "gainer_not_enough"

    await async_client.post(
        "/auth/sign_up",
        json={
            "username": gainer_username,
            "email": "gainer_not_enough@example.com",
            "phone": "+7 911 000-00-06",
            "password": "GainerNotEnoughPass",
        },
    )

    response = await async_client.post(
        "/transactions/send_coins",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "gainer_username": gainer_username,
            "coins_amount": 1_000_000.0,
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Невозможно выполнить перевод, т.к. на счёте недостаточно средств."
    )


@pytest.mark.asyncio
async def test_send_coins_to_me(async_client):
    await async_client.post(
        "/auth/sign_up",
        json={
            "username": "sender_to_me",
            "email": "sender_to_me@example.com",
            "phone": "+7 911 000-00-07",
            "password": "SenderToMePass",
        },
    )

    sign_in_response = await async_client.post(
        "/auth/sign_in",
        data={
            "username": "sender_to_me",
            "password": "SenderToMePass",
        },
    )
    access_token: str = sign_in_response.json()["access_token"]

    gainer_username: str = "sender_to_me"

    response = await async_client.post(
        "/transactions/send_coins",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "gainer_username": gainer_username,
            "coins_amount": 10.0,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Отправитель и получатель не могут совпадать."

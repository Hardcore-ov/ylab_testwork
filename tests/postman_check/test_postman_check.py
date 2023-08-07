import pytest
from httpx import AsyncClient

from tests.test_data import (
    dish_data,
    dish_data_second,
    dish_keys,
    menu_data,
    menu_keys,
    submenu_data,
    submenu_keys,
)


class TestPostman:

    async def test_create_menu(self, async_client: AsyncClient):

        response = await async_client.post('/api/v1/menus/',
                                           json=menu_data)
        resp_data = response.json()
        pytest.shared = resp_data['id']
        assert (sorted(list(resp_data.keys())) == menu_keys)
        assert response.status_code == 201
        assert resp_data['title'] == menu_data['title']
        assert resp_data['description'] == menu_data['description']
        assert resp_data['submenus_count'] == 0
        assert resp_data['dishes_count'] == 0

    async def test_create_submenu(self, async_client: AsyncClient):
        menu_id = await async_client.get('/api/v1/menus/')
        menu_id = menu_id.json()[0]['id']
        response = await async_client.post(f'/api/v1/menus/{pytest.shared}/submenus/',
                                           json=submenu_data)
        resp_data = response.json()
        submenu_id = resp_data['id']
        assert response.status_code == 201
        assert menu_id == pytest.shared
        assert sorted(list(resp_data.keys())) == submenu_keys
        assert resp_data['title'] == submenu_data['title']
        assert resp_data['description'] == submenu_data['description']
        assert resp_data['dishes_count'] == 0
        pytest.shared = [menu_id, submenu_id]

    async def test_create_dishes(self, async_client: AsyncClient):

        response = await async_client.post(f'/api/v1/menus/{pytest.shared[0]}/submenus/{pytest.shared[1]}/dishes/',
                                           json=dish_data)
        resp_data = response.json()
        assert response.status_code == 201
        assert sorted(list(resp_data.keys())) == dish_keys
        assert resp_data['title'] == dish_data['title']
        assert resp_data['description'] == dish_data['description']
        assert resp_data['price'] == dish_data['price']

        response = await async_client.post(f'/api/v1/menus/{pytest.shared[0]}/submenus/{pytest.shared[1]}/dishes/',
                                           json=dish_data_second)
        resp_data = response.json()
        assert response.status_code == 201
        assert sorted(list(resp_data.keys())) == dish_keys
        assert resp_data['title'] == dish_data_second['title']
        assert resp_data['description'] == dish_data_second['description']
        assert resp_data['price'] == dish_data_second['price']

    async def test_get_menu(self, async_client: AsyncClient):

        response = await async_client.get(f'/api/v1/menus/{pytest.shared[0]}')
        resp_data = response.json()
        assert response.status_code == 200
        assert sorted(list(resp_data.keys())) == menu_keys
        assert resp_data['id'] == pytest.shared[0]
        assert resp_data['description'] == menu_data['description']
        assert resp_data['title'] == menu_data['title']
        assert resp_data['submenus_count'] == 1
        assert resp_data['dishes_count'] == 2

    async def test_get_submenu_by_id(self, async_client: AsyncClient):

        response = await async_client.get(f'/api/v1/menus/{pytest.shared[0]}/submenus/{pytest.shared[1]}')
        resp_data = response.json()
        assert response.status_code == 200
        assert sorted(list(resp_data.keys())) == submenu_keys
        assert resp_data['id'] == pytest.shared[1]
        assert resp_data['description'] == submenu_data['description']
        assert resp_data['title'] == submenu_data['title']
        assert resp_data['dishes_count'] == 2

    async def test_delete_submenu(self, async_client: AsyncClient):

        response = await async_client.delete(f'/api/v1/menus/{pytest.shared[0]}/submenus/{pytest.shared[1]}')
        resp_data = response.json()
        assert response.status_code == 200
        assert resp_data['status'] is True
        assert resp_data['message'] == 'The submenu has been deleted'

    async def test_get_submenu_list(self, async_client: AsyncClient):

        response = await async_client.get(f'/api/v1/menus/{pytest.shared[0]}/submenus/')
        assert response.status_code == 200
        resp_data = response.json()
        assert resp_data == []

    async def test_get_dish_list(self, async_client: AsyncClient):

        response = await async_client.get(f'/api/v1/menus/{pytest.shared[0]}/submenus/{pytest.shared[1]}/dishes/')
        print(response.json())
        assert response.status_code == 200
        resp_data = response.json()
        assert resp_data == []

    async def test_get_menu_by_id(self, async_client: AsyncClient):

        response = await async_client.get(f'/api/v1/menus/{pytest.shared[0]}')
        resp_data = response.json()
        assert response.status_code == 200
        assert sorted(list(resp_data.keys())) == menu_keys
        assert resp_data['id'] == pytest.shared[0]
        assert resp_data['description'] == menu_data['description']
        assert resp_data['title'] == menu_data['title']
        assert resp_data['submenus_count'] == 0
        assert resp_data['dishes_count'] == 0

    async def test_delete_menu(self, async_client: AsyncClient):

        response = await async_client.delete(f'/api/v1/menus/{pytest.shared[0]}')
        resp_data = response.json()
        assert response.status_code == 200
        assert resp_data['status'] is True
        assert resp_data['message'] == 'The menu has been deleted'

    async def test_get_menu_list(self, async_client: AsyncClient, clear_db):

        response = await async_client.get('/api/v1/menus/')
        print(response.json())
        assert response.status_code == 200
        resp_data = response.json()
        assert resp_data == []

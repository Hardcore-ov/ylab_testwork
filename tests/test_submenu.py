from typing import Coroutine

from httpx import AsyncClient

from src.menu.models import Menu
from src.submenu.models import Submenu
from tests.test_data import (
    submenu_data,
    submenu_keys,
    updated_menu_data,
    updated_submenu_data,
)


class TestSubmenu:
    async def test_create_submenu(self, clear_db: Coroutine, async_client: AsyncClient, create_menu: Menu):

        menu = create_menu
        response = await async_client.post(f'/api/v1/menus/{menu.id}/submenus/',
                                           json=submenu_data)
        resp_data = response.json()
        assert response.status_code == 201
        assert sorted(list(resp_data.keys())) == submenu_keys
        assert resp_data['title'] == submenu_data['title']
        assert resp_data['description'] == submenu_data['description']
        assert resp_data['dishes_count'] == 0

    async def test_get_submenu_list(self, clear_db: Coroutine, async_client: AsyncClient, create_submenu: Submenu):

        submenu = create_submenu
        response = await async_client.get(f'/api/v1/menus/{submenu.menu_id}/submenus/')
        assert response.status_code == 200
        subresp_data = response.json()
        assert isinstance(subresp_data, list)
        assert len(subresp_data) == 1

    async def test_get_empty_submenu_list(self, clear_db: Coroutine, async_client: AsyncClient, create_menu: Menu):

        menu = create_menu
        response = await async_client.get(f'/api/v1/menus/{menu.id}/submenus/')
        assert response.status_code == 200
        resp_data = response.json()
        assert resp_data == []

    async def test_get_submenu_by_id(self, clear_db: Coroutine, async_client: AsyncClient, create_submenu: Submenu):

        submenu = create_submenu
        response = await async_client.get(f'/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}')
        resp_data = response.json()
        assert response.status_code == 200
        assert sorted(list(resp_data.keys())) == submenu_keys
        assert resp_data['title'] == submenu_data['title']
        assert resp_data['description'] == submenu_data['description']
        assert resp_data['dishes_count'] == 0

    async def test_get_submenu_not_found(self, clear_db: Coroutine, async_client: AsyncClient, create_menu: Menu):

        menu = create_menu
        submenu_id = 'fake_id'
        response = await async_client.get(f'/api/v1/menus/{menu.id}/submenus/{submenu_id}')
        assert response.status_code == 404
        resp_data = response.json()
        assert resp_data['detail'] == 'submenu not found'

    async def test_update_submenu(self, clear_db: Coroutine, async_client: AsyncClient, create_submenu: Submenu):

        submenu = create_submenu
        response = await async_client.patch(f'/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}',
                                            json=updated_submenu_data)
        resp_data = response.json()
        assert response.status_code == 200
        assert sorted(list(resp_data.keys())) == submenu_keys
        assert resp_data['title'] == updated_submenu_data['title']
        assert resp_data['description'] == updated_submenu_data['description']
        assert resp_data['dishes_count'] == 0

    async def test_patch_submenu_not_found(self, clear_db: Coroutine, async_client: AsyncClient, create_menu: Menu):

        menu = create_menu
        submenu_id = 'fake_id'
        response = await async_client.patch(f'/api/v1/menus/{menu.id}/submenus/{submenu_id}',
                                            json=updated_menu_data)
        assert response.status_code == 404
        resp_data = response.json()
        assert resp_data['detail'] == 'submenu not found'

    async def test_delete_submenu(self, clear_db: Coroutine, async_client: AsyncClient, create_submenu: Submenu):

        submenu = create_submenu
        response = await async_client.delete(f'/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}')
        resp_data = response.json()
        assert response.status_code == 200
        assert resp_data['status'] is True
        assert resp_data['message'] == 'The submenu has been deleted'
        deleted_resp = await async_client.get(f'/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}')
        assert deleted_resp.status_code == 404

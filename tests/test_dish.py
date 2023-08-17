from httpx import AsyncClient

from src.menu.models import Menu
from src.submenu.models import Submenu
from tests.conftest import db
from tests.test_data import dish_data, dish_keys, updated_dish_data


class TestDish:
    async def test_create_dish(self, clear_db, async_client: AsyncClient, create_submenu):
        submenu = create_submenu
        menu_id = submenu.__getattribute__('menu_id')
        submenu_id = submenu.__getattribute__('id')
        response = await async_client.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/',
                                           json=dish_data)
        resp_data = response.json()
        assert response.status_code == 201
        assert sorted(list(resp_data.keys())) == dish_keys
        assert resp_data['title'] == dish_data['title']
        assert resp_data['description'] == dish_data['description']
        assert resp_data['price'] == dish_data['price']

    async def test_get_dish_list(self, clear_db, async_client: AsyncClient, create_dish):
        menu = db.query(Menu).first()
        submenu = db.query(Submenu).filter_by(menu_id=menu.id).first()
        response = await async_client.get(f'/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/')
        assert response.status_code == 200
        resp_data = response.json()
        assert isinstance(resp_data, list)
        assert len(resp_data) == 1

    async def test_get_empty_dish_list(self, clear_db, async_client: AsyncClient, create_submenu):

        submenu = create_submenu
        response = await async_client.get(f'/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}/dishes/')
        assert response.status_code == 200
        resp_data = response.json()
        assert resp_data == []

    async def test_get_dish_by_id(self, clear_db, async_client: AsyncClient, create_dish):

        dish = create_dish
        menu = db.query(Menu).first()
        submenu = db.query(Submenu).filter_by(menu_id=menu.id).first()
        response = await async_client.get(f'/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}')
        resp_data = response.json()
        assert response.status_code == 200
        assert sorted(list(resp_data.keys())) == dish_keys
        assert resp_data['title'] == dish_data['title']
        assert resp_data['description'] == dish_data['description']
        assert resp_data['price'] == dish_data['price']

    async def test_get_dish_not_found(self, clear_db, async_client: AsyncClient, create_submenu):

        submenu = create_submenu
        dish_id = 'fake_id'
        subresp = await async_client.get(f'/api/v1/menus/{submenu.menu_id}/submenus/' f'{submenu.id}/dishes/{dish_id}')
        assert subresp.status_code == 404
        resp_data = subresp.json()
        assert resp_data['detail'] == 'dish not found'

    async def test_update_dish(self, clear_db, async_client: AsyncClient, create_dish):

        dish = create_dish
        menu = db.query(Menu).first()
        submenu = db.query(Submenu).filter_by(menu_id=menu.id).first()
        response = await async_client.patch(f'/api/v1/menus/{menu.id}/submenus/' f'{submenu.id}/dishes/{dish.id}',
                                            json=updated_dish_data)
        resp_data = response.json()
        assert response.status_code == 200
        assert sorted(list(resp_data.keys())) == dish_keys
        assert resp_data['title'] == updated_dish_data['title']
        assert resp_data['description'] == updated_dish_data['description']
        assert resp_data['price'] == updated_dish_data['price']

    async def test_patch_dish_not_found(self, clear_db, async_client: AsyncClient, create_submenu):

        submenu = create_submenu
        dish_id = 'fake_id'
        response = await async_client.patch(f'/api/v1/menus/{submenu.menu_id}/submenus/' f'{submenu.id}/dishes/{dish_id}',
                                            json=updated_dish_data)
        assert response.status_code == 404
        resp_data = response.json()
        assert resp_data['detail'] == 'dish not found'

    async def test_delete_dish(self, clear_db, async_client: AsyncClient, create_dish):

        dish = create_dish
        menu = db.query(Menu).first()
        submenu = db.query(Submenu).filter_by(menu_id=menu.id).first()
        response = await async_client.delete(f'/api/v1/menus/{menu.id}/submenus/' f'{submenu.id}/dishes/{dish.id}')
        resp_data = response.json()
        assert response.status_code == 200
        assert resp_data['status'] is True
        assert resp_data['message'] == 'The dish has been deleted'
        deleted_resp = await async_client.get(f'/api/v1/menus/{menu.id}/submenus/' f'{submenu.id}/dishes/{dish.id}')
        assert deleted_resp.status_code == 404

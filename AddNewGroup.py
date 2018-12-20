# -*- coding: utf-8 -*-
from application import Application
import pytest
from group import Group

@pytest.fixture()
def app(request):
    fixture = Application()
    request.addfinalizer(fixture.destroy)
    return fixture

def test_add_group(app):
    app.login(username="admin", password="secret")
    app.create_new_group(Group(name="NewGroup1", header="NewGroupHeader", footer="NewGroupFooter"))
    app.logout()

def test_add_empty_group(app):
    app.login(username="admin", password="secret")
    app.create_new_group(Group(name="", header="", footer=""))
    app.logout()
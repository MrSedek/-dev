from datetime import datetime
from model.group import Group
from model.contact import Contact
from pony.orm import *
from pymysql.converters import decoders

class ORMFixture:

    db = Database()
    class ORMGroup(db.Entity):
        _table_ = 'group_list'
        id = PrimaryKey(int, column='group_id')
        name = Optional(str, column='group_name')
        header = Optional(str, column='group_header')
        footer = Optional(str, column='group_footer')

    class ORMContact(db.Entity):
        _table_ = 'addressbook'
        id = PrimaryKey(int, column='id')
        firstname = Optional(str, column='firstname')
        lastname = Optional(str, column='lastname')
        deprecated = Optional(datetime, column='deprecated')

    def __init__(self, host, name, user, password):
        self.db.bind('mysql', host=host, name=name, user=user, password=password, conv=decoders)
        self.db.generate_mapping()
        sql_debug(True) # don't work

    @db_session
    def get_group_list(self):
        return self.conver_groups_to_model(select(g for g in ORMFixture.ORMGroup))

    def conver_groups_to_model(self, groups):
        def convert(group):
            return Group(id=str(group.id), name=group.name, header=group.header, footer=group.footer)
        return list(map(convert, groups))

    def get_contact_list(self):
        return self.conver_contacts_to_model(select(c for c in ORMFixture.ORMContact if c.deprecated is None))

    def conver_contacts_to_model(self):
        def convert(contact):
            return Contact(id=str(contact.id), firstname=contact.firstname, lastname=contact.lastname)

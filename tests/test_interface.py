from debile.master.dimport import dimport
from debile.master.interface import DebileMasterInterface, NAMESPACE
from debile.master.orm import Base, Builder, Person

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
import unittest


class DebileInterfaceTestCase(unittest.TestCase):
    # setup the database
    if 'DATABASE_URI' in os.environ:
        db_URI = os.environ['DATABASE_URI']
    else:
        # See README.md for the doc
        db_URI = 'postgres://debile:foobar@127.0.0.1:5432/debile_tests'
    engine = create_engine(db_URI,
                            implicit_returning=False)

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    session = Session()
    Base.metadata.drop_all(session.bind)

    # feed database
    class Args:
        pass
    args = Args()
    args.file = 'tests/resources/debile.yaml'
    args.force = False
    dimport(args, session)

    # some more setting up
    u = session.query(Person).filter_by(
        email='clement@mux.me'
    ).first()
    NAMESPACE.user = u


    def setUp(self):
        self.blade01_key = None
        with open('tests/resources/blade01.pgp') as f:
            self.blade01_key = f.read()

        self.interface = DebileMasterInterface(pgp_keyring=u'tests/resources/keyring')
        NAMESPACE.session = self.session


    def tearDown(self):
        for f in ('tests/resources/keyring', 'tests/resources/secret-keyring'):
            if os.path.exists(f):
                os.remove(f)


    def test_create_builder(self):
        self.interface.create_builder('blade01', self.blade01_key, ip='10.0.0.1')

        b = self.session.query(Builder).filter_by(name='blade01').one()

        assert b.ssl is None
        assert b.ip == '10.0.0.1'
        assert b.pgp == '7C367D02AF6D20DCF2BFB686E8D62122F818733D'


    def test_create_user_with_simple_auth(self):
        self.interface.create_user('John', 'john@example.org', self.blade01_key,
                ssl=None, ip='10.0.0.1')

        p = self.session.query(Person).filter_by(name='John').first()

        self.assertEquals(p.name, 'John')
        self.assertEquals(p.email, 'john@example.org')
        self.assertEquals(p.pgp, '7C367D02AF6D20DCF2BFB686E8D62122F818733D')
        self.assertEquals(p.ip, '10.0.0.1')
        self.assertIsNone(p.ssl)

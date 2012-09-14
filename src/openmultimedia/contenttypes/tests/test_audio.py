# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility, queryMultiAdapter

from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IAttributeUUID

from plone.app.referenceablebehavior.referenceable import IReferenceable

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from openmultimedia.contenttypes.content.audio import IAudio
from openmultimedia.contenttypes.testing import INTEGRATION_TESTING


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('openmultimedia.contenttypes.audio', 'v1')
        self.v1 = self.folder['v1']

    def test_adding(self):
        self.assertTrue(IAudio.providedBy(self.v1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='openmultimedia.contenttypes.audio')
        self.assertNotEqual(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='openmultimedia.contenttypes.audio')
        schema = fti.lookupSchema()
        self.assertEqual(IAudio, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='openmultimedia.contenttypes.audio')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IAudio.providedBy(new_object))

    def test_is_referenceable(self):
        self.assertTrue(IReferenceable.providedBy(self.v1))
        self.assertTrue(IAttributeUUID.providedBy(self.v1))

    def test_view(self):
        view = queryMultiAdapter((self.v1, self.request), name='view')
        self.assertTrue(view is not None)

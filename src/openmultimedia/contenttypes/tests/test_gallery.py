# -*- coding: utf-8 -*-

from openmultimedia.contenttypes.content.gallery import IGallery
from openmultimedia.contenttypes.testing import INTEGRATION_TESTING
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IAttributeUUID
from zope.component import createObject
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from zope.interface import directlyProvides

import pkg_resources
import unittest2 as unittest

# XXX: just to keep compatibility with collective.nitf 1.0a3 and Plone 4.1
PLONE_VERSION = pkg_resources.require("Plone")[0].version
if '4.1' in PLONE_VERSION:
    from collective.nitf.interfaces import INITFBrowserLayer as INITFLayer
else:
    from collective.nitf.interfaces import INITFLayer


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, INITFLayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory(
            'openmultimedia.contenttypes.gallery',
            'g1',
            description="gallery desctiption",
        )
        self.g1 = self.folder['g1']

    def test_adding(self):
        self.assertTrue(IGallery.providedBy(self.g1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='openmultimedia.contenttypes.gallery')
        self.assertNotEqual(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='openmultimedia.contenttypes.gallery')
        schema = fti.lookupSchema()
        self.assertEqual(IGallery, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='openmultimedia.contenttypes.gallery')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IGallery.providedBy(new_object))

    def test_is_referenceable(self):
        self.assertTrue(IReferenceable.providedBy(self.g1))
        self.assertTrue(IAttributeUUID.providedBy(self.g1))

    def test_image_description(self):
        """
        Here we test that calling image.Description() on an image that doesn't
        have a description. doesn't bring the parent description.
        """
        self.g1.invokeFactory('Image', id="image1", description="image description test")
        self.g1.invokeFactory('Image', id="image2")
        image1 = self.g1['image1']
        image2 = self.g1['image2']
        self.assertTrue(image1.Description() == "image description test")
        self.assertTrue(image2.Description() == "")
        #its diferent from the parent description
        self.assertTrue(image2.Description() != "gallery desctiption")

    def test_view(self):
        view = queryMultiAdapter((self.g1, self.request), name='view')
        self.assertTrue(view is not None)

    def test_view_get_description(self):
        self.g1.invokeFactory('Image', id="image1", description="image description test")
        self.g1.invokeFactory('Image', id="image2")
        image1 = self.g1['image1']
        image2 = self.g1['image2']
        view = queryMultiAdapter((self.g1, self.request), name='view')
        image1_desc = view.get_description(image1)
        image2_desc = view.get_description(image2)
        self.assertTrue(image1_desc == "image description test")
        self.assertTrue(image2_desc == "gallery desctiption")

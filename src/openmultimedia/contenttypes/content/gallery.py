# -*- coding: utf-8 -*-
from five import grok

from zope import schema
from zope.component import getUtility

from plone.app.textfield import RichText

from plone.directives import form

from plone.dexterity.content import Container

from plone.registry.interfaces import IRegistry

from Products.CMFPlone.interfaces import INonStructuralFolder

from collective.nitf import _
from collective.nitf import config
from collective.nitf.controlpanel import INITFSettings


class IGallery(form.Schema):
    """A Gallery item based on the News Industry Text Format specification.
    """

    text = RichText(
        # nitf/body/body.content
        title=_(u'Body text'),
        required=False,
        )

    section = schema.Choice(
        # nitf/head/pubdata/@position.section
        title=_(u'Section'),
        description=_(u'help_section',
                      default=u'Named section where the article will '
                               'appear.'),
        vocabulary=u'collective.nitf.AvailableSections',
        )

    form.fieldset(
        'categorization',
        label=_(u'Categorization'),
        fields=['section', 'subjects',
                'language'],
        )


class Gallery(Container):
    grok.implements(IGallery)


@form.default_value(field=IGallery['section'])
def section_default_value(data):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(INITFSettings)
    return settings.default_section

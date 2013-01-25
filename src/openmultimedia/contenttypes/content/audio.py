# -*- coding: utf-8 -*-

from zope import schema

from plone.dexterity.content import Item
from plone.directives import form
from plone.namedfile.field import NamedImage

from openmultimedia.contenttypes import _


class IAudio(form.Schema):
    """ A video.
    """

    remote_url = schema.TextLine(
        title=_(u"URL"),
        required=True,
        default=u'',
        readonly=True,
        )

    slug = schema.TextLine(
        title=_(u"Slug"),
        required=False,
        readonly=True,
        )

    image = NamedImage(
        title=_(u"Image"),
        required=False,
        )

    audio_url = schema.TextLine(
        title=_(u"Audio URL"),
        required=False,
        readonly=True,
        )


class Audio(Item):
    pass

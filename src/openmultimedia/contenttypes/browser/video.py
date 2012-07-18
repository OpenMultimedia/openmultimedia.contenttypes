# -*- coding: utf-8 -*-

from five import grok

from openmultimedia.contenttypes.content.video import IVideo

grok.templatedir('templates')


class View(grok.View):
    """ Default view displays a video player.
    """
    grok.context(IVideo)
    grok.require('zope2.View')

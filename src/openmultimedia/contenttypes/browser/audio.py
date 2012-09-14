# -*- coding: utf-8 -*-

from five import grok

from openmultimedia.contenttypes.content.audio import IAudio

grok.templatedir('audio_templates')


class View(grok.View):
    """ Default view displays a audio player.
    """
    grok.context(IAudio)
    grok.require('zope2.View')
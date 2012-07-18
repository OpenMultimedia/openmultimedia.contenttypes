# -*- coding: utf-8 -*-

import urllib2

from zope.component import getUtility

from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from five import grok

from plone.namedfile.field import NamedImage

from openmultimedia.api.interfaces import IVideoAPI
from openmultimedia.contenttypes.content.video import IVideo


@grok.subscribe(IVideo, IObjectAddedEvent)
@grok.subscribe(IVideo, IObjectModifiedEvent)
def update_metadata(obj, event):
    """ Read metadata associated with the video from the OpenMultimedia API.
    """
    video_api = getUtility(IVideoAPI)
    json = video_api.get_json(obj.remote_url)

    if json:
        title = json.get('titulo', None)
        description = json.get('descripcion', None)
        slug = json.get('slug', None)
        thumbnail = json.get('thumbnail_grande', None)
        video_url = json.get('archivo_url', None)
        audio_url = json.get('audio_url', None)

        if title:
            obj.title = title

        if description:
            obj.description = description

        if slug:
            obj.slug = slug

        if thumbnail:
            data = urllib2.urlopen(thumbnail)
            obj.image = NamedImage(data.read())

        if video_url:
            obj.video_url = video_url

        if audio_url:
            obj.audio_url = audio_url

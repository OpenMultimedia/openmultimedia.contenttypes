# -*- coding: utf-8 -*-

import urllib2
import logging
from DateTime import DateTime

from zope.component import getUtility

from zope.lifecycleevent.interfaces import IObjectAddedEvent

from five import grok

from plone.namedfile import NamedImage

from plone.app.blob.interfaces import IATBlob

from openmultimedia.api.interfaces import IVideoAPI
from openmultimedia.contenttypes.content.video import IVideo
from openmultimedia.contenttypes.content.audio import IAudio

logger = logging.getLogger('openmultimedia.contenttypes')


@grok.subscribe(IVideo, IObjectAddedEvent)
def update_metadata(obj, event):
    """ Read metadata associated with the video from the OpenMultimedia API.
    """
    if obj.remote_url:
        video_api = getUtility(IVideoAPI)
        json = video_api.get_json(obj.remote_url)

        if json:
            title = json.get('titulo', None)
            description = json.get('descripcion', None)
            slug = json.get('slug', None)
            thumbnail = json.get('thumbnail_grande', None)
            video_url = json.get('archivo_url', None)
            audio_url = json.get('audio_url', None)
            date = json.get('fecha', None)

            if title:
                obj.title = title

            if description:
                obj.description = description

            if slug:
                obj.slug = slug

            if date:
                date_obj = DateTime(date)
                obj.effective_date = date_obj
                obj.creation_date = date_obj

            if thumbnail:
                try:
                    data = urllib2.urlopen(thumbnail, timeout=3).read()
                except urllib2.HTTPError:
                    logger.info("An error ocurred when trying to access %s" % thumbnail)
                    data = ""
                except urllib2.URLError:
                    logger.info("Timeout when trying to access %s" % thumbnail)
                    data = ""

                obj.image = NamedImage(data, filename=thumbnail)

            if video_url:
                obj.video_url = video_url

            if audio_url:
                obj.audio_url = audio_url


@grok.subscribe(IAudio, IObjectAddedEvent)
def update_metadata_audio(obj, event):
    """ Read metadata associated with the audio from the OpenMultimedia API.
    """
    if obj.remote_url:
        video_api = getUtility(IVideoAPI)
        json = video_api.get_json(obj.remote_url)

        if json:
            title = json.get('titulo', None)
            description = json.get('descripcion', None)
            slug = json.get('slug', None)
            thumbnail = json.get('thumbnail_grande', None)
            audio_url = json.get('archivo_url', None)
            date = json.get('fecha', None)

            if title:
                obj.title = title

            if description:
                obj.description = description

            if slug:
                obj.slug = slug

            if date:
                date_obj = DateTime(date)
                obj.effective_date = date_obj
                obj.creation_date = date_obj

            if thumbnail:
                try:
                    data = urllib2.urlopen(thumbnail, timeout=3).read()
                except urllib2.HTTPError:
                    logger.info("An error ocurred when trying to access %s" % thumbnail)
                    data = ""
                except urllib2.URLError:
                    logger.info("Timeout when trying to access %s" % thumbnail)
                    data = ""

                obj.image = NamedImage(data, filename=thumbnail)
            if audio_url:
                obj.audio_url = audio_url

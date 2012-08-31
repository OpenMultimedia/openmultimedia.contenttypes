# -*- coding: utf-8 -*-

import urllib2
import logging
from DateTime import DateTime

from zope.component import getUtility

from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from five import grok

from plone.namedfile import NamedImage

from plone.app.imaging.interfaces import IImageScaleHandler

from plone.app.blob.interfaces import IATBlob
from Products.ATContentTypes.interface import IATImage
from zope.component import getMultiAdapter

from openmultimedia.api.interfaces import IVideoAPI
from openmultimedia.contenttypes.content.video import IVideo

logger = logging.getLogger('openmultimedia.contenttypes')


@grok.subscribe(IVideo, IObjectAddedEvent)
#@grok.subscribe(IVideo, IObjectModifiedEvent)
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


# @grok.subscribe(IATImage, IObjectAddedEvent)
@grok.subscribe(IATImage, IObjectModifiedEvent)
def images_size_generation(obj, event):    

    field = obj.Schema()['image']
    image = getMultiAdapter((obj, obj.REQUEST), name='images')
    scale_img = image.scale
    available = field.getAvailableSizes(obj)

    directions = ['down',]

    for scale in available:
        scale_img('image', scale=scale)
        for direction in directions:
            scale_img('image', scale=scale, direction=direction)

    special_cases = [
        #vtv/web/theme/tiles/templates/carousel.pt
        {'width':640, 'direction':'down'},
        #vtv/web/theme/templates/nitf_view.pt
        {'width':620, 'direction':'down'},
    ]

    for params in special_cases:
        scale_img('image', **params)

    handler = IImageScaleHandler(field, None)

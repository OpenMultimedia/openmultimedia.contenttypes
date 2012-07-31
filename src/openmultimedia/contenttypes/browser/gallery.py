from datetime import datetime

from zope.component import getUtility

from five import grok

from openmultimedia.contenttypes.content.gallery import IGallery

from collective.nitf.browser import View as NITFView
from collective.prettydate.interfaces import IPrettyDate

grok.templatedir('gallery_templates')

class View(NITFView):
    """ Default view looks like a News Item.
    """
    grok.context(IGallery)
    grok.name('view')
    grok.require('zope2.View')
    grok.template('gallery')
    
    def get_media(self):
        """ Return a list of object brains inside the NITF object.
        """
        media_types = ['Image']

        return self._get_brains(media_types)

    def get_prettydate(self, obj):
        date_utility = getUtility(IPrettyDate)

        date = None
        if datetime > date:
            date = obj.created()
        else:
            date = obj.effective()

        return date_utility.date(date)

    def media_type(self, obj):
        media = ''
        if IATImage.providedBy(obj):
            media = 'image'

        return media

    @property
    def force_column(self):
        return True
    

class Media(NITFView):
    grok.context(IGallery)
    grok.template('media')
    grok.require('cmf.ModifyPortalContent')

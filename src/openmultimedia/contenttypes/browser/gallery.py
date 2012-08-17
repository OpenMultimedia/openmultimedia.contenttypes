from datetime import datetime

from zope.component import getUtility

from five import grok

from plone.directives import dexterity

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
    
    def get_description(self, obj):
        if obj.Description():
            return obj.Description()
        else:
            return self.context.Description()

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


# TODO: enable_form_tabbing must be user selectable
class AddForm(dexterity.AddForm):
    """ Default view looks like a News Item.
    """
    grok.name('openmultimedia.contenttypes.gallery')
    grok.context(IGallery)
    schema = IGallery
    enable_form_tabbing = False

    def updateWidgets(self):
        super(AddForm, self).updateWidgets()
        # XXX why we need to do this?
        self.widgets['IDublinCore.description'].rows = 3
        self.widgets['IDublinCore.description'].style = u'width: 100%;'


class EditForm(dexterity.EditForm):
    """ Default view looks like a News Item.
    """
    grok.context(IGallery)
    schema = IGallery
    enable_form_tabbing = False

    def updateWidgets(self):
        super(EditForm, self).updateWidgets()
        # XXX why we need to do this?
        self.widgets['IDublinCore.description'].rows = 3
        self.widgets['IDublinCore.description'].style = u'width: 100%;'

class Media(NITFView):
    grok.context(IGallery)
    grok.template('media')
    grok.require('cmf.ModifyPortalContent')

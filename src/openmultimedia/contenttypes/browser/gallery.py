from five import grok

from openmultimedia.contenttypes.content.gallery import IGallery

from collective.nitf.browser import View as NITFView

grok.templatedir('gallery_templates')

class View(NITFView):
    """ Default view looks like a News Item.
    """
    grok.context(IGallery)
    grok.name('view')
    grok.require('zope2.View')
    grok.template('gallery')

class Media(NITFView):
    grok.context(IGallery)
    grok.template('media')
    grok.require('cmf.ModifyPortalContent')

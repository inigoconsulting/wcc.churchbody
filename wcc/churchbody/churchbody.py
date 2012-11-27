from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid, Interface

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow

from wcc.churchbody import MessageFactory as _


# Interface class; used to define content-type schema.

class IOtherChurchSchema(Interface):
    name = schema.TextLine(title=_(u'Church Name'))
    country = schema.Choice(
        title=_(u'Country'),
        vocabulary='wcc.vocabulary.country'
    )

class IChurchBody(form.Schema, IImageScaleTraversable):
    """
    A Church Body
    """

    member_of = RelationChoice(
            title=_(u"Member Of"),
            source=ObjPathSourceBinder(object_provides='wcc.churchbody.churchbody.IChurchBody'),
            required=False
    )

    assoc_member_of = RelationChoice(
            title=_(u"Associate Member Of"),
            source=ObjPathSourceBinder(object_provides='wcc.churchbody.churchbody.IChurchBody'),
            required=False
    )

    form.widget(other_members=DataGridFieldFactory)
    other_members = schema.List(
        title=_(u'Other Members'),
        value_type=DictRow(title=_(u'Member'), schema=IOtherChurchSchema),
        required=False
    )

    form.widget(other_members=DataGridFieldFactory)
    other_assoc_members = schema.List(
        title=_(u'Other Associate Members'),
        value_type=DictRow(title=_(u'Member'), schema=IOtherChurchSchema),
        required=False
    )

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class ChurchBody(dexterity.Item):
    grok.implements(IChurchBody)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# churchbody_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    grok.context(IChurchBody)
    grok.require('zope2.View')

    # grok.name('view')

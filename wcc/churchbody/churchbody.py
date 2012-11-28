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
from wcc.churchbody.backref import back_references

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

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

    form.widget(other_assoc_members=DataGridFieldFactory)
    other_assoc_members = schema.List(
        title=_(u'Other Associate Members'),
        value_type=DictRow(title=_(u'Member'), schema=IOtherChurchSchema),
        required=False
    )

# View class
# The view will automatically use a similarly named template in
# churchbody_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.


class IChurchBodyDataProvider(Interface):
    pass

class ChurchBodyDataProvider(grok.Adapter):
    grok.context(IChurchBody)
    grok.implements(IChurchBodyDataProvider)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return self.context.title

    @property
    def text(self):
        return self.context.text

    @property
    def member_of(self):
        if self.context.member_of:
            return self.context.member_of.to_object
        return None

    @property
    def assoc_member_of(self):
        if self.context.assoc_member_of:
            return self.context.assoc_member_of.to_object
        return None

    @property
    def members(self):
        return back_references(self.context, 'member_of')

    @property
    def assoc_members(self):
        return back_references(self.context, 'assoc_member_of')

    @property
    def other_members(self):
        return self.context.other_members

    @property
    def other_assoc_members(self):
        return self.context.other_assoc_members

class Index(dexterity.DisplayForm):
    grok.context(IChurchBody)
    grok.require('zope2.View')
    grok.name('view')
    grok.template('churchbody_view')

    def provider(self):
        return IChurchBodyDataProvider(self.context)

    def sort_by_countries(self, members):
        countries = {}
        vocabulary = getUtility(IVocabularyFactory,
                name='wcc.vocabulary.country')(self.context)
        for member in members:
            country = vocabulary.getTerm(member['country']).title
            countries.setdefault(country, [])
            countries[country].append(member['name'])
        for val in countries.values():
            val.sort()
        return countries

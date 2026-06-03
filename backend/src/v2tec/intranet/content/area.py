from plone.dexterity.content import Container
from plone.schema.email import Email
from plone.supermodel import model
from v2tec.intranet import _
from v2tec.intranet.utils import validadores
from zope import schema
from zope.interface import implementer


class IArea(model.Schema):
    """Definição de uma Área."""


@implementer(IArea)
class Area(Container):
    """Uma Área no V2Tec."""

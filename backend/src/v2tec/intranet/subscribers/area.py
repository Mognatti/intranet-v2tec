from plone import api
from v2tec.intranet import logger
from v2tec.intranet.content.area import Area
from zope.lifecycleevent import ObjectAddedEvent


def _update_excluded_from_nav(obj: Area):
    """Update excluded_from_nav in the Area object."""
    description = obj.description
    obj.exclude_from_nav = not bool(description)
    logger.info(f"Atualizado o campo excluded_from_nav para {obj.title}")


def create_editors_group(obj: Area):
    """Criar Grupo de Editores ao criar uma área"""
    uid = api.content.get_uuid(obj)
    group_id = f"area-{uid}-editors"
    if not api.group.get(group_id):
        api.group.create(groupname=group_id, title=f"Editores da {obj.title}")
        api.group.grant_roles(groupname=group_id, obj=obj, roles=["Editor"])
        logger.info(f"Grupo '{group_id}' criado para a área '{obj.title}'")
    else:
        logger.info(f"Grupo '{group_id}' já existe para a área '{obj.title}'")


def added(obj: Area, event: ObjectAddedEvent):
    """Post creation handler for Area."""
    _update_excluded_from_nav(obj)
    create_editors_group(obj)

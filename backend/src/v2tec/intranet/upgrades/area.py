import uuid

from plone import api
from Products.GenericSetup.tool import SetupTool
from v2tec.intranet import logger
from v2tec.intranet.content.area import Area


def adiciona_blocos_area(portal_setup: SetupTool):
    """Adiciona blocos de pessoas e sub-áreas em cada Área."""
    brains = api.content.find(portal_type="Area")
    for brain in brains:
        area: Area = brain.getObject()
        area_uid = api.content.get_uuid(area)
        area_path = "/".join(area.getPhysicalPath())

        uid_pessoas = str(uuid.uuid4())
        uid_subareas = str(uuid.uuid4())

        bloco_pessoas = {
            "@type": "listing",
            "query": [
                {
                    "i": "portal_type",
                    "o": "plone.app.querystring.operation.selection.any",
                    "v": ["Pessoa"],
                },
                {
                    "i": "area",
                    "o": "plone.app.querystring.operation.selection.any",
                    "v": [area_uid],
                },
            ],
            "sort_on": "sortable_title",
            "sort_order": "",
            "b_size": 25,
            "limit": 0,
        }

        bloco_subareas = {
            "@type": "listing",
            "query": [
                {
                    "i": "portal_type",
                    "o": "plone.app.querystring.operation.selection.any",
                    "v": ["Area"],
                },
                {
                    "i": "path",
                    "o": "plone.app.querystring.operation.string.path",
                    "v": {"query": area_path, "depth": 1},
                },
            ],
            "sort_on": "sortable_title",
            "sort_order": "",
            "b_size": 25,
            "limit": 0,
        }

        existing_blocks = getattr(area, "blocks", {}) or {}
        existing_items = (getattr(area, "blocks_layout", {}) or {}).get("items", [])

        area.blocks = {
            **existing_blocks,
            uid_pessoas: bloco_pessoas,
            uid_subareas: bloco_subareas,
        }
        area.blocks_layout = {
            "items": existing_items + [uid_pessoas, uid_subareas]
        }
        area.reindexObject()
        logger.info(f"Blocos adicionados à área {area.absolute_url()}")

import logging
import uuid

import requests


logging.basicConfig()
logger = logging.getLogger("v2tec.intranet.blocos_area")
logger.setLevel(logging.INFO)

BASE_URL = "http://localhost:8080/Plone/++api++"
USUARIO = "admin"
SENHA = "admin"

session = requests.Session()
session.headers.update({"Accept": "application/json"})

# Autenticação via JWT
response = session.post(f"{BASE_URL}/@login", json={"login": USUARIO, "password": SENHA})
if response.status_code != 200:
    raise ValueError("Usuário ou senha incorretos")
token = response.json()["token"]
session.headers.update({"Authorization": f"Bearer {token}"})


def busca_areas() -> list[dict]:
    """Retorna todas as Áreas do portal, lidando com paginação."""
    areas = []
    url = f"{BASE_URL}/@search?portal_type=Area&sort_on=path&b_size=500&metadata_fields=UID"
    while url:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()
        areas.extend(data["items"])
        url = data.get("batching", {}).get("next")
    return areas


def monta_blocos(area_uid: str, area_path: str) -> tuple[dict, dict]:
    """Retorna (blocks, blocks_layout) para uma Área."""
    uid_titulo = str(uuid.uuid4())
    uid_descricao = str(uuid.uuid4())
    uid_pessoas = str(uuid.uuid4())
    uid_subareas = str(uuid.uuid4())

    blocks = {
        uid_titulo: {"@type": "title"},
        uid_descricao: {"@type": "description"},
        uid_pessoas: {
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
        },
        uid_subareas: {
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
        },
    }

    blocks_layout = {
        "items": [uid_titulo, uid_descricao, uid_pessoas, uid_subareas]
    }

    return blocks, blocks_layout


areas = busca_areas()
logger.info(f"Encontradas {len(areas)} áreas")

for area in areas:
    area_uid = area["UID"]
    area_url = area["@id"]
    # Extrai o caminho físico a partir da URL da API
    # Ex: http://localhost:8080/Plone/++api++/estrututura/sti -> /Plone/estrututura/sti
    area_path = area_url.replace("http://localhost:8080/Plone/++api++", "/Plone")

    blocks, blocks_layout = monta_blocos(area_uid, area_path)

    response = session.patch(
        area_url,
        json={"blocks": blocks, "blocks_layout": blocks_layout},
    )

    if response.status_code > 299:
        logger.error(f"Erro ao atualizar '{area_url}': {response.status_code} - {response.text}")
    else:
        logger.info(f"Blocos configurados em '{area_url}'")

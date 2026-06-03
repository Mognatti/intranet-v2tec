from AccessControl import Unauthorized
from plone import api
from plone.dexterity.fti import DexterityFTI
from v2tec.intranet.content.pessoa import Pessoa
from zope.component import createObject

import pytest


CONTENT_TYPE = "Pessoa"


@pytest.fixture
def pessoa_payload() -> dict:
    """Return a payload to create a new pessoa."""
    return {
        "type": "Pessoa",
        "id": "joao-silva",
        "title": "João Silva",
        "description": "Desenvolvedor backend na V2Tec.",
        "email": "joao.silva@v2solucoes.com.br",
    }


class TestPessoa:
    @pytest.fixture(autouse=True)
    def _setup(self, get_fti, portal):
        self.fti = get_fti(CONTENT_TYPE)
        self.portal = portal

    def test_fti(self):
        assert isinstance(self.fti, DexterityFTI)

    def test_factory(self):
        factory = self.fti.factory
        obj = createObject(factory)
        assert obj is not None
        assert isinstance(obj, Pessoa)

    @pytest.mark.parametrize(
        "behavior",
        [
            "plone.basic",
            "plone.namefromtitle",
            "plone.shortname",
            "plone.excludefromnavigation",
            "plone.leadimage",
            "plone.versioning",
            "plone.constraintypes",
            "v2tec.intranet.behavior.contato",
            "v2tec.intranet.behavior.endereco",
        ],
    )
    def test_has_behavior(self, get_behaviors, behavior):
        assert behavior in get_behaviors(CONTENT_TYPE)

    @pytest.mark.parametrize(
        "behavior",
        [
            "volto.blocks",
            "volto.preview_image",
        ],
    )
    def test_has_not_behavior(self, get_behaviors, behavior):
        assert behavior not in get_behaviors(CONTENT_TYPE)

    @pytest.mark.parametrize(
        "role,allowed",
        [
            ["Manager", True],
            ["Site Administrator", True],
            ["Editor", False],
            ["Reviewer", False],
            ["Contributor", False],
            ["Reader", False],
        ],
    )
    def test_create(self, pessoa_payload, role: str, allowed: bool):
        with api.env.adopt_roles([role]):
            if allowed:
                content = api.content.create(container=self.portal, **pessoa_payload)
                assert content.portal_type == CONTENT_TYPE
                assert isinstance(content, Pessoa)
            else:
                with pytest.raises(Unauthorized):
                    api.content.create(container=self.portal, **pessoa_payload)

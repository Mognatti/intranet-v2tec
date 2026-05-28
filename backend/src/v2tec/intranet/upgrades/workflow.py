from plone import api
from Products.CMFPlone.WorkflowTool import WorkflowTool
from Products.GenericSetup.tool import SetupTool
from v2tec.intranet import logger


def atualiza_permissoes(portal_setup: SetupTool):
    """Upgrade all permissions follwing the new workflow."""
    message = "Permissões de workflow atualizadas seguindo o novo workflow."
    portal = api.portal.get()
    wf_tool: WorkflowTool = api.portal.get_tool("portal_workflow")
    wf_tool.notifyCreated(portal)
    wf_tool.updateRoleMappings()
    logger.info(message)

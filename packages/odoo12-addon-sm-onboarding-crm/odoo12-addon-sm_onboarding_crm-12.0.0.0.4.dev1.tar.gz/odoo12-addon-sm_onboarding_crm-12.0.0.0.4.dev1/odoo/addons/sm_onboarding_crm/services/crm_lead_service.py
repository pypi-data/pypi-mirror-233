from odoo.addons.component.core import Component
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils

from . import schemas

ONBOARDING_SALES_TEAM_XML_ID = "crm_team_sales_onboarding"
CRM_TYPE_OPPORTUNITY = "opportunity"
UTM_SOURCE_BALENYA_XML_ID = "utm_source_onboarding_company_balenya_main_web_page"
ADDON_NAME = 'sm_onboarding_crm'


class CrmLeadOnboardingService(Component):
    _inherit = "crm.lead.service"
    _name = "crm.lead.service"
    _description = "Crm lead requests"

    def _source_is_onboarding(self, source_id):
        """
        Check if the source is from the onboarding process
        :return Bool :
        """
        utm_source = self.env['utm.source']
        if utm_source.search([int(source_id)]):
            return True
        return False

    def _validator_create(self):
        validator_schema = super()._validator_create().copy()
        validator_schema.update(schemas.SM_CRM_LEAD_CREATE)
        return validator_schema

    def _prepare_create(self, params):
        """
        Prepare data for crm lead creation
        :param dic params:
        :return:
        """
        create_dict = super()._prepare_create(params)
        # Todo create test in this case not source_xml_id in json
        if create_dict.get("source_xml_id", None) is None:
            res = super().create(**params)
            return res
        target_source_xml_id = params.get("source_xml_id")
        # TODO Create test return from a different source to UTM_SOURCE_BALENYA_XML_ID
        if target_source_xml_id == UTM_SOURCE_BALENYA_XML_ID:
            utm_source_record = sm_utils.get_record_by_xml_id(
             self, ADDON_NAME, UTM_SOURCE_BALENYA_XML_ID)
            sales_team_record = sm_utils.get_record_by_xml_id(
             self, ADDON_NAME, ONBOARDING_SALES_TEAM_XML_ID)
            create_dict.update({
                "source_id": utm_source_record.id,
                "type": CRM_TYPE_OPPORTUNITY,
                "team_id": sales_team_record.id
            })

        return create_dict

    def create(self, **params):
        source_xml_id = params.get("source_xml_id")

        if source_xml_id is None:
            return super().create(**params)

        crm_lead_response = super(CrmLeadOnboardingService, self).create(**params)

        if source_xml_id == UTM_SOURCE_BALENYA_XML_ID:
            sales_team_record = sm_utils.get_record_by_xml_id(
                self, ADDON_NAME, ONBOARDING_SALES_TEAM_XML_ID)

            crm_lead_data = json.loads(crm_lead_response.response[0].decode("utf-8"))
            crm_lead_id = crm_lead_data.get("id", False)

            if not crm_lead_id:
                raise ValidationError(_("Crm lead id not found in response"))

            crm_lead_record = self.env["crm.lead"].search([('id', '=', crm_lead_id)])
            crm_lead_record.write({"team_id": sales_team_record.id})

        return crm_lead_response

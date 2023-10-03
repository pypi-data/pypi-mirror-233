import json
import logging
from . import schemas
from odoo.http import Response
from odoo.tools.translate import _
from odoo.addons.component.core import Component
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CsInvoiceService(Component):
    _inherit = "base.rest.private_abstract_service"
    _name = "cs.invoice.service"
    _usage = "cs-invoice"
    _description = """
        Invoice Services
    """

    def create(self, **params):
        _logger.info(str(self.work.request.httprequest.headers))
        create_dict = self._prepare_create(params)
        invoice = self.env['account.invoice'].create(create_dict)
        invoice.message_post(
            subject="Cs prepayment invoice created from APP",
            body=str(params),
            message_type="notification"
        )
        return Response(
            json.dumps({
                'message': _("Creation ok"),
                'id': invoice.id
            }),
            status=200,
            content_type="application/json"
        )

    def _validator_create(self):
        return schemas.S_CS_INVOICE_CREATE

    def _prepare_create(self, params):
        company = self.env.user.company_id
        # TODO: Conditional setup payment mode based on params when it's clear.
        create_dict = {
            'state': 'draft',
            'type': 'out_invoice',
            'journal_id': company.cs_app_oneshot_account_journal_id.id,
            # in the future we will define this based on the params.
            'invoice_email_sent': False,
            # in the future we will define this based on the params.
            'invoice_template': 'cs_app_invoice',
            'payment_mode_id': company.cs_app_oneshot_payment_mode_id.id
            # in the future we will define this based on the params.
        }
        customer = params.get('customer', False)
        cs_person_index = self._filter_reference(customer.get('reference', ''))
        related_partners = self.env['res.partner'].search(
            [('cs_person_index', '=', cs_person_index)])
        if len(related_partners) == 1:
            create_dict['partner_id'] = related_partners[0].id
        else:
            # TODO add track error whit sm_maintenance.models_sm_utils.create_system_task
            raise ValidationError(
                f"Cannot be billed if not defined user app invoice:{params.get('reference', '')}")

        items = params.get('items', False)
        if items:
            lines_list = []
            taxes_l = []
            for tax in company.cs_app_oneshot_product_id.taxes_id:
                # 4: link tax to invoice line
                taxes_l.append((4, tax.id))
            for item in items:
                # 0, 0: create invoice line with dictionary
                lines_list.append((0, 0, {
                    'product_id': company.cs_app_oneshot_product_id.id,
                    'name': item['description'],
                    'price_unit': item['price']/(1.0+(company.cs_app_oneshot_product_id.taxes_id[0].amount/100)),
                    'quantity': item['quantity'],
                    'account_id': company.cs_app_oneshot_product_id.property_account_income_id.id,
                    'account_analytic_id': company.cs_app_oneshot_product_id.income_analytic_account_id.id,
                    'line_type': 'default',
                    'invoice_line_tax_ids': taxes_l,
                }))
            create_dict['invoice_line_ids'] = lines_list
        create_dict['date_invoice'] = params.get('date')
        return create_dict

    @staticmethod
    def _filter_reference(reference):
        return reference.replace("T/", '').split('/', maxsplit=1)[0]

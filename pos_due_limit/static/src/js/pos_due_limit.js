/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";
import { _t } from "@web/core/l10n/translation";
import {ErrorPopup} from "@point_of_sale/app/errors/popups/error_popup";

patch(PaymentScreen.prototype, {
    async validateOrder(isForceValidate) {
        if (this.pos.config.is_spanish) {
            const order = this.currentOrder;
            order.is_l10n_es_simplified_invoice = order.canBeSimplifiedInvoiced() && !order.to_invoice;
            if (!order.is_l10n_es_simplified_invoice && !order.to_invoice) {
                this.popup.add(ErrorPopup, {
                    title: _t("Error"),
                    body: _t("Order amount is too large for a simplified invoice, use an invoice instead."),
                });
                return false;
            }
            if (order.is_l10n_es_simplified_invoice) {
                order.to_invoice = Boolean(this.pos.config.l10n_es_simplified_invoice_journal_id)
                if (await this._askForCustomerIfRequired() === false) {
                    return false;
                }
                order.partner = order.partner || this.pos.db.partner_by_id[this.pos.config.simplified_partner_id[0]];
            }
        }
            if (this.currentOrder.paymentlines[0].name == 'Customer Account'){
                if(this.currentOrder.paymentlines[0].amount > this.pos.get_order().partner.due_limit){
                    this.popup.add(ErrorPopup, {
                    title: _t("Warning"),
                    body: _t("The customer has exceeded the allowed due limit"),
                });
                return false;
                }
            }
        return await super.validateOrder(...arguments);
    },
});

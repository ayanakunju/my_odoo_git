/** @odoo-module */
import {InputBox} from "./input_box";
import { patch } from "@web/core/utils/patch";
import { useEffect, useRef, useState,  } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

patch(InputBox.prototype, {
    setup(){
        super.setup()
        this.orm = useService("orm");
        this.action = useService("action")
        this.state = useState({
        value:0
        })
        this.demoFunctionPatch

        useEffect(
            (rec) => {
            console.log("rec",rec)
            },
            () => [this.state.value]

            )
        this.inputref = useRef("inputbox12");
},
       demoFunctionPatch(e){
        this.state.value += e

       },
        demofu(){
        console.log(this.inputref.el.value)
        },

        async ormfunction() {
        this.sale_order = await this.orm.call("owl.model", "owl_model_search", []);
        console.log(this.sale_order)
        this.sale =  await this.orm.search("sale.order",[]);
        console.log(this.sale)
        this.sale_orders = await this.orm.searchRead("sale.order",[],['name'],{limit:5});
        console.log(this.sale_orders)
    },

        openform() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: 'sale.order',
            views: [[false, "form"]],
            res_id: 5,
        });
    }
})

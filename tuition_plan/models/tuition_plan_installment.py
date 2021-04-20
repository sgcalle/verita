# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api


class TuitionPlanInstallment(models.Model):
    _name = "tuition.plan.installment"
    _description = "Tuition Plan Installment"
    _order = "date"
    _rec_name = "date"

    date = fields.Date(string="Date",
        help="Date to trigger installment")
    plan_id = fields.Many2one(string="Tuition Plan",
        comodel_name="tuition.plan",
        required=True,
        ondelete="cascade")
    product_ids = fields.Many2many(string="Products",
        comodel_name="tuition.plan.product",
        relation="plan_product_plan_installment_rel",
        help="Products to include in order and/or invoice")
    
    def execute(self):
        make_sale_obj = self.env["res.partner.make.sale"]
        for installment in self.filtered(lambda i: i.plan_id.active and i.product_ids):
            plan = installment.plan_id
            students = plan.partner_ids | plan.default_partner_ids
            students = students.filtered(lambda s: s.grade_level_id in plan.grade_level_ids and s.student_status == "Enrolled")
            invoice_due_date = False
            if not plan.payment_term_id and plan.first_due_date:
                invoice_date_due_day = plan.first_due_date.day
                months = 0 if invoice_date_due_day >= installment.date.day else 1
                invoice_due_date = installment.date + relativedelta(months=months, day=invoice_date_due_day)
            order_line_ids = [(6, 0, [])]
            for product in installment.product_ids:
                order_line_ids.append((0, 0, {
                    "product_id": product.product_id.id,
                    "price_unit": product.amount,
                    "display_type": False,
                }))
            vals = {
                "company_id": plan.company_id.id,
                "invoice_date": installment.date,
                "invoice_date_due": invoice_due_date,
                "separate_by_financial_responsability": True,
                "analytic_account_id": plan.analytic_account_id.id,
                "journal_id": False,
                "order_line_ids": order_line_ids,
                "payment_term_id": plan.payment_term_id.id,
                "use_student_payment_term": plan.use_student_payment_term,
            }
            make_sale = make_sale_obj.with_context(active_ids=students.ids).create(vals)
            for sale in make_sale.sales_ids:
                if plan.discount_ids:
                    children = sale.family_id.member_ids\
                        .filtered(lambda m: m.person_type == "student" and m.student_status == "Enrolled")\
                        .sorted(lambda m: m.name)\
                        .sorted(lambda m: (m.grade_level_id.sequence or 0, m.grade_level_id.id or 0,
                            m.date_of_birth or fields.Date.context_today(self)), reverse=True).ids
                    if sale.student_id.id in children:
                        index = children.index(sale.student_id.id)
                    categories = set()
                    for discount in plan.discount_ids:
                        categories.add(discount.category_id)
                    for category in categories:
                        discounts = plan.discount_ids.filtered(lambda d: d.category_id == category)
                        category_index = len(discounts) - 1 if index >= len(discounts) else index
                        if category == False:
                            amount = sale.amount_total
                        else:
                            amount = sum(sale.order_line.filtered(lambda l: l.product_id.categ_id == category).mapped("price_total"))
                        if amount > 0:
                            sale.write({
                                "order_line": [(0, 0, {
                                    "product_id": plan.discount_product_id.id,
                                    "price_unit": min(-amount * discounts[index].percentage / 100, sale.amount_total),
                                })]
                            })
            if plan.automation in ["sales_order", "draft_invoice", "posted_invoice"]:
                for sale in make_sale.sales_ids:
                    sale.action_confirm()
                    if plan.automation in ["draft_invoice", "posted_invoice"]:
                        invoices = sale._create_invoices(grouped=True)
                        invoice_lines = invoices.invoice_line_ids
                        for product in installment.product_ids:
                            for line in invoice_lines:
                                if line.price_unit >= 0 and product.product_id == line.product_id and product.analytic_account_id:
                                    line.analytic_account_id = product.analytic_account_id.id
                        if plan.automation == "posted_invoice":
                            invoices.action_post()
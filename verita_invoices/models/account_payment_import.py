# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class AccountPaymentImport(models.Model):
    _name = "account.payment.import"
    _description = "Payment Import"
    # other code
    # transaction_id=fields.Char(string="Trabsaction ID", required=True, unique=True)

    transaction_date = fields.Date(string="Transaction Date",
                                   required=True)
    facts_id = fields.Char(string="Student ID",
                           required=True)
    paid_in_lei = fields.Float(string="Amount Paid in RON")
    paid_in_euro = fields.Float(string="Amount Paid in EURO")

    amount = fields.Float(string="Amount", compute='amount_in_base', store=True)

    error_msg = fields.Char(string="Error Msg")

    invoice_number = fields.Char(string="Invoice No")

    invoice_id = fields.Many2one(string="Invoice",
                                 comodel_name="account.move")
    payment_id = fields.Many2one(string="Payment",
                                 comodel_name="account.payment")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company.id)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True, store=True)

    def amount_in_base(self):
        eur = self.env['res.currency'].search([('name', '=', 'EUR')])
        ron = self.env['res.currency'].search([('name', '=', 'RON')])
        for rec in self:
            if rec.paid_in_euro > 0:
                rec.amount = eur.with_context(date=rec.transaction_date).compute(rec.paid_in_euro, ron)
            else:
                rec.amount = rec.paid_in_lei

    def create_payment(self, journal):
        move_obj = self.env["account.move"]
        payment_obj = self.env["account.payment"]

        for line in self.filtered(lambda l: not l.payment_id):
            matched_invoice = move_obj.search([
                ("name","like",line.invoice_number),
                ("type","=","out_invoice"),
                ("state","=","posted"),
                ("amount_residual",">",0.0)
            ])
            if not matched_invoice:
                line.error_msg = "No unpaid posted invoice found"
                continue
            elif len(matched_invoice) > 1:
                # filter by matching paypro id
                matched_invoice = matched_invoice.filtered(lambda i: i.student_id)
                if not matched_invoice:
                    line.error_msg = "No unpaid posted invoice found with matching student PayPro ID"
                    continue
                elif len(matched_invoice) > 1:
                    line.error_msg = "Multiple invoices matched"
                    continue
            line.error_msg = False
            defaults = payment_obj.with_context(active_ids=[matched_invoice.id], active_model="account.move").default_get([])
            defaults.update({
                "amount": line.amount,
                "journal_id": journal.id,
                "payment_date": line.transaction_date,
                "payment_method_id": journal.inbound_payment_method_ids[0].id,
            })
            payment = payment_obj.create(defaults)
            payment.post()
            line.invoice_id = matched_invoice.id
            line.payment_id = payment.id

# Copyright (c) 2024, thesni and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibraryMember(Document):
    #this method will run every time a document is saved
    def before_save(self):
        self.full_name = f'{self.first_name} {self.last_name or ""}'

    @frappe.whitelist()
    def create_membership(self, values):
        # create a new document
        doc = frappe.new_doc('Library Membership')
        doc.library_member = self.name
        doc.from_date = values["from_date"]
        doc.to_date = values["to_date"]
        doc.paid = values["paid"]
        doc.insert()
        return doc.name

    @frappe.whitelist()
    def create_transaction(self,values):
        doc=frappe.new_doc('Library Transaction')
        doc.article=values["article"]
        doc.library_member=self.name
        doc.type=values["type"]
        doc.date_of_transaction=values["date_of_transaction"]
        doc.insert()
        return doc.name

import frappe
from frappe.model.document import Document


class LibraryMembership(Document):
	# check before submitting this document
	def before_submit(self):
		exists = frappe.db.exists(
			"Library Membership",
				{
					"library_member": self.library_member,
					"docstatus": 1,
					# check if the membership's end date is later than this membership's start date
					"to_date": (">", self.from_date),
				},
			)
		if exists:
			frappe.throw("There is an active membership for this member")

	def validate(self):
		if self.from_date and self.to_date:
			if self.from_date > self.to_date:
				# frappe.throw("invalid date format")
				frappe.throw(
				    msg='Select a valid date',
				    title='Invalid date',)

// Copyright (c) 2024, thesni and contributors
// For license information, please see license.txt

frappe.query_reports["Article script report"] = {
	"filters": [
		{
			"fieldname":"name",
			"label":__("ID"),
			"fieldtype":"Link",
			"options":"Article"
		},
		{
			"fieldname":"author",
			"label":__("author"),
			"fieldtype":"Data"

		},
		{
			"fieldname":"publisher",
			"label":__("publisher"),
			"fieldtype":"Data"

		}

	]
};

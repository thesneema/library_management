frappe.ui.form.on('Article', {
    issue_copy: function(frm) {
        frappe.call({
            method: "your_app.article.article.issue_copy",
            args: {
                docname: frm.doc.name
            },
            callback: function(r) {
                if (r.message) {
                    frm.refresh();
                }
            }
        });
    },
    return_copy: function(frm) {
        frappe.prompt({
            fieldname: 'unique_id',
            label: 'Unique ID',
            fieldtype: 'Data',
            reqd: 1
        },
        function(values){
            frappe.call({
                method: "your_app.article.article.return_copy",
                args: {
                    docname: frm.doc.name,
                    unique_id: values.unique_id
                },
                callback: function(r) {
                    if (r.message) {
                        frm.refresh();
                    }
                }
            });
        },
        __('Return Copy'),
        __('Submit')
        );
    }
});
// Copyright (c) 2024, thesni and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Article", {
// 	refresh(frm) {

// 	},
// });

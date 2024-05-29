frappe.ui.form.on("Library Transaction", {
    refresh(frm) {
        if (frm.doc.type == 'Issued') {
            frm.set_query('article', () => {
                return {
                    filters: {
                        status: 'Available'
                    }
                }
            })
        }

        set_member_query(frm);

    },

    article(frm) {
        /*
         Check if the article has available copies
        */
        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Article",
                name: frm.doc.article
            },
            callback: function(r) {
                if (r.message) {
                    let article = r.message;
                    let available_copies = article.unique_ids.filter(copy => copy.status === 'Available').length;
                    if (available_copies === 0) {
                        frappe.msgprint(__('All copies of this article are currently issued.'));
                    } else {
                        frm.set_value('available_copies', available_copies);
                    }
                }
            }
        });
    },

    validate(frm) {
        if (frm.doc.type == 'Issued') {
            frappe.call({
                method: "library_management.library_management.doctype.library_transaction.library_transaction.issue_article",
                args: {
                    article: frm.doc.article,
                    member: frm.doc.member
                },
                callback: function(r) {
                    if (r.message === 'unavailable') {
                        frappe.msgprint(__('All copies of this article are currently issued.'));
                        frappe.validated = false;
                    }
                }
            });
        }
    }
});

frappe.ui.form.on("Article list", {
	article: function(frm, cdt, cdn) {
		row = locals[cdt][cdn]
		frm.call("find_and_set_article_id", {"article": row.article}).then(r => {
			if (r.message) {
				console.log(r.message);
				row.article_id = r.message
				frm.refresh_fields()
			}
			else {
				row.article_id = ""
				frm.refresh_fields()
			}
		})
	}
});

function set_member_query(frm) {
  frm.set_query("library_member", () => {
    return {
      query: "library_management.library_management.doctype.library_transaction.library_transaction.library_member_query"
    }
  })
}

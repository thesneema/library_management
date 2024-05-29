import frappe

def new_user_document(doc,method=None):
    frappe.msgprint(f"new {doc} in user")



def validate_single_librarian_role(doc, method=None):
    # Check if the user has the "Librarian" role
    if "Librarerian" in [d.role for d in doc.get("roles")]:
        # Query to check if any other user has the "Librarian" role
        librarerian_roles = frappe.db.exists("Has Role", {
            "role": "Librarerian",
            "parenttype": "User",
            "parent": ["!=", doc.name]
        })

        if librarerian_roles:
            frappe.throw("Another user already has the 'Librarian' role. Only one user can have this role at a time.")

    frappe.msgprint(f"New user document created/updated for: {doc.name}")

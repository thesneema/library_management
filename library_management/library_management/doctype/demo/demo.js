// Copyright (c) 2024, thesni and contributors
// For license information, please see license.txt

frappe.ui.form.on("demo", {
	refresh(frm) {
    frm.add_custom_button('demo', ()=> {
      let d = new frappe.ui.Dialog({
          title: 'Enter details',
          fields: [
              {
                  label: 'First Name',
                  fieldname: 'first_name',
                  fieldtype: 'Data'
              },
              {
                  label: 'Last Name',
                  fieldname: 'last_name',
                  fieldtype: 'Data'
              },
              {
                  label: 'Age',
                  fieldname: 'age',
                  fieldtype: 'Int'
              }
          ],
          size: 'small', // small, large, extra-large
          primary_action_label: 'Submit',
          primary_action(values) {
              console.log(values);
              d.hide();
          }
      });

      d.show();
    })
	},
});

frappe.ui.form.on('Library Member', {
    refresh: function(frm) {
        frm.add_custom_button('Create Membership', () => {
            let d = new frappe.ui.Dialog({
                title: 'Enter details',
                fields: [
                    {
                        label: 'From date',
                        fieldname: 'from_date',
                        fieldtype: 'Date'
                    },
                    {
                        label: 'To date',
                        fieldname: 'to_date',
                        fieldtype: 'Date'
                    },
                    {
                        label: 'Paid',
                        fieldname: 'paid',
                        fieldtype: 'Check'
                    }
                ],
                size: 'small', // small, large, extra-large
                primary_action_label: 'Submit',
                primary_action(values) {
                    console.log(values);
                    frm.call('create_membership', {values:values})
                    .then( r => {
                      d.hide();
                      frappe.msgprint(`Membership ${r.message} has been created`)
                    })
                }
            });

            d.show();
        });

        frm.add_custom_button('Create Transaction', () => {
            let d = new frappe.ui.Dialog({
                title: 'Enter details',
                fields: [
                    {
                        label: 'Article',
                        fieldname: 'article',
                        fieldtype: 'Link',
                        options: 'Article'
                    },
                    // {
                    //     label: 'Library Member',
                    //     fieldname: 'library_member',
                    //     fieldtype: 'Link',
                    //     options: 'Library Member'
                    // },
                    {
                        label: 'Type',
                        fieldname: 'type',
                        fieldtype: 'Select',
                        options: 'Issue\nReturn'

                    },
                    {
                        label: 'Date of Transaction',
                        fieldname: 'date_of_transaction',
                        fieldtype: 'Date',
                    },
                    {
                        label: 'Delay',
                        fieldname: 'delay_fine',
                        fieldtype: 'Currency',
                        depends_on:"eval:doc.type=='Return'"

                    },
                    {
                        label: 'Damage',
                        fieldname: 'damage_fine',
                        fieldtype: 'Currency',
                        depends_on:"eval:doc.type=='Return'"

                    }



                ],
                size: 'small', // small, large, extra-large
                primary_action_label: 'Submit',
                primary_action(values) {
                    console.log(values);
                    frm.call('create_transaction', {values:values})
                    .then( r => {
                      d.hide();
                      frappe.msgprint(`Transaction ${r.message} has been done`)
                    })
                }
            });

            d.show();
        });
    }
});

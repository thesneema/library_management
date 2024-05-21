frappe.ui.form.on('Library Membership', {
    from_date: function(frm){
    if (frm.doc.from_date>frm.doc.to_date && frm.doc.to_date){
    frappe.msgprint({
      title: __('Notification'),
      indicator: 'green',
      message: __('Please select valid date')
    });
  }
},
    to_date: function(frm){
    if (frm.doc.from_date>frm.doc.to_date){
    frappe.msgprint({
      title: __('Notification'),
      indicator: 'green',
      message: __('Please select valid date')
    });


  }
}
});

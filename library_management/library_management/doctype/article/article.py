import frappe
from frappe.model.document import Document

class Article(Document):
    def validate(self):
        # Clear existing rows in the child table
        # self.clear_table_rows()

        # Generate rows in the child table based on the count
        if self.count and not self.is_new():
            for i in range(self.count):
                # row = self.append("unique_ids", {})
                # # Generate unique ID for each copy
                # row.unique_id = f"{self.article}-{str(i + 1).zfill(3)}"  # Adjust padding as needed
                # # Set status based on availability
                # if i < self.count:
                #     row.status = "available"
                # else:
                #     row.status = "issued"

                new_article_id = frappe.new_doc("Article ID")
                # Generate unique ID for each copy
                new_article_id.article = self.article
                new_article_id.available = 1
                new_article_id.insert()

    # def clear_table_rows(self):
    #     # Clear existing rows in the child table
    #     self.set("unique_ids", [])

import frappe
from frappe.model.document import Document
from frappe.utils import getdate

class LibraryTransaction(Document):

    def before_submit(self):
        if self.type == "Issue":
            self.validate_issue()
            self.validate_maximum_limit()
            for row in self.get('articles'):
                article = frappe.get_doc("Article", row.article)
                article.status = "issued"
                article.save()
                self.append_issued_article_to_member(article)

        elif self.type == "Return":
            self.validate_return()
            for row in self.get('articles'):
                article = frappe.get_doc("Article", row.article)
                article.status = "available"
                article.save()
                self.remove_issued_article_from_member(article)

    def validate_issue(self):
        self.validate_membership()
        for row in self.get('articles'):
            article = frappe.get_doc("Article", row.article)
            if article.status == "issued":
                frappe.throw(f"Article {article.name} is already issued by another member")


    def validate_return(self):
        library_member = frappe.get_doc("Library Member", self.library_member)
        currently_issued = library_member.get("currently_issued", [])

        for row in self.get('articles'):
            returned_article = row.article

            # Check if the article is in the currently_issued list
            book_found = False
            for book in currently_issued:
                if book.currently_issued_article == returned_article:
                    book_found = True
                    break

            if book_found:
                # Remove the returned book from the currently_issued list
                updated_currently_issued = [
                    book for book in currently_issued
                    if not (book.currently_issued_article == returned_article and not book.get('return_date'))
                ]

                library_member.set("currently_issued", updated_currently_issued)
                library_member.save()
            else:
                frappe.throw(f"Article {returned_article} cannot be returned as it was not issued.")

            # Check that the return date is after the issue date
            issue_transaction = frappe.get_all(
                "Library Transaction",
                filters={
                    "library_member": self.library_member,
                    "article": row.article,
                    "type": "Issue",
                    "docstatus": 1
                },
                fields=["date"],
                order_by="date desc",
                limit=1
            )

            if issue_transaction:
                issue_date = getdate(issue_transaction[0].date)
                return_date = getdate(self.date)
                if return_date <= issue_date:
                    frappe.throw(f"Return date for article {returned_article} must be after the issue date {issue_date}")


    def on_cancel(self):
        library_member = frappe.get_doc("Library Member", self.library_member)
        currently_issued = library_member.get("currently_issued", [])

        if self.type == "Issue":
            for row in self.get('articles'):
                article = frappe.get_doc("Article", row.article)
                article.count += 1
                article.save()

                # Remove the book from the current_books list
                for i, book in enumerate(currently_issued):
                    if book.currently_issued_article == row.article and not book.get('return_date'):
                        currently_issued.pop(i)
                        break

        elif self.type == "Return":
            for row in self.get('articles'):
                article = frappe.get_doc("Article", row.article)
                article.count -= 1
                article.status = "Issued"
                article.save()

                # Restore the book to the currently issued list if needed
                book_found = False
                for book in currently_issued:
                    if book.currently_issued_article == row.article and book.get('return_date') == self.date:
                        book.return_date = None
                        book_found = True
                        break

                if not book_found:
                    library_member.append("currently_issued", {
                        "currently_issued_article": row.article,
                    })

        library_member.currently_issued_count = len(library_member.get("currently_issued"))
        library_member.save()

    def validate_maximum_limit(self):
        max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
        library_member = frappe.get_doc("Library Member", self.library_member)

        # Ensure current_book is initialized as an empty list if it's None
        currently_issued = library_member.get("currently_issued") or []

        currently_issued_count = len([book for book in currently_issued if not book.get('return_date')])
        new_issues_count = len(self.get('articles'))
        total_count = currently_issued_count + new_issues_count
        if total_count > max_articles:
            frappe.throw("The total count of issued articles exceeds the maximum limit")

    def validate_membership(self):
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": 1,
                "from_date": ("<", self.date),
                "to_date": (">", self.date),
            },
        )
        if not valid_membership:
            frappe.throw("The member does not have a valid membership")

    def before_save(self):
        total_damage_fine = 0

        # Calculate the total damage fine
        for row in self.fine:
            if row.fine_type == 'Damage':
                damage_fine = int(row.fine_amount) if row.fine_amount else 0
                total_damage_fine += damage_fine

        # Calculate the total delay fine
        total_delay_fine = self.calculate_return_delay_fine()

        # Calculate the total fine
        self.total_fine = total_damage_fine + total_delay_fine

    def calculate_return_delay_fine(self):
        total_delay_fine = 0
        loan_period = frappe.db.get_single_value('Library Settings', 'loan_period')
        single_day_fine = frappe.db.get_single_value('Library Settings', 'single_day_fine')

        for row in self.get('articles'):
            article = frappe.get_doc("Article", row.article)

            # Find the issue transaction for this article
            issue_transaction = frappe.get_all("Library Transaction",
                                               filters={
                                                   "library_member": self.library_member,
                                                   "article": row.article,
                                                   "type": "Issue",
                                                   "docstatus": 1
                                               },
                                               fields=["date"],
                                               order_by="date desc",
                                               limit=1)

            if issue_transaction:
                issued_date = getdate(issue_transaction[0].date)
                actual_duration = frappe.utils.date_diff(self.date, issued_date)

                if actual_duration > loan_period:
                    additional_days = actual_duration - loan_period
                    delay_fine = single_day_fine * additional_days
                    total_delay_fine += delay_fine

        return total_delay_fine

    @frappe.whitelist()
    def find_and_set_article_id(self, article):
        '''
        Method finds the unique ID for issuing an article
        args:
            article: name of the article being issued
        output:
            unique ID for issuing
        '''
        article_id = frappe.db.get_value("Article ID", {"article": article, "available": 1}, "name")
        return article_id

    def append_issued_article_to_member(self, article):
        library_member = frappe.get_doc("Library Member", self.library_member)
        library_member.append("currently_issued", {
            "currently_issued_article": article.name,
            # "status": self.type,
        })
        library_member.save()

    def remove_issued_article_from_member(self, article):
        library_member = frappe.get_doc("Library Member", self.library_member)
        updated_currently_issued = []

        for row in library_member.get("currently_issued", []):
            if row.currently_issued_article == article.name and not row.get('return_date'):
                continue  # Skip adding this row to the updated list, effectively removing it
            updated_currently_issued.append(row)

        library_member.set("currently_issued", updated_currently_issued)
        library_member.save()

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def library_member_query(doctype, txt, searchfield, start, page_len, filters):

    active_member_list = frappe.db.get_all("Library Membership", {"docstatus":1}, pluck="library_member")

    return [[member] for member in active_member_list]

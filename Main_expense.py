import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from expense_ui import Ui_MainWindow

class ExpenseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.expenses = []

        self.ui.btn_add.clicked.connect(self.add_expense)
        self.ui.btn_clear.clicked.connect(self.clear_expenses)

    def add_expense(self):
        desc = self.ui.txt_description.text()
        category = self.ui.cmb_category.currentText()
        quantity = self.ui.spin_quantity.value()
        amount_text = self.ui.txt_amount.text().replace(",", "").replace(".", "")
        date = self.ui.date_edit.date().toString("dd/MM/yyyy")

        if not desc or not amount_text:
            QMessageBox.warning(self, "Input tidak valid", "Harap isi dengan lengkap.")
            return

        try:
            price = int(amount_text)
        except ValueError:
            QMessageBox.warning(self, "Input tidak valid", "Harga satuan harus berupa angka.")
            return

        if price <= 0 or quantity <= 0:
            QMessageBox.warning(self, "Input tidak valid", "Jumlah item dan harga satuan harus lebih dari 0.")
            return

        total = quantity * price
        self.expenses.append((desc, category, quantity, price, total, date))
        self.update_table()

        self.ui.txt_description.clear()
        self.ui.txt_amount.clear()
        self.ui.spin_quantity.setValue(1)

    def clear_expenses(self):
        self.expenses = []
        self.update_table()

    def update_table(self):
        self.ui.table_expense.setRowCount(len(self.expenses))
        total_all = 0

        for row, (desc, category, quantity, price, total, date) in enumerate(self.expenses):
            self.ui.table_expense.setItem(row, 0, QTableWidgetItem(desc))
            self.ui.table_expense.setItem(row, 1, QTableWidgetItem(category))
            self.ui.table_expense.setItem(row, 2, QTableWidgetItem(str(quantity)))
            self.ui.table_expense.setItem(row, 3, QTableWidgetItem(f"Rp. {price:,}"))
            self.ui.table_expense.setItem(row, 4, QTableWidgetItem(f"Rp. {total:,}"))
            self.ui.table_expense.setItem(row, 5, QTableWidgetItem(date))
            total_all += total

        self.ui.lbl_total.setText(f"Total: Rp. {total_all:,}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseApp()
    window.show()
    sys.exit(app.exec_())

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QSpinBox, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QGroupBox
)

from model.order_model import OrderModel
from gui.shared.custom_popup.custom_popup import CustomPopup
from gui.shared.custom_popup.custom_popop_level import CustomPopupLevel
import uuid
from util.validate_date import validate_date
from datetime import datetime
class OrderUI(QWidget):
    def __init__(self, send_order, order_service, order_product_service, parent=None):
        super().__init__(parent)
        self.send_order = send_order
        self.order_service = order_service
        self.order_product_service = order_product_service

        root = QVBoxLayout(self)

        form_box = QGroupBox("Create Order")
        form_layout = QVBoxLayout(form_box)

        fields = QFormLayout()
        form_layout.addLayout(fields)

        self.customer_input = QLineEdit()
        self.customer_input.setPlaceholderText("e.g. C001")
        fields.addRow("Customer ID:", self.customer_input)

        self.date_input = QLineEdit()
        self.date_input.setText(datetime.today().strftime("%Y-%m-%d"))        
        self.date_input.setPlaceholderText("YYYY-MM-DD")
        fields.addRow("Order Date:", self.date_input)

        self.priority_input = QSpinBox()
        self.priority_input.setRange(1, 10)
        self.priority_input.setValue(1)
        fields.addRow("Priority:", self.priority_input)

        self.lines_table = QTableWidget(0, 2)
        self.lines_table.setHorizontalHeaderLabels(["productCode", "quantity"])
        form_layout.addWidget(QLabel("Order Items:"))
        form_layout.addWidget(self.lines_table)

        btns = QHBoxLayout()
        form_layout.addLayout(btns)

        self.add_line_btn = QPushButton("Add line")
        self.remove_line_btn = QPushButton("Remove selected line")
        self.create_order_btn = QPushButton("Send order")
        btns.addWidget(self.add_line_btn)
        btns.addWidget(self.remove_line_btn)
        btns.addStretch(1)
        btns.addWidget(self.create_order_btn)

        root.addWidget(form_box)

        orders_box = QGroupBox("Orders")
        orders_layout = QVBoxLayout(orders_box)

        self.refresh_orders_btn = QPushButton("Refresh orders")
        orders_layout.addWidget(self.refresh_orders_btn)

        self.orders_table = QTableWidget(0, 5)
        self.orders_table.setHorizontalHeaderLabels(["orderId", "customerId", "orderDate", "priority", "status"])
        self.orders_table.setSortingEnabled(True)
        orders_layout.addWidget(self.orders_table)

        root.addWidget(orders_box)

        items_box = QGroupBox("Order Items (selected order)")
        items_layout = QVBoxLayout(items_box)

        self.items_table = QTableWidget(0, 5)
        self.items_table.setHorizontalHeaderLabels(["orderId", "productCode", "qtyOrdered", "qtyFulfilled", "status"])
        self.items_table.setSortingEnabled(True)
        items_layout.addWidget(self.items_table)

        root.addWidget(items_box)

        self.add_line_btn.clicked.connect(self._add_empty_line)
        self.remove_line_btn.clicked.connect(self.remove_selected_line)
        self.create_order_btn.clicked.connect(self._on_send_order)

        self.refresh_orders_btn.clicked.connect(self.reload_orders)
        self.orders_table.itemSelectionChanged.connect(self._on_order_selected)

        self.reload_orders()
        
    def _add_empty_line(self):
        r = self.lines_table.rowCount()
        self.lines_table.insertRow(r)
        self.lines_table.setItem(r, 0, QTableWidgetItem(""))  # productCode
        self.lines_table.setItem(r, 1, QTableWidgetItem("1"))  # quantity

    def remove_selected_line(self):
        r = self.lines_table.currentRow()
        if r >= 0:
            self.lines_table.removeRow(r)

    def _read_lines(self):
        lines = []
        for r in range(self.lines_table.rowCount()):
            code_item = self.lines_table.item(r, 0)
            qty_item = self.lines_table.item(r, 1)

            code = (code_item.text().strip() if code_item else "")
            qty_raw = (qty_item.text().strip() if qty_item else "")

            if not code:
                continue

            try:
                qty = int(qty_raw)
            except ValueError:
                qty = 0

            if qty <= 0:
                continue

            lines.append({"productCode": code, "quantity": qty})

        return lines

    def _on_send_order(self):
        customer_id = self.customer_input.text().strip()
        order_date = self.date_input.text().strip()
        priority = int(self.priority_input.value())
        product_lines = self._read_lines()

        if not customer_id:
            dlg = CustomPopup(CustomPopupLevel.WARNING,"Customer ID is not must empty!")
            dlg.exec()
            return
        elif not order_date and validate_date(order_date): 
            dlg = CustomPopup(CustomPopupLevel.WARNING,"Order Date is not must empty!")
            dlg.exec()
            return
        elif not product_lines:
            dlg = CustomPopup(CustomPopupLevel.WARNING,"Product Line is not must empty!")
            dlg.exec()
            return
        
        order = OrderModel(
            orderId=uuid.uuid4().__str__(),
            userId=customer_id,
            orderDate=order_date,
            priority=priority,
            status=None  
        )
        try:
            self.send_order.send_order(order, product_lines)
            self.reload_orders()
            print(f"Send Order Success:{order}")
            dlg = CustomPopup(CustomPopupLevel.INFO,f"Success Send Order with id: {order.orderId}")
            dlg.exec()
        except Exception as e:
            print(f"Error sending order: {str(e)}")
            dlg = CustomPopup(CustomPopupLevel.ERROR,f"Failed to send order: {str(e)}")
            dlg.exec()


    def reload_orders(self):
        self.date_input.setText("")
        self.customer_input.setText("")
        data = self.order_service.get_all_orders()
        orders = data.values()
        self.orders_table.setRowCount(len(orders))
        self.orders_table.setSortingEnabled(False)
        self.orders_table.clearContents()
        for r, o in enumerate(orders):
            self.orders_table.setItem(r, 0, QTableWidgetItem(str(o.orderId)))
            self.orders_table.setItem(r, 1, QTableWidgetItem(str(getattr(o, "userId", ""))))
            self.orders_table.setItem(r, 2, QTableWidgetItem(str(getattr(o, "orderDate", ""))))
            self.orders_table.setItem(r, 3, QTableWidgetItem(str(getattr(o, "priority", ""))))
            self.orders_table.setItem(r, 4, QTableWidgetItem(str(getattr(o, "status", ""))))
        self.orders_table.resizeColumnsToContents()
        self.orders_table.resizeRowsToContents()
        self.orders_table.viewport().update()
        self.orders_table.repaint()
        self.items_table.setRowCount(0)

    def _on_order_selected(self):
        selected = self.orders_table.selectedItems()
        if not selected:
            return

        order_id = self.orders_table.item(self.orders_table.currentRow(), 0).text().strip()
        if not order_id:
            return

        items = self.order_product_service.get_order_products_by_order_id(order_id)
        self._render_items(items.values())

    def _render_items(self, items):
        self.items_table.setRowCount(len(items))
        self.items_table.setSortingEnabled(False)
        self.items_table.clearContents()
        for r, it in enumerate(items):
            self.items_table.setItem(r, 0, QTableWidgetItem(getattr(it, "orderId", "")))
            self.items_table.setItem(r, 1, QTableWidgetItem(getattr(it, "productCode", "")))
            self.items_table.setItem(r, 2, QTableWidgetItem(str(getattr(it, "quantityOrdered", ""))))
            self.items_table.setItem(r, 3, QTableWidgetItem(str(getattr(it, "quantityFulfilled", ""))))
            self.items_table.setItem(r, 4, QTableWidgetItem(getattr(it, "status", "")))
        self.items_table.resizeColumnsToContents()
        self.items_table.resizeRowsToContents()
        self.items_table.viewport().update()
        self.items_table.repaint()
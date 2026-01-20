import xlwt


def generate_excel(data, file_path):
    workbook = xlwt.Workbook()
    sheet_daily_report = workbook.add_sheet("daily_report")
    sheet_product_most_fulfilled = workbook.add_sheet("product_most_fulfilled")

    headers_daily = {0: "numberOrders", 1: "numberOrderCompleted", 2: "numberOrderPending"}
    for col, header in enumerate(headers_daily):
        sheet_daily_report.write(0, col, header)

    headers_product_most_fulfilled = {0: "productCode", 1: "quantityFulfilled"}
    for col, header in enumerate(headers_product_most_fulfilled):
        sheet_product_most_fulfilled.write(0, col, header)
    for row_idx, row_data in enumerate(data["productsMostFulfilled"], start=1):
        for col_idx, cell_data in enumerate(row_data):
            sheet_product_most_fulfilled.write(row_idx, col_idx, cell_data)
    for col_idx, row_data in enumerate(data["dailyReport"]):
        sheet_daily_report.write(1, col_idx, row_data)

    workbook.save(file_path)
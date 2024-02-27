#!/usr/bin/env python
import csv
import os

from PyPDF2 import PdfReader

# TODO: 3


def is_type(value, value_type):
    try:
        value_type(value)
        return True
    except ValueError:
        return False


def load_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()
    return text


def print_well_formatted_dict(my_dict):
    # Print formatted product information
    for product, details in my_dict.items():
        print(f"Description: {product}")
        for key, value in details.items():
            print(f"  {key}: {value}")
        print()  # Print an empty line for better readability

    print("LEN OF PRODUCTS:\t", len(my_dict))


def write_products_dictionary(my_dict, description, product, qty, price, amount):
    my_dict[description] = {
        'Product': product,
        'Quantity': qty,
        'Price per unit': f"{price} €",
        'Total amount': amount
    }


def process_pdf_file(pdf_path):
    print("PATH:\t", pdf_path)
    pdf_text = load_pdf(pdf_path)
    lines = pdf_text.split("\n")

    products = {}

    print_lines = False
    for line in lines:
        product = ""
        qty = ""
        description = ""
        amount = ""
        if not print_lines:
            if "Producto Descripción Unidades Importe Precio" in line:
                print_lines = True
            if "Uds . Precio Importe Producto Descripción" in line:
                print_lines = True
        else:
            if "CANON DIGITAL" in line:
                continue
            if "COMENTARIO:" in line:
                print_lines = False
            elif "B. Imponible" in line:
                print_lines = False
            elif "Total" in line:
                print_lines = False
            else:
                reversed_line = line[::-1]

                line_str = line.replace('.', '').replace(',', '.')

                temp_list = line_str.split(" ")[:-1]

                # Precio
                try:
                    price = temp_list[::-1][0]
                    temp_list.remove(price)
                except Exception as e:
                    print("PRICE EXCEPTION:", e)
                    continue

                temp_list = temp_list[::-1]

                if is_type(temp_list[1], float):
                    amount = temp_list[1]
                    temp_list.remove(amount)
                    # amount = "{:,.2f} €".format(float(amount))
                    amount = "{:.2f} €".format(float(amount))
                else:
                    if not is_type(temp_list[0], float):
                        product = (temp_list[0][::-1] + temp_list[1][::-1])[::-1]
                        temp_list.remove(temp_list[0])
                        temp_list.remove(temp_list[1])

                        try:
                            qty = temp_list[1]
                            temp_list.remove(qty)
                        except IndexError:
                            continue
                    else:
                        price = temp_list[0]
                        temp_list.remove(price)

                        try:
                            qty = str(int(temp_list[2]))
                            temp_list.remove(qty)
                        except Exception as e:
                            qty = temp_list
                            for item in range(len(qty)):
                                if int(item):
                                    qty = str(item)
                                    break
                            temp_list.remove(qty)
                            pass

                        product = temp_list[1]

                        temp_list.remove(product)

                if not qty:
                    try:
                        qty = temp_list[0]
                        temp_list.remove(qty)
                    except Exception as e:
                        # print("QTY EXCEPTION: ", e)
                        print("XD")
                        if not description:
                            description = " ".join(" ".join(temp_list[::-1][:-1]).split(" ")[::-1][2:][::-1])
                            new_line = line.replace(str(description) + " ", "")
                        qty = new_line.split(" ")[1].replace(",", ".")
                        if not price:
                            price = new_line.split(" ")[2].replace(",", ".")
                        if not product:
                            product = new_line.split(" ")[::-1][0]
                        if not amount:
                            amount = "{:.2f} €".format(float(price) * float(qty))
                        pass

                if not product:
                    product = temp_list[0]
                    temp_list.remove(product)

                if not amount:
                    try:
                        amount = "{:.2f} €".format(float(price) * float(qty))
                    # amount = str(float(price.split(" ")[0]) * float(qty)) + " €"
                    except Exception as e:
                        # print("AMOUNT EXCEPTION:", e)
                        continue

                if not description:
                    try:
                        description = " ".join(temp_list[::-1])
                    except Exception as e:
                        print("EXCEPTION, DESCRIPTION COULD NOT BE WRITTEN.\n", e)

                if description and product and qty and price and amount:
                    write_products_dictionary(products, description, product, qty, price, amount)

    if products:
        print_well_formatted_dict(products)

    return products


def main():
    product_details = []

    for filename in os.listdir('deliveries'):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join('deliveries', filename)
            products = process_pdf_file(pdf_path)
            for description, details in products.items():
                product_details.append([
                    description,
                    details['Product'],
                    details['Quantity'],
                    details['Price per unit'],
                    details['Total amount']
                ])

    with open('products_details.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Description', 'Quantity', 'Product', 'Price per unit', 'Total amount'])
        csvwriter.writerows(product_details)


if __name__ == '__main__':
    main()

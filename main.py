#!/usr/bin/env python
from PyPDF2 import PdfReader
import re

file_name = 1
# TODO: 3 + 5 (multiple line product), 4 (qty), 6 (qty, product), 7 (product, amount)


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_int(value):
    try:
        int(value)
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


def main():
    pdf_text = load_pdf(f"deliveries/{file_name}.pdf")

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

                line_str = line.replace(',', '.')

                temp_list = line_str.split(" ")[:-1]

                # Precio
                try:
                    price = temp_list[::-1][0]
                    temp_list.remove(price)
                except Exception as e:
                    print("PRICE EXCEPTION:", e)
                    continue

                temp_list = temp_list[::-1]

                if is_float(temp_list[1]):
                    amount = temp_list[1]
                    temp_list.remove(amount)
                    amount = "{:,.2f} €".format(float(amount))
                else:
                    if not is_float(temp_list[0]):
                        product = (temp_list[0][::-1] + temp_list[1][::-1])[::-1]
                        temp_list.remove(temp_list[0])
                        temp_list.remove(temp_list[1])

                        try:
                            qty = temp_list[1]
                            temp_list.remove(qty)
                        except IndexError:
                            continue
                    else:
                        product = temp_list[1]
                        price = temp_list[0]
                        qty = temp_list[2]
                        temp_list.remove(product)
                        temp_list.remove(price)
                        temp_list.remove(qty)

                if not product:
                    product = temp_list[0]
                    temp_list.remove(product)

                if not qty:
                    qty = temp_list[0]
                    temp_list.remove(qty)

                if not amount:
                    amount = "{:,.2f} €".format(float(price) * float(qty))
                    # amount = str(float(price.split(" ")[0]) * float(qty)) + " €"


                if not description:
                    try:
                        description = " ".join(temp_list[::-1])
                    except Exception as e:
                        print("EXCEPTION, DESCRIPTION COULD NOT BE WRITTEN.\n", e)

            if description and product and qty and price and amount:
                write_products_dictionary(products, description, product, qty, price, amount)

    if products:
        print_well_formatted_dict(products)


if __name__ == '__main__':
    main()

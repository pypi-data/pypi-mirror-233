import base64
import json
import xml.etree.ElementTree as ET

from django.http import HttpResponse

from takamol_einvoicer_test_kit4.einvoices.constants import INVOICE_TITLE, SELLER_INFO, SELLER_ADDRESS
from takamol_einvoicer_test_kit4.einvoices.helpers import convert_qr_code_into_image_url, get_items
from takamol_einvoicer_test_kit4.einvoices.models import Invoice, Item


class InvoiceService:

    @classmethod
    def generate_invoice(cls, invoice_type, items_list, invoice_data):
        """
        Generates an invoice for the specified type with the provided data.

        @param invoice_type: Simplified, Standard
        @param invoice_data: mandatory fields
        @param items_list: A list of items to associate with the invoice
        @return: an invoice object
        """
        invoice_kwargs = {
            'model_name': invoice_type,
            **invoice_data,
        }

        invoice = Invoice.objects.create(**invoice_kwargs)

        # Create associated items
        if items_list is not None:
            for item_data in items_list:
                Item.objects.create(invoice=invoice, **item_data)

        return invoice

    # TODO It might be better to relocate it to another position, as it doesn't seem to fit well with the current
    #  structure.

    @classmethod
    def store_b2b_invoice(cls, invoice, encoded_invoice):
        """
        Store a B2B (Business-to-Business) invoice in the database.

        @param encoded_invoice: xml invoice encoded as base 64
        @param invoice: invoice object
        """
        invoice.encoded_invoice = encoded_invoice
        invoice.qr_code = cls.extract_qr_code(encoded_invoice)
        invoice.save()

    @classmethod
    def extract_qr_code(cls, encoded_invoice):
        """
        Extract the QR code from the encoded XML invoice (B2B).

        @param encoded_invoice: xml invoice encoded as base 64
        @return: the qr code for the invoice
        """
        decoded_invoice = base64.b64decode(encoded_invoice.encode("utf-8"))

        root = ET.fromstring(decoded_invoice)

        namespaces = {
            'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
            'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
        }

        additional_doc_ref = root.find(".//cac:AdditionalDocumentReference[cbc:ID='QR']", namespaces)

        embedded_doc_binary = additional_doc_ref.find("cac:Attachment/cbc:EmbeddedDocumentBinaryObject", namespaces)

        return embedded_doc_binary.text

    # TODO generate a new pdf service to handle pdf functions
    @classmethod
    def generate_invoice_pdf_data(cls, invoice, buyer):
        """
        Generate the data in JSON format required for generating the invoice PDF.

        @param invoice: The invoice object for which the data is generated.
        @param buyer: The buyer object associated with the invoice.
        @return: A JSON string containing the necessary data for the invoice PDF generation.
        """
        data = {
            'title_ar': INVOICE_TITLE[invoice.model_name][invoice.type]['ar'],
            'title_en': INVOICE_TITLE[invoice.model_name][invoice.type]['en'],
            'seller_registration_name': SELLER_INFO["registration_name"],
            'seller_address': SELLER_ADDRESS,
            'seller_tax_number': invoice.tax_number,
            'seller_crn_number': SELLER_INFO["CRN"],
            'buyer_registration_name': buyer.registration_name,
            'buyer_address': buyer.address,
            'buyer_tax_number': buyer.tax_number,
            'buyer_crn_number': buyer.crn_number,
            'date': invoice.created_at.date(),
            'time': invoice.created_at.time(),
            'number': invoice.serial_number,
            'document_reference_number': invoice.get_parent_id_invoice_number,
            'document_note': invoice.note,
            'items': get_items(invoice),
            'total_excluding_vat': invoice.total_excluding_vat,
            'total_including_vat': invoice.total_including_vat,
            'vat_amount': invoice.vat_amount,
            'vat_rate': invoice.vat_rate,
            'qr_code': convert_qr_code_into_image_url(invoice.qr_code)

        }

        json_data = json.dumps(data)

        return HttpResponse(json_data, content_type='application/json')

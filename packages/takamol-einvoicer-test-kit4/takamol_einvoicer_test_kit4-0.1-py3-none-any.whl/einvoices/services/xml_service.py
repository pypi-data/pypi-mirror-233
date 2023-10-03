import xml.etree.ElementTree as ET

from takamol_einvoicer_test_kit4.einvoices.constants import INVOICE_TYPE_CODES_NAMES, INVOICE_TYPE_CODES, SELLER_INFO, SELLER_ADDRESS
from takamol_einvoicer_test_kit4.einvoices.helpers import convert_xml_str_to_encoded64
from takamol_einvoicer_test_kit4.einvoices.models import Invoice
from script.zatca_tool import sign_and_generate_hash, generate_qr, extract_hash_string, validate_invoice


class XmlService:

    # TODO: change the invoice xml generation func to accept the discount attribute and the type of discount (
    #  document level or line items level)
    @classmethod
    def create_invoice_xml(cls, invoice_data, buyer_info):
        """
        @param buyer_info:Buyer information object.
        @param invoice_data: invoice object (Simplified, Standard)
        @return: the invoice as xml format
        """
        # Create the invoice element
        invoice = ET.Element("Invoice", attrib={
            "xmlns": "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2",
            "xmlns:cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "xmlns:cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
            "xmlns:ext": "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2",

        })
        invoice_with_ubl_extensions = cls.create_ubl_extensions(invoice)

        final_invoice = cls.create_invoice_elements(invoice_with_ubl_extensions, invoice_data, buyer_info)

        xml = ET.tostring(final_invoice, encoding="utf-8", method="xml", xml_declaration=True)
        # TODO sign the invoice / handle the errors
        signing_result = sign_and_generate_hash(xml.decode("utf-8"))
        if signing_result['success']:
            signed_invoice = signing_result['signed_invoice']
            invoice_data.hash_key = extract_hash_string(signing_result['logs'])

            # TODO append QR code to the invoice / handle the errors
            qr_result = generate_qr(signed_invoice)
            if qr_result['success']:
                invoice_data.qr_code = qr_result['qr']

                # TODO validate the invoice / handle the errors
                validation_result = validate_invoice(signed_invoice)
                if validation_result['valid']:
                    # TODO encoded the invoice_xml to store it in invoice obj / handle the errors
                    invoice_data.encoded_invoice = convert_xml_str_to_encoded64(signed_invoice)

                    invoice_data.save()
                    return True, signed_invoice

        # TODO handle all possible errors
        return False, "Issue"

    @classmethod
    def create_ubl_extensions(cls, invoice):
        """
        Create UBL extensions element for the given invoice xml.

        @param invoice: xml object.
        @return: the invoice xml with ubl extensions.
        """
        # Create the UBLExtensions element and its children
        ubl_extensions = ET.SubElement(invoice, "ext:UBLExtensions")
        ubl_extension = ET.SubElement(ubl_extensions, "ext:UBLExtension")
        extension_uri = ET.SubElement(ubl_extension, "ext:ExtensionURI")
        extension_uri.text = "urn:oasis:names:specification:ubl:dsig:enveloped:xades"
        extension_content = ET.SubElement(ubl_extension, "ext:ExtensionContent")
        ubl_document_signatures = ET.SubElement(extension_content, "sig:UBLDocumentSignatures", attrib={
            "xmlns:sig": "urn:oasis:names:specification:ubl:schema:xsd:CommonSignatureComponents-2",
            "xmlns:sac": "urn:oasis:names:specification:ubl:schema:xsd:SignatureAggregateComponents-2",
            "xmlns:sbc": "urn:oasis:names:specification:ubl:schema:xsd:SignatureBasicComponents-2"
        })

        # Create the SignatureInformation element and its children
        signature_information = ET.SubElement(ubl_document_signatures, "sac:SignatureInformation")
        id_element = ET.SubElement(signature_information, "cbc:ID")
        id_element.text = "urn:oasis:names:specification:ubl:signature:1"
        referenced_signature_id = ET.SubElement(signature_information, "sbc:ReferencedSignatureID")
        referenced_signature_id.text = "urn:oasis:names:specification:ubl:signature:Invoice"
        signature = ET.SubElement(signature_information, "ds:Signature", attrib={
            "xmlns:ds": "http://www.w3.org/2000/09/xmldsig#",
            "Id": "signature"
        })
        # Create the SignedInfo element and its children
        signed_info = ET.SubElement(signature, "ds:SignedInfo")
        canonicalization_method = ET.SubElement(signed_info, "ds:CanonicalizationMethod", attrib={
            "Algorithm": "http://www.w3.org/2006/12/xml-c14n11"
        })
        signature_method = ET.SubElement(signed_info, "ds:SignatureMethod", attrib={
            "Algorithm": "http://www.w3.org/2001/04/xmldsig-more#ecdsa-sha256"
        })
        reference = ET.SubElement(signed_info, "ds:Reference", attrib={
            "Id": "invoiceSignedData",
            "URI": ""
        })

        # Create the Transforms element and its children
        transforms = ET.SubElement(reference, "ds:Transforms")
        transform1 = ET.SubElement(transforms, "ds:Transform", attrib={
            "Algorithm": "http://www.w3.org/TR/1999/REC-xpath-19991116"
        })
        xpath1 = ET.SubElement(transform1, "ds:XPath")
        xpath1.text = "not(//ancestor-or-self::ext:UBLExtensions)"

        transform2 = ET.SubElement(transforms, "ds:Transform", attrib={
            "Algorithm": "http://www.w3.org/TR/1999/REC-xpath-19991116"
        })
        xpath2 = ET.SubElement(transform2, "ds:XPath")
        xpath2.text = "not(//ancestor-or-self::cac:Signature)"

        transform3 = ET.SubElement(transforms, "ds:Transform", attrib={
            "Algorithm": "http://www.w3.org/TR/1999/REC-xpath-19991116"
        })
        xpath3 = ET.SubElement(transform3, "ds:XPath")
        xpath3.text = "not(//ancestor-or-self::cac:AdditionalDocumentReference[cbc:ID='QR'])"

        transform4 = ET.SubElement(transforms, "ds:Transform", attrib={
            "Algorithm": "http://www.w3.org/2006/12/xml-c14n11"
        })

        # Create the DigestMethod element
        digest_method = ET.SubElement(reference, "ds:DigestMethod", attrib={
            "Algorithm": "http://www.w3.org/2001/04/xmlenc#sha256"
        })

        # Create the DigestValue element
        digest_value = ET.SubElement(reference, "ds:DigestValue")

        # Create the SignatureValue element
        signature_value = ET.SubElement(signature, "ds:SignatureValue")

        # Create the KeyInfo element and its children
        key_info = ET.SubElement(signature, "ds:KeyInfo")
        x509_data = ET.SubElement(key_info, "ds:X509Data")
        x509_certificate = ET.SubElement(x509_data, "ds:X509Certificate")

        # Create the Object element and its children
        obj = ET.SubElement(signature, "ds:Object")
        qualifying_properties = ET.SubElement(obj, "xades:QualifyingProperties", attrib={
            "xmlns:xades": "http://uri.etsi.org/01903/v1.3.2#",
            "Target": "signature"
        })
        signed_properties = ET.SubElement(qualifying_properties, "xades:SignedProperties", attrib={
            "Id": "xadesSignedProperties"
        })
        signed_signature_properties = ET.SubElement(signed_properties, "xades:SignedSignatureProperties")
        signing_time = ET.SubElement(signed_signature_properties, "xades:SigningTime")
        signing_certificate = ET.SubElement(signed_signature_properties, "xades:SigningCertificate")
        cert = ET.SubElement(signing_certificate, "xades:Cert")
        cert_digest = ET.SubElement(cert, "xades:CertDigest")
        digest_method = ET.SubElement(cert_digest, "ds:DigestMethod", attrib={
            "Algorithm": "http://www.w3.org/2001/04/xmlenc#sha256"
        })
        digest_value = ET.SubElement(cert_digest, "ds:DigestValue")
        issuer_serial = ET.SubElement(cert, "xades:IssuerSerial")
        x509_issuer_name = ET.SubElement(issuer_serial, "ds:X509IssuerName")
        x509_serial_number = ET.SubElement(issuer_serial, "ds:X509SerialNumber")

        return invoice

    @classmethod
    def create_invoice_elements(cls, invoice_xml, invoice_data, buyer_info):
        """
        Create invoice elements in the provided invoice XML based on the given invoice data and buyer information.

        @param invoice_xml: The XML element representing the invoice to be populated.
        @param invoice_data: The data of the invoice.
        @param buyer_info: The information of the buyer.
        @return: The invoice xml after adding new tags and populating them with invoice data.
        """
        # Add the ProfileID element
        profile_id = ET.SubElement(invoice_xml, "cbc:ProfileID")
        profile_id.text = "reporting:1.0"

        # Add the ID element
        id_element = ET.SubElement(invoice_xml, "cbc:ID")
        id_element.text = invoice_data.serial_number

        # Add the UUID element
        uuid = ET.SubElement(invoice_xml, "cbc:UUID")
        uuid.text = f"{invoice_data.id}"

        # Add the IssueDate element
        issue_date = ET.SubElement(invoice_xml, "cbc:IssueDate")
        issue_date.text = invoice_data.created_at.strftime('%Y-%m-%d')

        # Add the IssueTime element
        issue_time = ET.SubElement(invoice_xml, "cbc:IssueTime")
        issue_time.text = invoice_data.created_at.strftime('%H:%M:%S')

        # Add the InvoiceTypeCode element
        invoice_type_code_constant = invoice_data.model_name
        invoice_type_code = ET.SubElement(invoice_xml, "cbc:InvoiceTypeCode",
                                          attrib={"name": INVOICE_TYPE_CODES_NAMES.get(invoice_type_code_constant)})
        invoice_type_code.text = INVOICE_TYPE_CODES.get(invoice_data.type)

        # Add the Note element
        note = ET.SubElement(invoice_xml, "cbc:Note", attrib={"languageID": "ar"})

        if invoice_data.type != Invoice.TAX:
            note.text = invoice_data.note

        # Add the DocumentCurrencyCode element
        document_currency_code = ET.SubElement(invoice_xml, "cbc:DocumentCurrencyCode")
        document_currency_code.text = "SAR"

        # Add the TaxCurrencyCode element
        tax_currency_code = ET.SubElement(invoice_xml, "cbc:TaxCurrencyCode")
        tax_currency_code.text = "SAR"

        if invoice_data.type != Invoice.TAX:
            # Add the BillingReference element for credit and debit
            invoice_xml = cls.create_billing_reference(invoice_xml, invoice_data)

        # Add the AdditionalDocumentReference elements
        additional_document_reference1 = ET.SubElement(invoice_xml, "cac:AdditionalDocumentReference")
        additional_document_reference1_id = ET.SubElement(additional_document_reference1, "cbc:ID")
        additional_document_reference1_id.text = "ICV"
        additional_document_reference1_uuid = ET.SubElement(additional_document_reference1, "cbc:UUID")
        additional_document_reference1_uuid.text = f"{invoice_data.icv}"

        additional_document_reference2 = ET.SubElement(invoice_xml, "cac:AdditionalDocumentReference")
        additional_document_reference2_id = ET.SubElement(additional_document_reference2, "cbc:ID")
        additional_document_reference2_id.text = "PIH"
        attachment2 = ET.SubElement(additional_document_reference2, "cac:Attachment")
        embedded_document_binary_object2 = ET.SubElement(attachment2, "cbc:EmbeddedDocumentBinaryObject",
                                                         attrib={"mimeCode": "text/plain"})

        embedded_document_binary_object2.text = invoice_data.get_phk

        # Add the AdditionalDocumentReference for QR code
        additional_document_reference3 = ET.SubElement(invoice_xml, "cac:AdditionalDocumentReference")
        additional_document_reference3_id = ET.SubElement(additional_document_reference3, "cbc:ID")
        additional_document_reference3_id.text = "QR"
        attachment3 = ET.SubElement(additional_document_reference3, "cac:Attachment")
        embedded_document_binary_object3 = ET.SubElement(attachment3, "cbc:EmbeddedDocumentBinaryObject",
                                                         attrib={"mimeCode": "text/plain"})
        # this will be gotten from SDK
        embedded_document_binary_object3.text = ""

        # Add the Signature element
        signature = ET.SubElement(invoice_xml, "cac:Signature")
        signature_id = ET.SubElement(signature, "cbc:ID")
        signature_id.text = "urn:oasis:names:specification:ubl:signature:Invoice"
        signature_method = ET.SubElement(signature, "cbc:SignatureMethod")
        signature_method.text = "urn:oasis:names:specification:ubl:dsig:enveloped:xades"

        # Add the AccountingSupplierParty element
        accounting_supplier_party = ET.SubElement(invoice_xml, "cac:AccountingSupplierParty")
        seller_party = ET.SubElement(accounting_supplier_party, "cac:Party")
        seller_party_identification = ET.SubElement(seller_party, "cac:PartyIdentification")
        seller_party_id = ET.SubElement(seller_party_identification, "cbc:ID", attrib={"schemeID": "CRN"})
        seller_party_id.text = SELLER_INFO.get("CRN")
        seller_postal_address = ET.SubElement(seller_party, "cac:PostalAddress")
        seller_street_name = ET.SubElement(seller_postal_address, "cbc:StreetName")
        seller_street_name.text = SELLER_ADDRESS.get("street_name")
        seller_building_number = ET.SubElement(seller_postal_address, "cbc:BuildingNumber")
        seller_building_number.text = SELLER_ADDRESS.get("building_number")
        seller_plot_identification = ET.SubElement(seller_postal_address, "cbc:PlotIdentification")
        seller_plot_identification.text = SELLER_ADDRESS.get("building_number")
        seller_city_subdivision_name = ET.SubElement(seller_postal_address, "cbc:CitySubdivisionName")
        seller_city_subdivision_name.text = ' | '.join(SELLER_ADDRESS["city"])
        seller_city_name = ET.SubElement(seller_postal_address, "cbc:CityName")
        seller_city_name.text = ' | '.join(SELLER_ADDRESS["city"])
        seller_postal_zone = ET.SubElement(seller_postal_address, "cbc:PostalZone")
        seller_postal_zone.text = SELLER_ADDRESS.get("postal_zone")
        seller_country = ET.SubElement(seller_postal_address, "cac:Country")
        seller_identification_code = ET.SubElement(seller_country, "cbc:IdentificationCode")
        seller_identification_code.text = "SA"
        seller_party_tax_scheme = ET.SubElement(seller_party, "cac:PartyTaxScheme")
        seller_company_id = ET.SubElement(seller_party_tax_scheme, "cbc:CompanyID")
        seller_company_id.text = SELLER_INFO.get("company_ID")
        seller_tax_scheme = ET.SubElement(seller_party_tax_scheme, "cac:TaxScheme")
        seller_tax_scheme_id = ET.SubElement(seller_tax_scheme, "cbc:ID")
        seller_tax_scheme_id.text = "VAT"
        seller_party_legal_entity = ET.SubElement(seller_party, "cac:PartyLegalEntity")
        seller_registration_name = ET.SubElement(seller_party_legal_entity, "cbc:RegistrationName")
        seller_registration_name.text = SELLER_INFO.get("registration_name")

        # Add the AccountingCustomerParty element (buyer)
        accounting_customer_party = ET.SubElement(invoice_xml, "cac:AccountingCustomerParty")
        buyer_party = ET.SubElement(accounting_customer_party, "cac:Party")
        if invoice_type_code_constant == "Standard":
            buyer_party = cls.create_party_identification(buyer_party, buyer_info)
        buyer_postal_address = ET.SubElement(buyer_party, "cac:PostalAddress")
        buyer_street_name = ET.SubElement(buyer_postal_address, "cbc:StreetName")
        buyer_street_name.text = buyer_info["street_name"]
        if invoice_type_code_constant != "Standard":
            buyer_city_subdivision_name = ET.SubElement(buyer_postal_address, "cbc:CitySubdivisionName")
            buyer_city_subdivision_name.text = buyer_info["city_subdivision_name"]
        if invoice_type_code_constant == "Standard":
            buyer_postal_address = cls.create_b2b_extra_address_info(buyer_postal_address, buyer_info)
        buyer_country = ET.SubElement(buyer_postal_address, "cac:Country")
        buyer_identification_code = ET.SubElement(buyer_country, "cbc:IdentificationCode")
        buyer_identification_code.text = "SA"
        buyer_party_tax_scheme = ET.SubElement(buyer_party, "cac:PartyTaxScheme")
        buyer_tax_scheme = ET.SubElement(buyer_party_tax_scheme, "cac:TaxScheme")
        buyer_tax_scheme_id = ET.SubElement(buyer_tax_scheme, "cbc:ID")
        buyer_tax_scheme_id.text = "VAT"
        buyer_party_legal_entity = ET.SubElement(buyer_party, "cac:PartyLegalEntity")
        buyer_registration_name = ET.SubElement(buyer_party_legal_entity, "cbc:RegistrationName")
        buyer_registration_name.text = buyer_info["registration_name"]

        # Add the Delivery element
        if invoice_type_code_constant == "Standard" and invoice_data.actual_delivery_date is not None:
            invoice_xml = cls.create_delivery_element(invoice_xml, invoice_data)

        # Add the PaymentMeans element
        payment_means = ET.SubElement(invoice_xml, "cac:PaymentMeans")
        payment_means_code = ET.SubElement(payment_means, "cbc:PaymentMeansCode")
        # 10 means online payment
        payment_means_code.text = "10"

        # TODO call create_allowance_charge_element if there is a discount
        # if discount:
        #
        #     invoice_xml = cls.create_allowance_charge_element(invoice_xml, invoice_data)

        # Add the TaxTotal1 element
        tax_total1 = ET.SubElement(invoice_xml, "cac:TaxTotal")
        tax_amount = ET.SubElement(tax_total1, "cbc:TaxAmount", attrib={"currencyID": "SAR"})
        tax_amount.text = f"{invoice_data.vat_amount}"

        # Add the TaxTotal2 element and its children
        tax_total2 = ET.SubElement(invoice_xml, "cac:TaxTotal")
        tax_amount2 = ET.SubElement(tax_total2, "cbc:TaxAmount", attrib={"currencyID": "SAR"})
        tax_amount2.text = f"{invoice_data.vat_amount}"

        tax_subtotal = ET.SubElement(tax_total2, "cac:TaxSubtotal")
        taxable_amount = ET.SubElement(tax_subtotal, "cbc:TaxableAmount", attrib={"currencyID": "SAR"})
        taxable_amount.text = f"{invoice_data.total_excluding_vat}"

        tax_total_tax_amount = ET.SubElement(tax_subtotal, "cbc:TaxAmount", attrib={"currencyID": "SAR"})
        tax_total_tax_amount.text = f"{invoice_data.vat_amount}"

        tax_total_tax_category = ET.SubElement(tax_subtotal, "cac:TaxCategory")
        tax_category_id_element = ET.SubElement(tax_total_tax_category, "cbc:ID", attrib={
            "schemeID": "UN/ECE 5305",
            "schemeAgencyID": "6"
        })
        tax_category_id_element.text = "S"
        percent_element = ET.SubElement(tax_total_tax_category, "cbc:Percent")
        percent_element.text = "15.00"
        tax_scheme = ET.SubElement(tax_total_tax_category, "cac:TaxScheme")
        tax_id_element = ET.SubElement(tax_scheme, "cbc:ID", attrib={
            "schemeID": "UN/ECE 5153",
            "schemeAgencyID": "6"
        })
        tax_id_element.text = "VAT"

        # Add the LegalMonetaryTotal element (this will have the invoice data)
        legal_monetary_total = ET.SubElement(invoice_xml, "cac:LegalMonetaryTotal")
        line_extension_amount = ET.SubElement(legal_monetary_total, "cbc:LineExtensionAmount",
                                              attrib={"currencyID": "SAR"})
        line_extension_amount.text = f"{invoice_data.total_excluding_vat}"
        tax_exclusive_amount = ET.SubElement(legal_monetary_total, "cbc:TaxExclusiveAmount",
                                             attrib={"currencyID": "SAR"})
        tax_exclusive_amount.text = f"{invoice_data.total_excluding_vat}"
        tax_inclusive_amount = ET.SubElement(legal_monetary_total, "cbc:TaxInclusiveAmount",
                                             attrib={"currencyID": "SAR"})
        tax_inclusive_amount.text = f"{invoice_data.total_including_vat}"

        # if discount:
        #     allowance_total_amount = ET.SubElement(legal_monetary_total, "cbc:AllowanceTotalAmount",
        #                                            attrib={"currencyID": "SAR"})
        #     # TODO change the value in case of a discount
        #     allowance_total_amount.text = "0.00"

        pre_paid_amount = ET.SubElement(legal_monetary_total, "cbc:PrepaidAmount",
                                        attrib={"currencyID": "SAR"})
        # TODO change the value depends on the new type
        pre_paid_amount.text = "0.00"

        payable_amount = ET.SubElement(legal_monetary_total, "cbc:PayableAmount",
                                       attrib={"currencyID": "SAR"})
        payable_amount.text = f"{invoice_data.total_including_vat}"

        invoice_xml = cls.create_invoice_items(invoice_xml, invoice_data.items)

        return invoice_xml

    @classmethod
    def create_invoice_items(cls, invoice_xml, items):
        """
        Append InvoiceLine to the invoice XML and populate the XML using invoice items' data.
        @param invoice_xml: The invoice xml.
        @param items: The invoice object items.
        @return: The invoice xml with InvoiceLine
        """
        # List of invoice line data

        # Create InvoiceLine elements using a loop
        for index, item in enumerate(items):
            # Create InvoiceLine element
            invoice_line = ET.SubElement(invoice_xml, "cac:InvoiceLine")

            # Add child elements to the InvoiceLine element
            invoice_line_id = ET.SubElement(invoice_line, "cbc:ID")
            invoice_line_id.text = f"{index + 1}"

            invoice_line_quantity = ET.SubElement(invoice_line, "cbc:InvoicedQuantity", attrib={"unitCode": "PCE"})
            invoice_line_quantity.text = f"{item.quantity}"

            invoice_line_amount = ET.SubElement(invoice_line, "cbc:LineExtensionAmount", attrib={"currencyID": "SAR"})
            invoice_line_amount.text = f"{round(item.subtotal_excluding_vat, 2)}"

            tax_total = ET.SubElement(invoice_line, "cac:TaxTotal")
            tax_amount = ET.SubElement(tax_total, "cbc:TaxAmount", attrib={"currencyID": "SAR"})
            tax_amount.text = f"{round(item.vat_amount, 2)}"

            rounding_amount = ET.SubElement(tax_total, "cbc:RoundingAmount", attrib={"currencyID": "SAR"})
            rounding_amount.text = f"{round(item.subtotal_including_vat, 2)}"

            xml_item = ET.SubElement(invoice_line, "cac:Item")
            item_name = ET.SubElement(xml_item, "cbc:Name")
            item_name.text = item.description_en

            classified_tax_category = ET.SubElement(xml_item, "cac:ClassifiedTaxCategory")
            classified_tax_category_id = ET.SubElement(classified_tax_category, "cbc:ID")
            classified_tax_category_id.text = "S"

            classified_tax_category_percent = ET.SubElement(classified_tax_category, "cbc:Percent")
            classified_tax_category_percent.text = f"{item.vat_rate * 100}"

            tax_scheme = ET.SubElement(classified_tax_category, "cac:TaxScheme")
            tax_scheme_id = ET.SubElement(tax_scheme, "cbc:ID")
            tax_scheme_id.text = "VAT"

            price = ET.SubElement(invoice_line, "cac:Price")
            price_amount = ET.SubElement(price, "cbc:PriceAmount", attrib={"currencyID": "SAR"})
            price_amount.text = f"{round(item.unit_price, 2)}"
            # if discount:
            # generate an allownacecharege for the price
            # invoice_xml = cls.add_allowance_charge_to_price(price)

        return invoice_xml

    @classmethod
    def create_billing_reference(cls, invoice_xml, invoice_data):
        """
        Create a billing reference in the given invoice XML.

        @param invoice_xml: The XML element representing the invoice.
        @param invoice_data: The invoice object containing the necessary data.
        @return: The updated invoice XML with the added billing reference.
        """

        billing_reference = ET.SubElement(invoice_xml, "cac:BillingReference")
        invoice_document_reference = ET.SubElement(billing_reference, "cac:InvoiceDocumentReference")
        id_element = ET.SubElement(invoice_document_reference, "cbc:ID")
        id_element.text = invoice_data.parent_id

        return invoice_xml

    @classmethod
    def create_party_identification(cls, buyer_party, buyer_info):
        """
            Create the PartyIdentification element for the buyer party.

            @param buyer_party: The parent element to attach the PartyIdentification to.
            @param buyer_info: Buyer information object.
            @return: The created PartyIdentification element.
        """
        party_identification = ET.SubElement(buyer_party, "cac:PartyIdentification")
        # TODO change the value depends on B2B identification ) (TIN, CRN, MOM, MLS, 700, SAG, NAT, GCC, IQA, OTH)
        id_element = ET.SubElement(party_identification, "cbc:ID", attrib={
            "schemeID": "TIN"
        })
        id_element.text = buyer_info["tin"]
        return buyer_party

    @classmethod
    def create_b2b_extra_address_info(cls, buyer_postal_address, buyer_info):
        """
            Create B2B extra address information for the buyer's postal address.

            @param buyer_info:Buyer information object.
            @param buyer_postal_address: The buyer's postal address object.
            @return: The updated buyer's postal address element.
        """

        building_number = ET.SubElement(buyer_postal_address, "cbc:BuildingNumber")
        building_number.text = buyer_info["building_number"]

        plot_identification = ET.SubElement(buyer_postal_address, "cbc:PlotIdentification")
        plot_identification.text = buyer_info["plot_identification"]

        buyer_city_subdivision_name = ET.SubElement(buyer_postal_address, "cbc:CitySubdivisionName")
        buyer_city_subdivision_name.text = buyer_info["city_subdivision_name"]

        city_name = ET.SubElement(buyer_postal_address, "cbc:CityName")
        city_name.text = buyer_info["city_name"]

        postal_zone = ET.SubElement(buyer_postal_address, "cbc:PostalZone")
        postal_zone.text = buyer_info["postal_zone"]

        return buyer_postal_address

    @classmethod
    def create_delivery_element(cls, invoice_xml, invoice_date):
        """
        Create the Delivery element in the invoice XML.
        @param invoice_xml: The XML element representing the invoice.
        @param invoice_date: The invoice date object containing the actual delivery date.
        @return: The updated invoice XML element.
        """
        delivery = ET.SubElement(invoice_xml, "cac:Delivery")
        actual_delivery_date = ET.SubElement(delivery, "cbc:ActualDeliveryDate")
        actual_delivery_date.text = invoice_date.actual_delivery_date

        return invoice_xml

    @classmethod
    def create_allowance_charge_element(cls, invoice_xml, invoice_data):
        """
            Adds an AllowanceCharge element to the provided invoice XML element.

            This function appends an AllowanceCharge element to the given invoice XML, representing a discount or allowance
            for the invoice. It also creates TaxCategory elements within AllowanceCharge to specify tax-related details.

            @param invoice_xml: The XML element representing the invoice to which the AllowanceCharge element will be added.
                                (Type: Element)
            @param invoice_data: The invoice data used for tax category information.

            @return: The updated invoice XML element with the added AllowanceCharge element.
             (Type: Element)
        """
        # Add the AllowanceCharge element
        allowance_charge = ET.SubElement(invoice_xml, "cac:AllowanceCharge")
        charge_indicator = ET.SubElement(allowance_charge, "cbc:ChargeIndicator")
        charge_indicator.text = "false"
        allowance_charge_reason = ET.SubElement(allowance_charge, "cbc:AllowanceChargeReason")
        allowance_charge_reason.text = "discount"
        amount = ET.SubElement(allowance_charge, "cbc:Amount", attrib={"currencyID": "SAR"})
        amount.text = "0.00"

        # Create the TaxCategory element and its children

        for _ in invoice_data.items:
            tax_category = ET.SubElement(allowance_charge, "cac:TaxCategory")
            id_element1 = ET.SubElement(tax_category, "cbc:ID", attrib={
                "schemeID": "UN/ECE 5305",
                "schemeAgencyID": "6"
            })
            id_element1.text = "S"
            percent1 = ET.SubElement(tax_category, "cbc:Percent")
            percent1.text = "15"
            seller_tax_scheme = ET.SubElement(tax_category, "cac:TaxScheme")
            id_element2 = ET.SubElement(seller_tax_scheme, "cbc:ID", attrib={
                "schemeID": "UN/ECE 5153",
                "schemeAgencyID": "6"
            })
            id_element2.text = "VAT"

        return invoice_xml

    @classmethod
    def add_allowance_charge_to_price(cls, price_element, currency="SAR"):
        """
            Adds an AllowanceCharge subelement to the provided Price element.

            This function appends an AllowanceCharge subelement to the given Price element and populates it with default values.

            @param price_element: The Price element to which the AllowanceCharge subelement will be added.
                                  (Type: Element)
            @param currency: The currency identifier for the AllowanceCharge element. Default is "SAR".
                             (Type: str)
        """
        allowance_charge = ET.SubElement(price_element, "cac:AllowanceCharge")
        charge_indicator = ET.SubElement(allowance_charge, "cbc:ChargeIndicator")
        charge_indicator.text = "false"
        allowance_charge_reason = ET.SubElement(allowance_charge, "cbc:AllowanceChargeReason")
        allowance_charge_reason.text = "discount"
        allowance_charge_amount = ET.SubElement(allowance_charge, "cbc:Amount", attrib={"currencyID": currency})
        allowance_charge_amount.text = "0.00"

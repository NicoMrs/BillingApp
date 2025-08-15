# template.py

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_RIGHT
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors

class CustomStyle:
    """ custom styles """
    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    heading = styles["Heading2"]

    left_title = ParagraphStyle(
        name = "left_tile",
        parent=styles['Normal'],
        fontSize=14,
        fontName='Helvetica-Bold',
        leading=18,
        rightIndent=0
    )

    right_title = ParagraphStyle(
        name = "right_tile",
        parent=styles['Normal'],
        fontSize=14,
        fontName='Helvetica-Bold',
        alignment=TA_RIGHT,
        leading=18,
        rightIndent=0
    )

    right = ParagraphStyle(name="right", parent=styles['Normal'], alignment=TA_RIGHT, rightIndent=0)

    @classmethod
    def get_style(cls, **kwargs):
        """ return a custom style"""
        return ParagraphStyle(name="gen", parent=cls.styles['Normal'], **kwargs)


def footer(company, TVA):
    """ Closure function to return pdf footer """

    def inner(canvas: canvas.Canvas, doc):
        canvas.saveState()
        text = [
            f"Siège social {company.street}, {company.postcode}, {company.city}, {company.country}",
            f"N°SIREN: {company.siren}"
        ]

        if TVA:
            text.append(f"N° TVA: {company.tva_number}")
        footer_text = "  -  ".join(txt for txt in text)
        canvas.setFont('Helvetica', 9)
        canvas.drawString(72, 20, footer_text)  # 30pt from left, 20pt from bottom
        canvas.restoreState()

    return inner

class BuildPDFMixin:

    """
    Mixin to generate an billing PDF using ReportLab.

    Expects the consuming class to define:
        self._elements (list) → list of Flowable objects
        self.company → object with name, street, postcode, city, country, email, phone
        self.client → object with name, street, postcode, city, country, siret
        self.bank → object with iban, bic
        self.number (str)
        self.invoice_date (str)
        self.period_month (str), self.period_year (int)
        self.quantity (float/int)
        self.unit_price (float)
        self.total_HT (float)
        self.TVA (bool)
    """

    def _header(self):
        self._elements.append(Paragraph("<b>FACTURE</b>", CustomStyle.get_style(fontSize=25, leading=25)))
        self._elements.append(Spacer(1, 20))

    def _company_details(self):
        self._elements.append(Paragraph(self.company.name, CustomStyle.left_title))
        self._elements.append(Paragraph(f"{self.company.street}", ))
        self._elements.append(Paragraph(f"{self.company.postcode}, {self.company.city}, {self.company.country}",
                                        CustomStyle.normal))
        self._elements.append(Paragraph(self.company.email, CustomStyle.normal))
        self._elements.append(Paragraph(self.company.phone, CustomStyle.normal))
        self._elements.append(Spacer(1, 4))

    def _client_details(self):
        self._elements.append(Paragraph(self.client.name, CustomStyle.right_title))
        self._elements.append(Paragraph(f"{self.client.street}", CustomStyle.right))
        self._elements.append(Paragraph(f"{self.client.postcode}, {self.client.city}, {self.client.country}",
                                        CustomStyle.right))
        self._elements.append(Paragraph(f"N°SIRET: {self.client.siret}", CustomStyle.right))
        self._elements.append(Paragraph(f"N°TVA: {self.client.tva_number}", CustomStyle.right))
        self._elements.append(Spacer(1, 60))

    def _invoice_details(self):
        self._elements.append(Paragraph(f"<b>Facture n°{self.number}</b>",
                                        CustomStyle.get_style(fontSize=12,leading=16)))
        self._elements.append(Paragraph(f"Date d’émission : {self.invoice_date}", CustomStyle.normal))
        self._elements.append(Paragraph(f"Date limite de paiement : 30 jours à compter de l'émission de la "
                                        f"présente facture",
                                        CustomStyle.normal))
        self._elements.append(Spacer(1, 24))

    def _period(self):
        self._elements.append(Paragraph(f"Période de réalisation de la prestation: "
                                        f"{self.period_month} {self.period_year}", CustomStyle.heading))
        self._elements.append(Spacer(1, 6))

    def _invoice_data(self):

        table_data = [
            ["Description", "Quantité", "Prix unitaire HT (€)", "Total HT (€)"],
            ["Prestation de service en informatique", self.quantity, self.unit_price, f"{self.total_HT:.2f}"]
        ]

        # Table Style
        table = Table(table_data, colWidths=[180, 60, 100, 100], hAlign='CENTER')
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
        ]))
        self._elements.append(table)
        self._elements.append(Spacer(1, 20))
        self._elements.append(Paragraph(f"<b>Sous Total HT (euros):</b> {self.total_HT:.2f}",CustomStyle.right))
        sub_tot = self.quantity*self.unit_price

        if self.TVA:
            tot = sub_tot*1.20
            self._elements.append(Paragraph(f"<b>TVA (20%) (euros):</b> {0.20*sub_tot:.2f}", CustomStyle.right))
        else:
            tot = sub_tot
            self._elements.append(Paragraph("<i>TVA non applicable, art. 293 B du CG </i>", CustomStyle.right))

        self._elements.append(Paragraph(
            f"<b>Total TTC (euros) : {tot:.2f}</b>",
            CustomStyle.get_style(fontSize=12,alignment=TA_RIGHT, spaceBefore=8)))

    # Billing details
    def _billing(self):
        self._elements.append(Spacer(1, 100))
        self._elements.append(Paragraph("<b>Informations de paiements</b>",  CustomStyle.normal))
        self._elements.append(Paragraph(f"<b>IBAN :</b> {self.bank.iban}",  CustomStyle.normal))
        self._elements.append(Paragraph(f"<b>BIC :</b> {self.bank.bic}",  CustomStyle.normal))

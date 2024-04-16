import datetime
import numpy as np
import tkinter as tk
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename
from openpyxl.styles import Color, PatternFill, Font, Border
from openpyxl.styles import colors
from openpyxl import *
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import  Font
from openpyxl.styles import  Color
from openpyxl.styles import Alignment

import pandas as pd

from tkinter import filedialog

from openpyxl.chart import (
	LineChart,
	Series,
	Reference,
)

from openpyxl.cell import Cell
from openpyxl.descriptors import (
	String,
	Sequence,
	Integer,
	)
import base64
import io
import unicodedata
import math

#de avut grija la sume (daca sunt cu , sau . si de schimbat codul la TB IN FUNCTIE DE ASTA)

class MyDict(dict):
	def __missing__(self, key):

		return str(key)
# def normal_round(n, decimals=0):
#     expoN = n * 10 ** decimals
#     if abs(expoN) - abs(math.floor(expoN)) < 0.5:
#         return math.floor(expoN) / 10 ** decimals
#     return math.ceil(expoN) / 10 ** decimals

def normal_round(n, decimals=0):
	expoN = n * 10 ** decimals
	rounded_value = round(expoN) / 10 ** decimals
	if round(n, decimals) != rounded_value:
		# Dacă valoarea rotunjită nu este corectă, scădem 0.01 pentru a corecta
		rounded_value -= 0.01
	return rounded_value

date=datetime.datetime.now().date()
periodStartYear="2024"
periodStart="2"
LEGRAND_TAXFILENUM_Header="RO37623474" 
LEGRAND_TAXFILENUM="0037623474" #PENTRU A COMPLETA CAMPURILE CUSTOMER SAU SUPPLIERID CU DATELE EXPUR ACOLO UNDE E CAZUL-CERINTA ESTE SA FIE FORMAT DIN 00+CUI, fara atribut RO
contactPersonFirstName="MIRELA"
contactPersonLastName="BERECHET"
contactPhone="0213202328"
headerComment="L" #L PT DECL LUNARA, VA TREBUI MODIFICATA DACA AVEM CEVA LA CERERE
IBAN="RO16BACX0000001559318000"
strada = "Str. Dacia 3"
oras = "Oarja"
# codPostal = "000000"
countrySubentity = "RO-AG"
country = "RO"
vatID ="RO37623474" 
numeCompanie = "S.C. BIMED TEKNIK ROMANIA SRL"




Clients=pd.read_excel("D:/Projects/27. Efactura/BIMED/MasterDate Clienti _FBL5N_Customer by tax_AD.XLSX")


newheader=["Tax no 1","Tax no 2","Exmpty1","Empty2", "VAT registration no", "Country","Name", "Customer","Empty3"]
listheader=["Tax Number 1", "Tax No. 2"]

m = [set(listheader).issubset(i) for i in Clients.values.tolist()] #gasire rand pe care se afla headerul
Clients=Clients.iloc[:, 1:10]
index=Clients[m].index.values #salvare index header
print(index[0]+1)
new_header=Clients.iloc[int(index[0])]
Clients.columns=newheader


Clients.drop(Clients.index[:1], inplace=True)
# Clients=Clients[newheader]
Clients.dropna(axis=1, how="all", inplace=True)
Clients["CUI"]=Clients["VAT registration no"].fillna(Clients["Tax no 2"]).fillna(Clients["Tax no 1"])


Clients["Customer"]=Clients["Customer"].astype(str).str.lstrip("0").str.replace(r'\.0$', '', regex=True)
# Clients.loc[Clients["CUI"].astype(str).str.startswith("RO"), "Cty"]="RO"
Clients=Clients.loc[Clients["Country"].astype(str)=="RO"]
dictClients_CUI=Clients.set_index('Customer').to_dict()['CUI']
# dictClients_City=Clients.set_index('Customer').to_dict()['CITY']
dictClients_Country=Clients.set_index('Customer').to_dict()['Country']
# dictClients_Street=Clients.set_index('Customer').to_dict()['FORMATTED_LINE_2']
dictUM={'PAC':'AB','CM2':'CMK','EA':'EA','PC':'H87','KG':'KGM','L':'LTR','M':'MTR','ROL':'XRO',}

Clients.to_excel("D:/Projects/27. Efactura/E-Factura Expeditors/out/Clients.xlsx")


Sales_EFACTURA=pd.read_excel("D:/Projects/27. Efactura/BIMED/Sales invoices _credit note_NA MARTIE 2023-FEB 2024.XLSX")


# Se actualizează moneda pentru liniile cu contul 704 folosind dicționarul creat

Sales_EFACTURA["Reference"]=Sales_EFACTURA["Reference"].astype(str).str.lstrip("0").str.replace(r'\.0$', '', regex=True)

#!!!!!!!!!!
#!!!!!!!!!!
#!!!!!!!!!!
#!!!!!!!!!!
#!!!!!!!!!!




#=================================================DE STERS NEAPARAT===================================================================================
Sales_EFACTURA["STREET_CLIENT"]="str. abc"
Sales_EFACTURA["CITY_CLIENT"]="BUCURESTI"
Sales_EFACTURA["REGION"]="DB"
Sales_EFACTURA["Company"]=Sales_EFACTURA["Name 1"]
#=================================================DE STERS NEAPARAT===================================================================================
















# Sales_EFACTURA=Sales_EFACTURA.loc[~Sales_EFACTURA["GL Cat"].astype(str).str.contains("Currency Adjustment Factor")]
# Sales_EFACTURA.to_excel("D:/Projects/27. Efactura/E-Factura Expeditors/out/RJ GRUPAT.xlsx")
Sales_EFACTURA["Cod Unitate Masura"]=Sales_EFACTURA["Base Unit of Measure"].map(dictUM)
Sales_EFACTURA["Base Unit of Measure"]=Sales_EFACTURA["Base Unit of Measure"].fillna("PC")
Sales_EFACTURA["Cod Unitate Masura"]=Sales_EFACTURA["Cod Unitate Masura"].fillna("H87")
Sales_EFACTURA["CUI_CLIENT"]=Sales_EFACTURA["Customer"].astype(str).str.lstrip("0").str.replace(r'\.0$', '', regex=True).map(dictClients_CUI)
Sales_EFACTURA["COUNTRY_CLIENT"]=Sales_EFACTURA["Customer"].astype(str).str.lstrip("0").str.replace(r'\.0$', '', regex=True).map(dictClients_Country)
Sales_EFACTURA["General ledger amount"]=Sales_EFACTURA["General ledger amount"]*-1
Sales_EFACTURA["Amount in local currency"]=Sales_EFACTURA["Amount in local currency"]*-1
Sales_EFACTURA.to_excel("D:/Projects/27. Efactura/BIMED/out/Sales initial.xlsx")
Sales_EFACTURA=Sales_EFACTURA.loc[Sales_EFACTURA["COUNTRY_CLIENT"]=="RO"]
# Sales_EFACTURA["CITY_CLIENT"]=Sales_EFACTURA["GCI"].str.lstrip("0").str.replace(r'\.0$', '', regex=True).map(dictClients_City)
# Sales_EFACTURA["STREET_CLIENT"]=Sales_EFACTURA["GCI"].str.lstrip("0").str.replace(r'\.0$', '', regex=True).map(dictClients_Street)
dictTaxCode={"A1":"S", 'B0':"AE", 'Y8':'E'}
Sales_EFACTURA["ID TVA"]=Sales_EFACTURA["Tax Code"].map(dictTaxCode)
dictCota={"AE":0, "S":19.00, "E":0 }
Sales_EFACTURA["Valoare linia TVA (Valuta)"]=Sales_EFACTURA["General ledger amount"]*(Sales_EFACTURA["Tax Propotion"]/100)
Sales_EFACTURA["Cota"]=Sales_EFACTURA["Tax Propotion"]
Sales_EFACTURA["Valoare linia TVA"]=Sales_EFACTURA["Amount in local currency"]*(Sales_EFACTURA["Tax Propotion"]/100)
Sales_EFACTURA["Valoare linie cu TVA (Valuta)"]=Sales_EFACTURA["General ledger amount"]+Sales_EFACTURA["Valoare linia TVA (Valuta)"]
Sales_EFACTURA["Valoare linie cu TVA"]=Sales_EFACTURA["Amount in local currency"] + Sales_EFACTURA["Valoare linia TVA"]
total_factura=Sales_EFACTURA.groupby("Reference")["Amount in local currency"].transform('sum')
Sales_EFACTURA["Total Factura"]=total_factura
Sales_EFACTURA['flagInvoiceCreditNote'] = Sales_EFACTURA['Total Factura'] >= 0
Sales_EFACTURA['flagInvoiceCreditNote']=Sales_EFACTURA['flagInvoiceCreditNote'].astype(str).str.replace("True","Invoice")
Sales_EFACTURA['flagInvoiceCreditNote']=Sales_EFACTURA['flagInvoiceCreditNote'].astype(str).str.replace("False","CreditNote")
Sales_EFACTURA.loc[Sales_EFACTURA["flagInvoiceCreditNote"]=="Invoice", 'Inv Type code']=380
Sales_EFACTURA.loc[Sales_EFACTURA["flagInvoiceCreditNote"]=="CreditNote", 'Inv Type code']=381
Sales_EFACTURA["Quantity"]=Sales_EFACTURA["Quantity"].fillna(-1)
Sales_EFACTURA["Quantity"]=Sales_EFACTURA["Quantity"]*(-1)
Sales_EFACTURA.loc[Sales_EFACTURA["Quantity"]==0, 'Quantity']=1
Sales_EFACTURA["Unit Price"]=Sales_EFACTURA["General ledger amount"]/Sales_EFACTURA["Quantity"]
Sales_EFACTURA['Data scadenta'] = Sales_EFACTURA['Document Date'] + pd.Timedelta(days=60)
# Sales_EFACTURA['Amount'] = Sales_EFACTURA.groupby(['Billing Description', 'Reference'])['Amount'].transform('sum').round(2)
# Sales_EFACTURA['General ledger amount'] = Sales_EFACTURA.groupby(['Billing Description', 'Reference'])['General ledger amount'].transform('sum').round(2)

# După ce am calculat suma prețurilor, eliminăm duplicatele

# Sales_EFACTURA = Sales_EFACTURA.drop_duplicates(subset=['Reference', 'Billing Description'])
# Sales_EFACTURA.loc[Sales_EFACTURA["General ledger amount"]!="nan", 'General ledger amount']=Sales_EFACTURA["General ledger amount"]/Sales_EFACTURA["FX Inv"]

# Sales_EFACTURA.loc[Sales_EFACTURA["General ledger currency"]!="nan", "FX"]=Sales_EFACTURA["General ledger amount"]/Sales_EFACTURA["General ledger amount"]
# Sales_EFACTURA['FX'] = Sales_EFACTURA.groupby('Reference')['FX'].transform(lambda x: x.fillna(method='ffill'))
# Sales_EFACTURA['General ledger currency'] = Sales_EFACTURA.groupby('Reference')['General ledger currency'].transform(lambda x: x.fillna(method='ffill'))
# Sales_EFACTURA.loc[Sales_EFACTURA["General ledger amount"].astype(str)=="nan", "General ledger amount" ]=Sales_EFACTURA["General ledger amount"]/Sales_EFACTURA['FX']

listaNumarFact = list(set(list(Sales_EFACTURA["Reference"])))
# listaTipFactura=list(set(list(Sales_EFACTURA["Inv Type code"])))
totalFactura=Sales_EFACTURA["Amount in local currency"].sum()
primaFactura = list(Sales_EFACTURA["Reference"])[0]
ultimaFactura=list(Sales_EFACTURA["Reference"])[-1]
print(totalFactura, primaFactura, ultimaFactura)
print("asta e prima factura in prelucrare_date.py ",primaFactura)
Sales_EFACTURA.to_excel("D:/Projects/27. Efactura/BIMED/out/Sales.xlsx")

issue_date = pd.to_datetime(Sales_EFACTURA["Document Date"]).dt.strftime('%Y-%m-%d').iloc[0]
nrFacturiTrimise = len(listaNumarFact)

for i in range(0, len(listaNumarFact)):
	df_fact_curenta = Sales_EFACTURA.groupby(["Reference"]).get_group(listaNumarFact[i])
	if df_fact_curenta["flagInvoiceCreditNote"].iloc[0]=="Invoice":
#-------------------------------------------------------------------INVOICE IN LEI--------------------------------------------------------------------------------------------------
		issue_date = pd.to_datetime(df_fact_curenta["Document Date"]).dt.strftime('%Y-%m-%d').iloc[0]
		data_scadenta=pd.to_datetime(df_fact_curenta["Data scadenta"]).dt.strftime('%Y-%m-%d').iloc[0]

		if str(df_fact_curenta["General ledger currency"].iloc[0])=="RON":    
			listaCote = list(set(list(df_fact_curenta["Cota"])))
			subtotalTva = df_fact_curenta.groupby("Cota")["Valoare linia TVA"].sum().reset_index()
			subtotalBaza=df_fact_curenta.groupby("Cota")["General ledger amount"].sum().reset_index()
			subtotalIDTVA=df_fact_curenta.groupby("ID TVA")["Cota"].sum().reset_index()
			
			total_amount = 0
			tva_total=0

			XML_Header = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n
			<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"\n xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:ns4="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"\n xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2 http://docs.oasis-open.org/ubl/os-UBL-2.1/xsd/maindoc/UBL-Invoice-2.1.xsd">
			<cbc:CustomizationID>urn:cen.eu:en16931:2017#compliant#urn:efactura.mfinante.ro:CIUS-RO:1.0.1</cbc:CustomizationID>
			<cbc:ID>BMD-{str(df_fact_curenta["Reference"].iloc[0]).replace(".0", "")}</cbc:ID>
			<cbc:IssueDate>{issue_date}</cbc:IssueDate>
			<cbc:DueDate>{data_scadenta}</cbc:DueDate>
			<cbc:InvoiceTypeCode>{str(df_fact_curenta["Inv Type code"].iloc[0]).replace(".0", "")[:299]}</cbc:InvoiceTypeCode>

<cbc:DocumentCurrencyCode>RON</cbc:DocumentCurrencyCode>
<cbc:TaxCurrencyCode>RON</cbc:TaxCurrencyCode>
		   

			'''

			AccountingSupplierParty = '''
			<cac:AccountingSupplierParty>
				<cac:Party>
					<cac:PostalAddress>
						<cbc:StreetName>'''+str(strada)+'''</cbc:StreetName>
						<cbc:CityName>'''+str(oras)+'''</cbc:CityName>
						<cbc:CountrySubentity>'''+str(countrySubentity)+'''</cbc:CountrySubentity>
						<cac:Country>
							<cbc:IdentificationCode>'''+str(country)+'''</cbc:IdentificationCode>
						</cac:Country>
					</cac:PostalAddress>
					<cac:PartyTaxScheme>
						<cbc:CompanyID>'''+str(vatID)+'''</cbc:CompanyID>
						<cac:TaxScheme>
							<cbc:ID>VAT</cbc:ID>
						</cac:TaxScheme>
					</cac:PartyTaxScheme>
					<cac:PartyLegalEntity>
						<cbc:RegistrationName>'''+str(numeCompanie)+'''</cbc:RegistrationName>
						<cbc:CompanyID>'''+str(vatID)+'''</cbc:CompanyID>
					</cac:PartyLegalEntity>
				</cac:Party>
			</cac:AccountingSupplierParty>
			'''
			AccountingCustomerPartyXML=f'''
			<cac:AccountingCustomerParty>
				<cac:Party>
					<cac:PostalAddress>
						<cbc:StreetName>{str(df_fact_curenta["STREET_CLIENT"].iloc[0])}</cbc:StreetName>
						<cbc:CityName>{str(df_fact_curenta["CITY_CLIENT"].iloc[0])}</cbc:CityName>
						<cbc:CountrySubentity>RO-{df_fact_curenta["REGION"].iloc[0]}</cbc:CountrySubentity>
						<cac:Country>
							<cbc:IdentificationCode>{str(df_fact_curenta["COUNTRY_CLIENT"].iloc[0])}</cbc:IdentificationCode>
						</cac:Country>
					</cac:PostalAddress>
					<cac:PartyTaxScheme>
						<cbc:CompanyID>{str(df_fact_curenta["CUI_CLIENT"].iloc[0])}</cbc:CompanyID>
						<cac:TaxScheme>
							<cbc:ID>VAT</cbc:ID>
						</cac:TaxScheme>
					</cac:PartyTaxScheme>
					<cac:PartyLegalEntity>
						<cbc:RegistrationName>{str(df_fact_curenta["Company"].iloc[0])}</cbc:RegistrationName>
						<cbc:CompanyID>{str(df_fact_curenta["CUI_CLIENT"].iloc[0])}</cbc:CompanyID>
					</cac:PartyLegalEntity>
				</cac:Party>
			</cac:AccountingCustomerParty>'''
			# invoiceLine += xml_efactura + AccountingCustomerPartyXML 
			# Variabilă pentru a număra elementele din fiecare factură
			invoiceLine = ""
			line_count = 1
			total_tva=0
			# print(subtotalTva)
			# <cbc:ID>{row["ID TVA"]}</cbc:ID>
			TAXTOTAL="\n<cac:TaxTotal>\n"
			TaxTotal =""
			for index, row in subtotalTva.iterrows():
				taxamount=subtotalTva["Valoare linia TVA"][index].sum()
				taxamounttotal=subtotalTva["Valoare linia TVA"].sum()
				taxamounttotal=normal_round(taxamounttotal, decimals=2)
				baza = subtotalBaza["General ledger amount"][index].sum()
				baza=normal_round(baza, decimals=2)
				taxamount=normal_round(taxamount, decimals=2)

				if str(subtotalIDTVA["ID TVA"][index])=="AE":

					TaxExemptionReasonCode="VATEX-EU-AE"
				if str(subtotalIDTVA["ID TVA"][index])=="E":
					TaxExemptionReasonCode="VATEX-EU-G"
					TaxTotal = TaxTotal+f'''
					
						
						<cac:TaxSubtotal>
							<cbc:TaxableAmount currencyID="RON">{str(round(float(str(baza)),2))}</cbc:TaxableAmount>
							<cbc:TaxAmount currencyID="RON">{str(round(float(str(row["Valoare linia TVA"])),2))}</cbc:TaxAmount>
							<cac:TaxCategory>
								<cbc:ID>{subtotalIDTVA["ID TVA"][index]}</cbc:ID>
								<cbc:Percent>{str(round(float(str(row["Cota"])),2))}</cbc:Percent>
								<cbc:TaxExemptionReasonCode>{TaxExemptionReasonCode}</cbc:TaxExemptionReasonCode>
								<cac:TaxScheme>
									<cbc:ID>VAT</cbc:ID>
								</cac:TaxScheme>
							</cac:TaxCategory>
						</cac:TaxSubtotal>
					\n'''
				else:
		   	 		TaxTotal = TaxTotal + f'''

						<cac:TaxSubtotal>
								<cbc:TaxableAmount currencyID="RON">{str(round(float(str(baza)),2))}</cbc:TaxableAmount>
								<cbc:TaxAmount currencyID="RON">{str(round(float(str(row["Valoare linia TVA"])),2))}</cbc:TaxAmount>
								<cac:TaxCategory>
									<cbc:ID>{subtotalIDTVA["ID TVA"][index]}</cbc:ID>
									<cbc:Percent>{str(round(float(str(row["Cota"])),2))}</cbc:Percent>
									<cac:TaxScheme>
										<cbc:ID>VAT</cbc:ID>
									</cac:TaxScheme>
								</cac:TaxCategory>
						</cac:TaxSubtotal>
					\n'''
					# print("abc")
			TAXTOTAL = TAXTOTAL + '<cbc:TaxAmount currencyID="RON">' + str(round(float(str(taxamounttotal)),2)) +'</cbc:TaxAmount>' + TaxTotal + "\n</cac:TaxTotal>\n"
			for index, row in df_fact_curenta.iterrows():
				line_amount = row["General ledger amount"]
				# line_amount=normal_round(line_amount, decimals=2)
				val_cu_tva = row["Valoare linie cu TVA"]
				tva = row["Valoare linia TVA"]
				# tva = normal_round(tva, decimals=2)
				
				total_tva += val_cu_tva
				tva_total += tva
				total_amount += line_amount
				# total_amount=normal_round(total_amount, decimals=2)
				invoiceLine += f'''<cac:InvoiceLine>
						<cbc:ID>{line_count}</cbc:ID>
						<cbc:InvoicedQuantity unitCode="{row["Cod Unitate Masura"]}">{row["Quantity"]}</cbc:InvoicedQuantity>
						<cbc:LineExtensionAmount currencyID="RON">{str(round(float(str(row["General ledger amount"])),2))}</cbc:LineExtensionAmount>
						<cac:Item>
							<cbc:Name>{row["Material Description"]}</cbc:Name>
							<cac:ClassifiedTaxCategory>
								<cbc:ID>{row["ID TVA"]}</cbc:ID>
								<cbc:Percent>{str(round(float(str(row["Cota"])),2))}</cbc:Percent>
								<cac:TaxScheme>
									<cbc:ID>VAT</cbc:ID>
								</cac:TaxScheme>
							</cac:ClassifiedTaxCategory>
						</cac:Item>
						<cac:Price>
							<cbc:PriceAmount currencyID="RON">{str(abs(round(float(str(row["Unit Price"])),2)))}</cbc:PriceAmount>
						</cac:Price>
					</cac:InvoiceLine>'''
					
				
				
				# Incrementați numărul elementului pentru următoarea linie din factură
				line_count += 1
			total_amount_with_vat = total_amount + tva_total
			# total_amount_with_vat=normal_round(total_amount_with_vat, decimals=2)
			# print(row["Reference"], total_tva)
			# print(str(df_fact_curenta["Reference"].iloc[0]).replace(".0", "") ,total_amount_without_vat)

			PaymentMeans = f'''
			<cac:PaymentMeans>
				<cbc:PaymentMeansCode>10</cbc:PaymentMeansCode>
			</cac:PaymentMeans>'''


			LegalMonetary = f'''
			<cac:LegalMonetaryTotal>
				<cbc:LineExtensionAmount currencyID="RON">{str(round(float(str(total_amount)),2))}</cbc:LineExtensionAmount>
				<cbc:TaxExclusiveAmount currencyID="RON">{str(round(float(str(total_amount)),2))}</cbc:TaxExclusiveAmount>
				<cbc:TaxInclusiveAmount currencyID="RON">{str(round(float(str(total_amount_with_vat)),2))}</cbc:TaxInclusiveAmount>
				<cbc:AllowanceTotalAmount currencyID="RON">0.00</cbc:AllowanceTotalAmount>
				<cbc:ChargeTotalAmount currencyID="RON">0.00</cbc:ChargeTotalAmount>
				<cbc:PrepaidAmount currencyID="RON">0.00</cbc:PrepaidAmount>
				<cbc:PayableRoundingAmount currencyID="RON">0.00</cbc:PayableRoundingAmount>
				<cbc:PayableAmount currencyID="RON">{str(round(float(str(total_amount_with_vat)),2))}</cbc:PayableAmount>
			</cac:LegalMonetaryTotal>'''


			# print(total_amount)
			# eFacturaXML = meta + XML_Header + AccountingSupplierParty + AccountingCustomerPartyXML + " TAX TOTAL " + " LEGAL MONETARY TOOL " + invoiceLine +"</Invoice>"
			# Scrieți fișierul XML pentru fiecare factură în parte
			eFacturaXML = XML_Header + AccountingSupplierParty + AccountingCustomerPartyXML + TAXTOTAL + LegalMonetary + invoiceLine +"\n</Invoice>"
			def remove_diacritics(input_str):
				nfkd_form = unicodedata.normalize('NFKD', input_str)
				return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

			eFacturaXML = remove_diacritics(eFacturaXML)
			eFacturaXML=eFacturaXML.replace("&"," ")

			# Scrie conținutul în fișierul XML
			with open(f"D:/Projects/27. Efactura/BIMED/xml/SalesInvoice_{str(listaNumarFact[i]).replace('.0', '').replace(':', '')}.xml", "w", encoding="utf-8") as f:
				f.write(eFacturaXML)

			print("A PRELUCRAT DATELE")
	#-------------------------------------------------------------------INVOICE IN VALUTA--------------------------------------------------------------------------------------------------
		else:
			df_fact_curenta = Sales_EFACTURA.groupby(["Reference"]).get_group(listaNumarFact[i])
			issue_date = pd.to_datetime(df_fact_curenta["Document Date"]).dt.strftime('%Y-%m-%d').iloc[0]
			data_scadenta=pd.to_datetime(df_fact_curenta["Data scadenta"]).dt.strftime('%Y-%m-%d').iloc[0]

			currency=str(df_fact_curenta["General ledger currency"].iloc[0])
			
			listaCote = list(set(list(df_fact_curenta["Cota"])))
			subtotalTvaLEI=df_fact_curenta.groupby("Cota")["Valoare linia TVA"].sum().reset_index()
			subtotalTva = df_fact_curenta.groupby("Cota")["Valoare linia TVA (Valuta)"].sum().reset_index()
			subtotalBaza=df_fact_curenta.groupby("Cota")["General ledger amount"].sum().reset_index()
			subtotalBazaValuta=df_fact_curenta.groupby("Cota")["General ledger amount"].sum().reset_index()
			subtotalTvaValuta=df_fact_curenta.groupby("Cota")["Valoare linia TVA (Valuta)"].sum().reset_index()
			subtotalIDTVA=df_fact_curenta.groupby("ID TVA")["Cota"].sum().reset_index()
			
			total_amount = 0
			tva_total=0

			XML_Header = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n
			<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"\n xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:ns4="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"\n xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2 http://docs.oasis-open.org/ubl/os-UBL-2.1/xsd/maindoc/UBL-Invoice-2.1.xsd">
			<cbc:CustomizationID>urn:cen.eu:en16931:2017#compliant#urn:efactura.mfinante.ro:CIUS-RO:1.0.1</cbc:CustomizationID>
			<cbc:ID>BMD-{str(df_fact_curenta["Reference"].iloc[0]).replace(".0", "")}</cbc:ID>
			<cbc:IssueDate>{issue_date}</cbc:IssueDate>
			<cbc:DueDate>{data_scadenta}</cbc:DueDate>
			<cbc:InvoiceTypeCode>{str(df_fact_curenta["Inv Type code"].iloc[0]).replace(".0", "")[:299]}</cbc:InvoiceTypeCode>
			<cbc:DocumentCurrencyCode>{str(df_fact_curenta['General ledger currency'].iloc[0])}</cbc:DocumentCurrencyCode>
			<cbc:TaxCurrencyCode>RON</cbc:TaxCurrencyCode>
			'''

			AccountingSupplierParty = '''
			<cac:AccountingSupplierParty>
				<cac:Party>
					<cac:PostalAddress>
						<cbc:StreetName>'''+str(strada)+'''</cbc:StreetName>
						<cbc:CityName>'''+str(oras)+'''</cbc:CityName>
						<cbc:CountrySubentity>'''+str(countrySubentity)+'''</cbc:CountrySubentity>
						<cac:Country>
							<cbc:IdentificationCode>'''+str(country)+'''</cbc:IdentificationCode>
						</cac:Country>
					</cac:PostalAddress>
					<cac:PartyTaxScheme>
						<cbc:CompanyID>'''+str(vatID)+'''</cbc:CompanyID>
						<cac:TaxScheme>
							<cbc:ID>VAT</cbc:ID>
						</cac:TaxScheme>
					</cac:PartyTaxScheme>
					<cac:PartyLegalEntity>
						<cbc:RegistrationName>'''+str(numeCompanie)+'''</cbc:RegistrationName>
						<cbc:CompanyID>'''+str(vatID)+'''</cbc:CompanyID>
					</cac:PartyLegalEntity>
				</cac:Party>
			</cac:AccountingSupplierParty>
			'''
			AccountingCustomerPartyXML=f'''
			<cac:AccountingCustomerParty>
				<cac:Party>
					<cac:PostalAddress>
						<cbc:StreetName>{str(df_fact_curenta["STREET_CLIENT"].iloc[0])}</cbc:StreetName>
						<cbc:CityName>{str(df_fact_curenta["CITY_CLIENT"].iloc[0])}</cbc:CityName>
						<cbc:CountrySubentity>RO-{df_fact_curenta["REGION"].iloc[0]}</cbc:CountrySubentity>
						<cac:Country>
							<cbc:IdentificationCode>{str(df_fact_curenta["COUNTRY_CLIENT"].iloc[0])}</cbc:IdentificationCode>
						</cac:Country>
					</cac:PostalAddress>
					<cac:PartyTaxScheme>
						<cbc:CompanyID>{str(df_fact_curenta["CUI_CLIENT"].iloc[0])}</cbc:CompanyID>
						<cac:TaxScheme>
							<cbc:ID>VAT</cbc:ID>
						</cac:TaxScheme>
					</cac:PartyTaxScheme>
					<cac:PartyLegalEntity>
						<cbc:RegistrationName>{str(df_fact_curenta["Company"].iloc[0])}</cbc:RegistrationName>
						<cbc:CompanyID>{str(df_fact_curenta["CUI_CLIENT"].iloc[0])}</cbc:CompanyID>
					</cac:PartyLegalEntity>
				</cac:Party>
			</cac:AccountingCustomerParty>'''
			# invoiceLine += xml_efactura + AccountingCustomerPartyXML 
			# Variabilă pentru a număra elementele din fiecare factură
			invoiceLine = ""
			line_count = 1
			total_tva=0
			# print(subtotalTva)
			# <cbc:ID>{row["ID TVA"]}</cbc:ID>
			TAXTOTAL="\n<cac:TaxTotal>\n"
			TaxTotal =""
			for index, row in subtotalTva.iterrows():
				taxamount=subtotalTvaValuta["Valoare linia TVA (Valuta)"][index].sum()
				taxamounttotal=subtotalTvaValuta["Valoare linia TVA (Valuta)"].sum()
				taxamounttotalLEI=subtotalTvaLEI["Valoare linia TVA"].sum()
				taxamounttotal=normal_round(taxamounttotal, decimals=2)
				taxamounttotalLEI=normal_round(taxamounttotalLEI, decimals=2)
				bazaV = subtotalBazaValuta["General ledger amount"][index].sum()
				baza= subtotalBaza["General ledger amount"][index].sum()
				baza=normal_round(baza, decimals=2)
				bazaV=normal_round(bazaV, decimals=2)
				taxamount=normal_round(taxamount, decimals=2)

				if str(subtotalIDTVA["ID TVA"][index])=="AE":

					TaxExemptionReasonCode="VATEX-EU-AE"
				if str(subtotalIDTVA["ID TVA"][index])=="E":
					TaxExemptionReasonCode="VATEX-EU-G"
					TaxTotal = TaxTotal+f'''
					
						
						<cac:TaxSubtotal>
							<cbc:TaxableAmount currencyID="{str(currency)}">{str(round(float(str(bazaV)),2))}</cbc:TaxableAmount>
							<cbc:TaxAmount currencyID="{str(currency)}">{str(round(float(str(row["Valoare linia TVA (Valuta)"])),2))}</cbc:TaxAmount>
							<cac:TaxCategory>
								<cbc:ID>{subtotalIDTVA["ID TVA"][index]}</cbc:ID>
								<cbc:Percent>{str(round(float(str(row["Cota"])),2))}</cbc:Percent>
								<cbc:TaxExemptionReasonCode>{TaxExemptionReasonCode}</cbc:TaxExemptionReasonCode>
								<cac:TaxScheme>
									<cbc:ID>VAT</cbc:ID>
								</cac:TaxScheme>
							</cac:TaxCategory>
						</cac:TaxSubtotal>
					\n'''
				else:
		   	 		TaxTotal = TaxTotal + f'''

						<cac:TaxSubtotal>
								<cbc:TaxableAmount currencyID="{str(currency)}">{str(round(float(str(bazaV)),2))}</cbc:TaxableAmount>
								<cbc:TaxAmount currencyID="{str(currency)}">{str(round(float(str(row["Valoare linia TVA (Valuta)"])),2))}</cbc:TaxAmount>
								<cac:TaxCategory>
									<cbc:ID>{subtotalIDTVA["ID TVA"][index]}</cbc:ID>
									<cbc:Percent>{str(round(float(str(row["Cota"])),2))}</cbc:Percent>
									<cac:TaxScheme>
										<cbc:ID>VAT</cbc:ID>
									</cac:TaxScheme>
								</cac:TaxCategory>
						</cac:TaxSubtotal>
					\n'''
					# print("abc")
			TAXTOTAL = TAXTOTAL + '<cbc:TaxAmount currencyID="RON">' + str(round(float(str(taxamounttotalLEI)),2)) +'</cbc:TaxAmount>' + "\n</cac:TaxTotal>\n"+ TAXTOTAL + '<cbc:TaxAmount currencyID="'+str(currency)+'">' + str(round(float(str(taxamounttotal)),2)) +'</cbc:TaxAmount>' + TaxTotal + "\n</cac:TaxTotal>\n"
			for index, row in df_fact_curenta.iterrows():
				line_amount = row["General ledger amount"]
				currency=row["General ledger currency"]
				# line_amount=normal_round(line_amount, decimals=2)
				val_cu_tva = row["Valoare linie cu TVA (Valuta)"]
				tva = row["Valoare linia TVA (Valuta)"]
				# tva = normal_round(tva, decimals=2)
				
				total_tva += val_cu_tva
				tva_total += tva
				total_amount += line_amount
				# total_amount=normal_round(total_amount, decimals=2)
				invoiceLine += f'''<cac:InvoiceLine>
						<cbc:ID>{line_count}</cbc:ID>
						<cbc:InvoicedQuantity unitCode="{row["Cod Unitate Masura"]}">{row["Quantity"]}</cbc:InvoicedQuantity>
						<cbc:LineExtensionAmount currencyID="{str(row["General ledger currency"])}">{str(round(float(str(row["General ledger amount"])),2))}</cbc:LineExtensionAmount>
						<cac:Item>
							<cbc:Name>{row["Material Description"]}</cbc:Name>
							<cac:ClassifiedTaxCategory>
								<cbc:ID>{row["ID TVA"]}</cbc:ID>
								<cbc:Percent>{str(round(float(str(row["Cota"])),2))}</cbc:Percent>
								<cac:TaxScheme>
									<cbc:ID>VAT</cbc:ID>
								</cac:TaxScheme>
							</cac:ClassifiedTaxCategory>
						</cac:Item>
						<cac:Price>
							<cbc:PriceAmount currencyID="{str(row["General ledger currency"])}">{str(abs(round(float(str(row["Unit Price"])),2)))}</cbc:PriceAmount>
						</cac:Price>
					</cac:InvoiceLine>'''
					
				
				
				# Incrementați numărul elementului pentru următoarea linie din factură
				line_count += 1
			total_amount_with_vat = total_amount + tva_total
			# total_amount_with_vat=normal_round(total_amount_with_vat, decimals=2)
			# print(row["Reference"], total_tva)
			# print(str(df_fact_curenta["Reference"].iloc[0]).replace(".0", "") ,total_amount_without_vat)

			PaymentMeans = f'''
			<cac:PaymentMeans>
				<cbc:PaymentMeansCode>10</cbc:PaymentMeansCode>
			</cac:PaymentMeans>'''


			LegalMonetary = f'''
			<cac:LegalMonetaryTotal>
				<cbc:LineExtensionAmount currencyID="{str(currency)}">{str(round(float(str(total_amount)),2))}</cbc:LineExtensionAmount>
				<cbc:TaxExclusiveAmount currencyID="{str(currency)}">{str(round(float(str(total_amount)),2))}</cbc:TaxExclusiveAmount>
				<cbc:TaxInclusiveAmount currencyID="{str(currency)}">{str(round(float(str(total_amount_with_vat)),2))}</cbc:TaxInclusiveAmount>
				<cbc:AllowanceTotalAmount currencyID="{str(currency)}">0.00</cbc:AllowanceTotalAmount>
				<cbc:ChargeTotalAmount currencyID="{str(currency)}">0.00</cbc:ChargeTotalAmount>
				<cbc:PrepaidAmount currencyID="{str(currency)}">0.00</cbc:PrepaidAmount>
				<cbc:PayableRoundingAmount currencyID="{str(currency)}">0.00</cbc:PayableRoundingAmount>
				<cbc:PayableAmount currencyID="{str(currency)}">{str(round(float(str(total_amount_with_vat)),2))}</cbc:PayableAmount>
			</cac:LegalMonetaryTotal>'''


			# print(total_amount)
			# eFacturaXML = meta + XML_Header + AccountingSupplierParty + AccountingCustomerPartyXML + " TAX TOTAL " + " LEGAL MONETARY TOOL " + invoiceLine +"</Invoice>"
			# Scrieți fișierul XML pentru fiecare factură în parte
			eFacturaXML = XML_Header + AccountingSupplierParty + AccountingCustomerPartyXML + TAXTOTAL + LegalMonetary + invoiceLine +"\n</Invoice>"
			def remove_diacritics(input_str):
				nfkd_form = unicodedata.normalize('NFKD', input_str)
				return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

			eFacturaXML = remove_diacritics(eFacturaXML)
			eFacturaXML=eFacturaXML.replace("&"," ")

			# Scrie conținutul în fișierul XML
			with open(f"D:/Projects/27. Efactura/BIMED/xml/SalesInvoiceValuta_{str(listaNumarFact[i]).replace('.0', '').replace(':', '')}.xml", "w", encoding="utf-8") as f:
				f.write(eFacturaXML)

			print("A PRELUCRAT DATELE")
#------------------------------CREDIT NOTE LEI--------------------------------------------------------------------------------------------------------------------------------

	else:
	# else:
		df_fact_curenta = Sales_EFACTURA.groupby(["Reference"]).get_group(listaNumarFact[i])
		issue_date = pd.to_datetime(df_fact_curenta["Document Date"]).dt.strftime('%Y-%m-%d').iloc[0]
		data_scadenta=pd.to_datetime(df_fact_curenta["Data scadenta"]).dt.strftime('%Y-%m-%d').iloc[0]
		if str(df_fact_curenta["General ledger currency"].iloc[0])=="RON":

			listaCote = list(set(list(df_fact_curenta["Cota"])))
			subtotalTva = df_fact_curenta.groupby("Cota")["Valoare linia TVA"].sum().reset_index()
			subtotalBaza=df_fact_curenta.groupby("Cota")["General ledger amount"].sum().reset_index()
			subtotalIDTVA=df_fact_curenta.groupby("ID TVA")["Cota"].sum().reset_index()

			total_amount = 0
			tva_total=0

			XML_Header = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n
			<CreditNote\nxmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" 
		xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
		xmlns="urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2">
		
		<cbc:CustomizationID>urn:cen.eu:en16931:2017#compliant#urn:efactura.mfinante.ro:CIUS-RO:1.0.1</cbc:CustomizationID>
			<cbc:ID>BMD-{str(df_fact_curenta["Reference"].iloc[0]).replace(".0", "")}</cbc:ID>
			<cbc:IssueDate>{issue_date}</cbc:IssueDate>
			
			<cbc:CreditNoteTypeCode>{str(df_fact_curenta["Inv Type code"].iloc[0]).replace(".0", "")}</cbc:CreditNoteTypeCode>
			<cbc:DocumentCurrencyCode>RON</cbc:DocumentCurrencyCode>
			'''

			AccountingSupplierParty = '''
			<cac:AccountingSupplierParty>
				<cac:Party>
					<cac:PostalAddress>
						<cbc:StreetName>'''+str(strada)+'''</cbc:StreetName>
						<cbc:CityName>'''+str(oras)+'''</cbc:CityName>
						<cbc:CountrySubentity>'''+str(countrySubentity)+'''</cbc:CountrySubentity>
						<cac:Country>
							<cbc:IdentificationCode>'''+str(country)+'''</cbc:IdentificationCode>
						</cac:Country>
					</cac:PostalAddress>
					<cac:PartyTaxScheme>
						<cbc:CompanyID>'''+str(vatID)+'''</cbc:CompanyID>
						<cac:TaxScheme>
							<cbc:ID>VAT</cbc:ID>
						</cac:TaxScheme>
					</cac:PartyTaxScheme>
					<cac:PartyLegalEntity>
						<cbc:RegistrationName>'''+str(numeCompanie)+'''</cbc:RegistrationName>
						<cbc:CompanyID>'''+str(vatID)+'''</cbc:CompanyID>
					</cac:PartyLegalEntity>
				</cac:Party>
			</cac:AccountingSupplierParty>
			'''
			AccountingCustomerPartyXML=f'''
			<cac:AccountingCustomerParty>
				<cac:Party>
					<cac:PostalAddress>
						<cbc:StreetName>{str(df_fact_curenta["STREET_CLIENT"].iloc[0])}</cbc:StreetName>
						<cbc:CityName>{str(df_fact_curenta["CITY_CLIENT"].iloc[0])}</cbc:CityName>
						<cbc:CountrySubentity>RO-{df_fact_curenta["REGION"].iloc[0]}</cbc:CountrySubentity>
						<cac:Country>
							<cbc:IdentificationCode>{str(df_fact_curenta["COUNTRY_CLIENT"].iloc[0])}</cbc:IdentificationCode>
						</cac:Country>
					</cac:PostalAddress>
					<cac:PartyTaxScheme>
						<cbc:CompanyID>{str(df_fact_curenta["CUI_CLIENT"].iloc[0])}</cbc:CompanyID>
						<cac:TaxScheme>
							<cbc:ID>VAT</cbc:ID>
						</cac:TaxScheme>
					</cac:PartyTaxScheme>
					<cac:PartyLegalEntity>
						<cbc:RegistrationName>{str(df_fact_curenta["Company"].iloc[0])}</cbc:RegistrationName>
						<cbc:CompanyID>{str(df_fact_curenta["CUI_CLIENT"].iloc[0])}</cbc:CompanyID>
					</cac:PartyLegalEntity>
				</cac:Party>
			</cac:AccountingCustomerParty>'''
			# invoiceLine += xml_efactura + AccountingCustomerPartyXML 
			# Variabilă pentru a număra elementele din fiecare factură
			invoiceLine = ""
			line_count = 1
			total_tva=0

			# print(subtotalTva)
			# <cbc:ID>{row["ID TVA"]}</cbc:ID>
			TAXTOTAL="\n<cac:TaxTotal>\n"
			TaxTotal =""
			for index, row in subtotalTva.iterrows():
				taxamount=subtotalTva["Valoare linia TVA"][index].sum()
				taxamounttotal=subtotalTva["Valoare linia TVA"].sum()
				# taxamounttotal=normal_round(taxamounttotal, decimals=2)
				baza = subtotalBaza["General ledger amount"][index].sum()
				baza=normal_round(baza, decimals=2)
				# taxamount=normal_round(taxamount, decimals=2)
				if str(subtotalIDTVA["ID TVA"][index])=="AE":
					TaxExemptionReasonCode="VATEX-EU-AE"
				if str(subtotalIDTVA["ID TVA"][index])=="E":
					TaxExemptionReasonCode="VATEX-EU-G"
					TaxTotal = TaxTotal+f'''
					
						
						<cac:TaxSubtotal>
							<cbc:TaxableAmount currencyID="RON">{str(round(float(str(baza)),2))}</cbc:TaxableAmount>
							<cbc:TaxAmount currencyID="RON">{str(round(float(str(row["Valoare linia TVA"])),2))}</cbc:TaxAmount>
							<cac:TaxCategory>
								<cbc:ID>{subtotalIDTVA["ID TVA"][index]}</cbc:ID>
								<cbc:Percent>{str(round(float(str(row["Cota"])),2))}</cbc:Percent>
								<cbc:TaxExemptionReasonCode>{TaxExemptionReasonCode}</cbc:TaxExemptionReasonCode>
								<cac:TaxScheme>
									<cbc:ID>VAT</cbc:ID>
								</cac:TaxScheme>
							</cac:TaxCategory>
						</cac:TaxSubtotal>
					\n'''
				
				else:
					TaxTotal = TaxTotal + f'''
					
						
						<cac:TaxSubtotal>
							<cbc:TaxableAmount currencyID="RON">{str(round(float(str(baza)),2))}</cbc:TaxableAmount>
							<cbc:TaxAmount currencyID="RON">{str(round(float(str(row["Valoare linia TVA"])),2))}</cbc:TaxAmount>
							<cac:TaxCategory>
								<cbc:ID>{subtotalIDTVA["ID TVA"][index]}</cbc:ID>
								<cbc:Percent>{str(round(float(str(row["Cota"])),2))}</cbc:Percent>
								<cac:TaxScheme>
									<cbc:ID>VAT</cbc:ID>
								</cac:TaxScheme>
							</cac:TaxCategory>
						</cac:TaxSubtotal>
					\n'''
			TAXTOTAL=TAXTOTAL+'<cbc:TaxAmount currencyID="RON">'+str(round(float(str(taxamounttotal)),2))+'</cbc:TaxAmount>'+TaxTotal+"\n</cac:TaxTotal>\n"

			for index, row in df_fact_curenta.iterrows():
				line_amount = row["General ledger amount"]
				# line_amount=normal_round(line_amount, decimals=2)
				val_cu_tva = row["Valoare linie cu TVA"]
				tva=row["Valoare linia TVA"]
				# tva=normal_round(tva, decimals=2)
				# val_cu_tva=normal_round(val_cu_tva, decimals=2)
				
				total_tva += val_cu_tva
				tva_total+=tva
				total_amount += line_amount
				# total_amount=normal_round(total_amount, decimals=2)
				# tva_total=normal_round(tva_total, decimals=2)

				invoiceLine += f'''<cac:CreditNoteLine>
						<cbc:ID>{line_count}</cbc:ID>
						<cbc:CreditedQuantity unitCode="{row["Cod Unitate Masura"]}">{row["Quantity"]}</cbc:CreditedQuantity>
						<cbc:LineExtensionAmount currencyID="RON">{str(round(float(str(row["General ledger amount"])),2))}</cbc:LineExtensionAmount>
						<cac:Item>
							<cbc:Name>{row["Material Description"]}</cbc:Name>
							<cac:ClassifiedTaxCategory>
								<cbc:ID>{row["ID TVA"]}</cbc:ID>
								<cbc:Percent>{str(round(float(str(row["Cota"])),2))}</cbc:Percent>
								<cac:TaxScheme>
									<cbc:ID>VAT</cbc:ID>
								</cac:TaxScheme>
							</cac:ClassifiedTaxCategory>
						</cac:Item>
						<cac:Price>
							<cbc:PriceAmount currencyID="RON">{str(abs(round(float(str(row["Unit Price"])),2)))}</cbc:PriceAmount>
						</cac:Price>
					</cac:CreditNoteLine>'''

				# Incrementați numărul elementului pentru următoarea linie din factură
				line_count += 1
			total_amount_with_vat =total_amount +tva_total
			# total_amount_with_vat=normal_round(total_amount_with_vat, decimals=2)
			# total_amount_with_vat=normal_round(total_amount_with_vat, decimals=2) 


			PaymentMeans = f'''
			<cac:PaymentMeans>
				<cbc:PaymentMeansCode>10</cbc:PaymentMeansCode>
			</cac:PaymentMeans>'''

			LegalMonetary = f'''
			<cac:LegalMonetaryTotal>
				<cbc:LineExtensionAmount currencyID="RON">{str(round(float(str(total_amount)),2))}</cbc:LineExtensionAmount>
				<cbc:TaxExclusiveAmount currencyID="RON">{str(round(float(str(total_amount)),2))}</cbc:TaxExclusiveAmount>
				<cbc:TaxInclusiveAmount currencyID="RON">{str(round(float(str(total_amount_with_vat)),2))}</cbc:TaxInclusiveAmount>
				<cbc:AllowanceTotalAmount currencyID="RON">0.00</cbc:AllowanceTotalAmount>
				<cbc:ChargeTotalAmount currencyID="RON">0.00</cbc:ChargeTotalAmount>
				<cbc:PrepaidAmount currencyID="RON">0.00</cbc:PrepaidAmount>
				<cbc:PayableRoundingAmount currencyID="RON">0.00</cbc:PayableRoundingAmount>
				<cbc:PayableAmount currencyID="RON">{str(round(float(str(total_amount_with_vat)),2))}</cbc:PayableAmount>
			</cac:LegalMonetaryTotal>'''

			eFacturaXML = XML_Header + AccountingSupplierParty + AccountingCustomerPartyXML + TAXTOTAL + LegalMonetary + invoiceLine +"\n</CreditNote>"
			eFacturaXML=eFacturaXML.replace("&"," ")
			def remove_diacritics(input_str):
				nfkd_form = unicodedata.normalize('NFKD', input_str)
				return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

			eFacturaXML = remove_diacritics(eFacturaXML)

			# Scrie conținutul în fișierul XML
			with open(f"D:/Projects/27. Efactura/BIMED/xml/SalesCreditNote_{str(listaNumarFact[i]).replace('.0', '').replace(':', '')}.xml", "w", encoding="utf-8") as f:
				f.write(eFacturaXML)

			print("A PRELUCRAT DATELE")


#------------------------------CREDIT NOTE VALUTA--------------------------------------------------------------------------------------------------------------------------------
		else:
			df_fact_curenta = Sales_EFACTURA.groupby(["Reference"]).get_group(listaNumarFact[i])
			issue_date = pd.to_datetime(df_fact_curenta["Document Date"]).dt.strftime('%Y-%m-%d').iloc[0]
			data_scadenta=pd.to_datetime(df_fact_curenta["Data scadenta"]).dt.strftime('%Y-%m-%d').iloc[0]
			currency=str(df_fact_curenta["General ledger currency"].iloc[0])
			
			listaCote = list(set(list(df_fact_curenta["Cota"])))
			subtotalTvaLEI=df_fact_curenta.groupby("Cota")["Valoare linia TVA"].sum().reset_index()
			subtotalTva = df_fact_curenta.groupby("Cota")["Valoare linia TVA (Valuta)"].sum().reset_index()
			subtotalBaza=df_fact_curenta.groupby("Cota")["General ledger amount"].sum().reset_index()
			subtotalBazaValuta=df_fact_curenta.groupby("Cota")["General ledger amount"].sum().reset_index()
			subtotalTvaValuta=df_fact_curenta.groupby("Cota")["Valoare linia TVA (Valuta)"].sum().reset_index()
			subtotalIDTVA=df_fact_curenta.groupby("ID TVA")["Cota"].sum().reset_index()
			
			total_amount = 0
			tva_total=0

			XML_Header = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n
			<CreditNote\nxmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" 
		xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
		xmlns="urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2">
		
		<cbc:CustomizationID>urn:cen.eu:en16931:2017#compliant#urn:efactura.mfinante.ro:CIUS-RO:1.0.1</cbc:CustomizationID>
			<cbc:ID>BMD-{str(df_fact_curenta["Reference"].iloc[0]).replace(".0", "")}</cbc:ID>
			<cbc:IssueDate>{issue_date}</cbc:IssueDate>
		  
			<cbc:CreditNoteTypeCode>{str(df_fact_curenta["Inv Type code"].iloc[0]).replace(".0", "")}</cbc:CreditNoteTypeCode>
			<cbc:DocumentCurrencyCode>{str(df_fact_curenta['General ledger currency'].iloc[0])}</cbc:DocumentCurrencyCode>
			<cbc:TaxCurrencyCode>RON</cbc:TaxCurrencyCode>
			'''

			AccountingSupplierParty = '''
			<cac:AccountingSupplierParty>
				<cac:Party>
					<cac:PostalAddress>
						<cbc:StreetName>'''+str(strada)+'''</cbc:StreetName>
						<cbc:CityName>'''+str(oras)+'''</cbc:CityName>
						<cbc:CountrySubentity>'''+str(countrySubentity)+'''</cbc:CountrySubentity>
						<cac:Country>
							<cbc:IdentificationCode>'''+str(country)+'''</cbc:IdentificationCode>
						</cac:Country>
					</cac:PostalAddress>
					<cac:PartyTaxScheme>
						<cbc:CompanyID>'''+str(vatID)+'''</cbc:CompanyID>
						<cac:TaxScheme>
							<cbc:ID>VAT</cbc:ID>
						</cac:TaxScheme>
					</cac:PartyTaxScheme>
					<cac:PartyLegalEntity>
						<cbc:RegistrationName>'''+str(numeCompanie)+'''</cbc:RegistrationName>
						<cbc:CompanyID>'''+str(vatID)+'''</cbc:CompanyID>
					</cac:PartyLegalEntity>
				</cac:Party>
			</cac:AccountingSupplierParty>
			'''
			AccountingCustomerPartyXML=f'''
			<cac:AccountingCustomerParty>
				<cac:Party>
					<cac:PostalAddress>
						<cbc:StreetName>{str(df_fact_curenta["STREET_CLIENT"].iloc[0])}</cbc:StreetName>
						<cbc:CityName>{str(df_fact_curenta["CITY_CLIENT"].iloc[0])}</cbc:CityName>
						<cbc:CountrySubentity>RO-{df_fact_curenta["REGION"].iloc[0]}</cbc:CountrySubentity>
						<cac:Country>
							<cbc:IdentificationCode>{str(df_fact_curenta["COUNTRY_CLIENT"].iloc[0])}</cbc:IdentificationCode>
						</cac:Country>
					</cac:PostalAddress>
					<cac:PartyTaxScheme>
						<cbc:CompanyID>{str(df_fact_curenta["CUI_CLIENT"].iloc[0])}</cbc:CompanyID>
						<cac:TaxScheme>
							<cbc:ID>VAT</cbc:ID>
						</cac:TaxScheme>
					</cac:PartyTaxScheme>
					<cac:PartyLegalEntity>
						<cbc:RegistrationName>{str(df_fact_curenta["Company"].iloc[0])}</cbc:RegistrationName>
						<cbc:CompanyID>{str(df_fact_curenta["CUI_CLIENT"].iloc[0])}</cbc:CompanyID>
					</cac:PartyLegalEntity>
				</cac:Party>
			</cac:AccountingCustomerParty>'''
			# invoiceLine += xml_efactura + AccountingCustomerPartyXML 
			# Variabilă pentru a număra elementele din fiecare factură
			invoiceLine = ""
			line_count = 1
			total_tva=0
			# print(subtotalTva)
			# <cbc:ID>{row["ID TVA"]}</cbc:ID>
			TAXTOTAL="\n<cac:TaxTotal>\n"
			TaxTotal =""
			for index, row in subtotalTva.iterrows():
				taxamount=subtotalTvaValuta["Valoare linia TVA (Valuta)"][index].sum()
				taxamounttotal=subtotalTvaValuta["Valoare linia TVA (Valuta)"].sum()
				taxamounttotalLEI=subtotalTvaLEI["Valoare linia TVA"].sum()
				taxamounttotal=normal_round(taxamounttotal, decimals=2)
				taxamount=normal_round(taxamount, decimals=2)
				taxamounttotalLEI=normal_round(taxamounttotalLEI, decimals=2)
				bazaV = subtotalBazaValuta["General ledger amount"][index].sum()
				baza= subtotalBaza["General ledger amount"][index].sum()
				# baza=normal_round(baza, decimals=2)
				# bazaV=normal_round(bazaV, decimals=2)

				if str(subtotalIDTVA["ID TVA"][index])=="AE":

					TaxExemptionReasonCode="VATEX-EU-AE"
				if str(subtotalIDTVA["ID TVA"][index])=="E":
					TaxExemptionReasonCode="VATEX-EU-G"
					TaxTotal = TaxTotal+f'''
					
						
						<cac:TaxSubtotal>
							<cbc:TaxableAmount currencyID="{str(currency)}">{str(round(float(str(bazaV)),2))}</cbc:TaxableAmount>
							<cbc:TaxAmount currencyID="{str(currency)}">{str(round(float(str(row["Valoare linia TVA (Valuta)"])),2))}</cbc:TaxAmount>
							<cac:TaxCategory>
								<cbc:ID>{subtotalIDTVA["ID TVA"][index]}</cbc:ID>
								<cbc:Percent>{str(round(float(str(row["Cota"])),2))}</cbc:Percent>
								<cbc:TaxExemptionReasonCode>{TaxExemptionReasonCode}</cbc:TaxExemptionReasonCode>
								<cac:TaxScheme>
									<cbc:ID>VAT</cbc:ID>
								</cac:TaxScheme>
							</cac:TaxCategory>
						</cac:TaxSubtotal>
					\n'''
				else:
		   	 		TaxTotal = TaxTotal + f'''

						<cac:TaxSubtotal>
								<cbc:TaxableAmount currencyID="{str(currency)}">{str(round(float(str(bazaV)),2))}</cbc:TaxableAmount>
								<cbc:TaxAmount currencyID="{str(currency)}">{str(round(float(str(row["Valoare linia TVA (Valuta)"])),2))}</cbc:TaxAmount>
								<cac:TaxCategory>
									<cbc:ID>{subtotalIDTVA["ID TVA"][index]}</cbc:ID>
									<cbc:Percent>{str(round(float(str(row["Cota"])),2))}</cbc:Percent>
									<cac:TaxScheme>
										<cbc:ID>VAT</cbc:ID>
									</cac:TaxScheme>
								</cac:TaxCategory>
						</cac:TaxSubtotal>
					\n'''
					# print("abc")
			TAXTOTAL = TAXTOTAL + '<cbc:TaxAmount currencyID="RON">' + str(round(float(str(taxamounttotalLEI)),2)) +'</cbc:TaxAmount>' + "\n</cac:TaxTotal>\n"+ TAXTOTAL + '<cbc:TaxAmount currencyID="'+str(currency)+'">' + str(round(float(str(taxamounttotal)),2)) +'</cbc:TaxAmount>' + TaxTotal + "\n</cac:TaxTotal>\n"
			for index, row in df_fact_curenta.iterrows():
				line_amount = row["General ledger amount"]
				currency=row["General ledger currency"]
				# line_amount=normal_round(line_amount, decimals=2)
				val_cu_tva = row["Valoare linie cu TVA (Valuta)"]
				tva = row["Valoare linia TVA (Valuta)"]
				# tva = normal_round(tva, decimals=2)
				
				total_tva += val_cu_tva
				tva_total += tva
				total_amount += line_amount
				total_tva=normal_round(total_tva, decimals=2)
				# total_amount=normal_round(total_amount, decimals=2)
				invoiceLine += f'''<cac:CreditNoteLine>
						<cbc:ID>{line_count}</cbc:ID>
						<cbc:CreditedQuantity unitCode="{row["Cod Unitate Masura"]}">{row["Quantity"]}</cbc:CreditedQuantity>
						<cbc:LineExtensionAmount currencyID="{str(row["General ledger currency"])}">{str(round(float(str(row["General ledger amount"])),2))}</cbc:LineExtensionAmount>
						<cac:Item>
							<cbc:Name>{row["Material Description"]}</cbc:Name>
							<cac:ClassifiedTaxCategory>
								<cbc:ID>{row["ID TVA"]}</cbc:ID>
								<cbc:Percent>{str(round(float(str(row["Cota"])),2))}</cbc:Percent>
								<cac:TaxScheme>
									<cbc:ID>VAT</cbc:ID>
								</cac:TaxScheme>
							</cac:ClassifiedTaxCategory>
						</cac:Item>
						<cac:Price>
							<cbc:PriceAmount currencyID="{str(row["General ledger currency"])}">{str(abs(round(float(str(row["Unit Price"])),2)))}</cbc:PriceAmount>
						</cac:Price>
					</cac:CreditNoteLine>'''
					
				
				
				# Incrementați numărul elementului pentru următoarea linie din factură
				line_count += 1
			total_amount_with_vat = total_amount + tva_total
			# total_amount_with_vat=normal_round(total_amount_with_vat, decimals=2)
			# print(row["Reference"], total_tva)
			# print(str(df_fact_curenta["Reference"].iloc[0]).replace(".0", "") ,total_amount_without_vat)

			PaymentMeans = f'''
			<cac:PaymentMeans>
				<cbc:PaymentMeansCode>10</cbc:PaymentMeansCode>
			</cac:PaymentMeans>'''


			LegalMonetary = f'''
			<cac:LegalMonetaryTotal>
				<cbc:LineExtensionAmount currencyID="{str(currency)}">{str(round(float(str(total_amount)),2))}</cbc:LineExtensionAmount>
				<cbc:TaxExclusiveAmount currencyID="{str(currency)}">{str(round(float(str(total_amount)),2))}</cbc:TaxExclusiveAmount>
				<cbc:TaxInclusiveAmount currencyID="{str(currency)}">{str(round(float(str(total_amount_with_vat)),2))}</cbc:TaxInclusiveAmount>
				<cbc:AllowanceTotalAmount currencyID="{str(currency)}">0.00</cbc:AllowanceTotalAmount>
				<cbc:ChargeTotalAmount currencyID="{str(currency)}">0.00</cbc:ChargeTotalAmount>
				<cbc:PrepaidAmount currencyID="{str(currency)}">0.00</cbc:PrepaidAmount>
				<cbc:PayableRoundingAmount currencyID="{str(currency)}">0.00</cbc:PayableRoundingAmount>
				<cbc:PayableAmount currencyID="{str(currency)}">{str(round(float(str(total_amount_with_vat)),2))}</cbc:PayableAmount>
			</cac:LegalMonetaryTotal>'''


			# print(total_amount)
			# eFacturaXML = meta + XML_Header + AccountingSupplierParty + AccountingCustomerPartyXML + " TAX TOTAL " + " LEGAL MONETARY TOOL " + invoiceLine +"</Invoice>"
			# Scrieți fișierul XML pentru fiecare factură în parte
			eFacturaXML = XML_Header + AccountingSupplierParty + AccountingCustomerPartyXML + TAXTOTAL + LegalMonetary + invoiceLine +"\n</CreditNote>"
			def remove_diacritics(input_str):
				nfkd_form = unicodedata.normalize('NFKD', input_str)
				return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

			eFacturaXML = remove_diacritics(eFacturaXML)
			eFacturaXML=eFacturaXML.replace("&"," ")

			# Scrie conținutul în fișierul XML
			with open(f"D:/Projects/27. Efactura/BIMED/xml/SalesCreditNoteValuta_{str(listaNumarFact[i]).replace('.0', '').replace(':', '')}.xml", "w", encoding="utf-8") as f:
				f.write(eFacturaXML)

			print("A PRELUCRAT DATELE")
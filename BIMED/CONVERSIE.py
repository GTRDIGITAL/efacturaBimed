import os
import datetime
import time
import requests
import shutil
 
def separare():
    def stergeFisiere(directory_path, file_extension):
            try:
                for filename in os.listdir(directory_path):
                    file_path = os.path.join(directory_path, filename)
                    if filename.endswith(file_extension):
                        os.remove(file_path)
                        print(f"Fisierul {filename} a fost sters.")
            except Exception as e:
                print(f"Eroare la stergerea fișierelor: {str(e)}")
   
    folderCreditNote = 'D:/Projects/27. Efactura/BIMED/folderCreditNote'
    folderInvoice = 'D:/Projects/27. Efactura/BIMED/folderInvoice'
 
    # stergeFisiere('D:/Projects/27. Efactura/BIMED/output conversie', '.xml')
    # stergeFisiere('D:/Projects/27. Efactura/BIMED/output zip api', '.zip')
    stergeFisiere('D:/Projects/27. Efactura/BIMED/output conversie PDF', '.pdf')
    stergeFisiere('D:/Projects/27. Efactura/BIMED/output conversie PDF', '.txt')
    stergeFisiere('D:/Projects/27. Efactura/BIMED/folderCreditNote', '.xml')
    stergeFisiere('D:/Projects/27. Efactura/BIMED/folderInvoice', '.xml')
 
 
 
   
 
    # Crearea directoarelor dacă nu există
    os.makedirs(folderCreditNote, exist_ok=True)
    os.makedirs(folderInvoice, exist_ok=True)
 
    outsPath = 'D:/Projects/27. Efactura/BIMED/xml'
 
    for filename in os.listdir(outsPath):
        if filename.endswith('.xml'):
            file_path = os.path.join(outsPath, filename)
            with open(file_path, 'rb') as file:
                xml_data = file.read()
                if b"CreditNote" in xml_data:
                    output_path = os.path.join(folderCreditNote, filename)
                else:
                    output_path = os.path.join(folderInvoice, filename)
            shutil.move(file_path, output_path)
# separare()
 
 
 
 
def conversieINV():
    print("start time ", datetime.datetime.now())
    output_directory = 'D:/Projects/27. Efactura/BIMED/folderInvoice'
    #--------------------------- CONVERSIE ------------------------------------
    convert = 'https://webservicesp.anaf.ro/prod/FCTEL/rest/transformare/FACT1/DA'
    headerss={"Content-Type": "text/plain"}
    n = 0
    max_attempts = 5  # Numărul maxim de încercări
   
    for filename in os.listdir(output_directory):
       
        attempt = 0  # Inițializează contorul de încercări
        success = False  # Inițializează flag-ul de succes
        while attempt < max_attempts and not success:
            # print("sleep")
            # time.sleep(3)
            if filename.endswith('.xml'):
                xml_file_path = os.path.join(output_directory, filename)
                with open(xml_file_path, 'rb') as xml_file:
                    xml_data = xml_file.read()
                try:
                    response = requests.post(convert, data=xml_data, headers=headerss, timeout=60)
                    filename = filename.replace(".xml", "")
                    if response.status_code == 200:
                        with open(f'D:/Projects/27. Efactura/BIMED/output conversie PDF/{filename}.pdf', 'wb') as file:
                            file.write(response.content)
                            print(f'Fisierul {filename} a fost convertit cu success')
                            success = True  # Marchează procesul ca fiind cu succes
                            n += 1
                            print(n)
                    else:
                        print("Eroare la efectuarea cererii HTTP:", response.status_code)
                        print(response.text)
                except Exception as e:
                    print(f"Eroare la procesarea fișierului {filename}: {e}")
                attempt += 1  # Incrementez numărul de încercări
    print("end time ", datetime.datetime.now())
   
conversieINV()
 
# stocarePDF()
# print('aici facem conversia si stocarea PDF in BD')
 
 
pdf_directory = 'D:/Projects/27. Efactura/BIMED/output conversie PDF'
 
def conversieFCN():
    print('start time', datetime.datetime.now())
    output_directory = 'D:/Projects/27. Efactura/BIMED/folderCreditNote'
    convert = 'https://webservicesp.anaf.ro/prod/FCTEL/rest/transformare/FCN/DA'
    headerss = {"Content-Type": "text/plain"}
    max_attempts = 5  # Numărul maxim de încercări
    n = 0
 
    for filename in os.listdir(output_directory):
        n += 1
        print(n)
        attempt = 0  # Inițializează contorul de încercări
        success = False  # Inițializează flag-ul de succes
        while attempt < max_attempts and not success:
            # print("sleep")
            # time.sleep(3)
            if filename.endswith('.xml'):
                xml_file_path = os.path.join(output_directory, filename)
                with open(xml_file_path, 'rb') as xml_file:
                    xml_data = xml_file.read()
                try:
                    response = requests.post(convert, data=xml_data, headers=headerss, timeout=60)
                    filename = filename.replace(".xml", "")
                    if response.status_code == 200:
                        with open(f'D:/Projects/27. Efactura/BIMED/output conversie PDF/{filename}.pdf', 'wb') as file:
                            file.write(response.content)
                            print(f'Fisierul {filename} a fost convertit cu success')
                            success = True  # Marchează procesul ca fiind cu succes
                    else:
                        print("Eroare la efectuarea cererii HTTP:", response.status_code)
                        print(response.text)
                except Exception as e:
                    print(f"Eroare la procesarea fișierului {filename}: {e}")
                attempt += 1  # Incrementez numărul de încercări
    print('end time', datetime.datetime.now())
 
# conversieFCN()
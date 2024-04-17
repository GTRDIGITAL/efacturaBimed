# import mysql.connector
import datetime
import os
from flask_login import login_required, current_user
from flask import session
import json
import zipfile
import shutil
import time
import pymysql
import requests

def citeste_configurare(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

config = citeste_configurare('config.json')
mysql_config = config['mysql']

# Conectează-te la noua bază de date

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
print(timestamp)
# Creează tabela pentru dict1


listaFactt = []

# def stocareDictionarFacturi(data):
    
#     connection = pymysql.connect(
#         host=mysql_config['host'],
#         user=mysql_config['user'],
#         password=mysql_config['password'],
#         database=mysql_config['database']
#     )

#     cursor = connection.cursor()
    
    
    
#     dictionarFacturi = data
#     data_trimis = datetime.datetime.now()
#     for item in dictionarFacturi["mesaje"]:
#         print(item["Factura"], item["Index"])
#         factura = item["Factura"]
#         index_solicitare = item["Index"]
        
#         user_id = current_user.id
        
        
#         insert_query = "INSERT ignore INTO trimitereFacturi (factura, index_incarcare, data_trimis, user_id) VALUES (%s, %s, %s, %s)"
#         values = (factura, index_solicitare, data_trimis, user_id)

#         cursor.execute(insert_query, values)
#     connection.commit()
#     cursor.close()

def stocareDictionarFacturi(data):
    
    connection = pymysql.connect(
        host=mysql_config['host'],
        user=mysql_config['user'],
        password=mysql_config['password'],
        database=mysql_config['database']
    )

    try:
        cursor = connection.cursor()
        
        dictionarFacturi = data
        data_trimis = datetime.datetime.now()
        for item in dictionarFacturi["mesaje"]:
            print(item["Factura"], item["Index"])
            factura = item["Factura"]
            index_solicitare = item["Index"]
            
            user_id = current_user.id
            
            insert_query = "INSERT ignore INTO trimiterefacturi (factura, index_incarcare, data_trimis, user_id) VALUES (%s, %s, %s, %s)"
            values = (factura, index_solicitare, data_trimis, user_id)

            cursor.execute(insert_query, values)
        connection.commit()
    except Exception as e:
        print(f"Eroare la inserare: {e}")
    finally:
        cursor.close()    
    # mydb.close()

def stocareMesajeAnaf(data):
    
    connection = pymysql.connect(
        host=mysql_config['host'],
        user=mysql_config['user'],
        password=mysql_config['password'],
        database=mysql_config['database']
    )

    cursor = connection.cursor()
    # Adaugă datele în tabela dict2
    dict2 = data
    for item in dict2["mesaje"]:
        data_creare = item["data_creare"]
        cif = item["cif"]
        id_solicitare = str(item["id_solicitare"])
        detalii = item["detalii"]
        tip = item["tip"]
        id_factura = item["id"]
 
        insert_query = "INSERT IGNORE INTO statusMesaje (data_creare, cif, id_solicitare, detalii, tip, id_factura) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (data_creare, cif, id_solicitare, detalii, tip, id_factura)
 
        cursor.execute(insert_query, values)
        
 
    connection.commit()
    
 
    # Interogare pentru a citi din nou datele actualizate
    select_query = "SELECT * FROM statusMesaje"
    cursor.execute(select_query)
    updated_results = cursor.fetchall()
    print("updated results ", updated_results)
    cursor.close()


def interogareTabela():
    connection = pymysql.connect(
        host=mysql_config['host'],
        user=mysql_config['user'],
        password=mysql_config['password'],
        database=mysql_config['database']
    )
    cursor = connection.cursor()
    
    selectQuery = "SELECT distinct * FROM JOINDATE WHERE tip IN('ERORI FACTURA', 'FACTURA TRIMISA')"
    cursor.execute(selectQuery)

    results = []

    for row in cursor.fetchall():
        if 'ERORI' in row[5]:
            descarcata = 'Nu'
        else:
            descarcata = row[8]
        
        result_dict = {
            "factura": row[0],
            "data_creare": row[1],
            "cif": row[2],
            "id_solicitare": row[3],
            "detalii": row[4],
            "tip": row[5],
            "id_factura": row[6],
            "user_id": row[7],
            "descarcata": descarcata  
        }
        results.append(result_dict)
    cursor.close()

    return results


def interogareTabelaPrimite():
    
    connection = pymysql.connect(
        host=mysql_config['host'],
        user=mysql_config['user'],
        password=mysql_config['password'],
        database=mysql_config['database']
    )
    cursor = connection.cursor()
    
    selectQuery = "SELECT distinct * FROM JOINDATE WHERE tip ='FACTURA PRIMITA'"
    cursor.execute(selectQuery)

    results = []

    for row in cursor.fetchall():
        result_dict = {
            "factura": row[0],
            "data_creare": row[1],
            "cif": row[2],
            "id_solicitare": row[3],
            "detalii": row[4],
            "tip": row[5],
            "id_factura": row[6],
            "user_id": row[7],
            "descarcata": row[8]
        }
        results.append(result_dict)
        # print(results)
    cursor.close()
    
    return results

def numarFacturiTrimise():
    connection = pymysql.connect(
        host=mysql_config['host'],
        user=mysql_config['user'],
        password=mysql_config['password'],
        database=mysql_config['database']
    )
    cursor = connection.cursor()
    
    numarFact = "SELECT COUNT(*) AS numar_facturi FROM trimiterefacturi GROUP BY data_trimis HAVING COUNT(*) > 1 ORDER BY data_trimis DESC limit 1"
    cursor.execute(numarFact)
    resultNrFact = cursor.fetchall()
    resultNrFactList = [row[0] for row in resultNrFact]
    cursor.close()
    
    return resultNrFactList

nrFactTrimise = numarFacturiTrimise()
print("NUMARUL DE FACTURI TRIMISE ", nrFactTrimise)

def nrFacturiIstoric():
    
    connection = pymysql.connect(
        host=mysql_config['host'],
        user=mysql_config['user'],
        password=mysql_config['password'],
        database=mysql_config['database']
    )
    cursor = connection.cursor()
    
    numarFacturiTrimiseIstoric =  "select count(*) from trimiterefacturi"
    cursor.execute(numarFacturiTrimiseIstoric)
    resultIstoric = cursor.fetchall()
    cursor.close()
    
    return resultIstoric

# print(nrFacturiIstoric())
    

def listaFacturi(data):
    
    connection = pymysql.connect(
        host=mysql_config['host'],
        user=mysql_config['user'],
        password=mysql_config['password'],
        database=mysql_config['database']
    )
    cursor = connection.cursor()
    
    selectQueryFacturi = f"SELECT index_incarcare FROM trimiterefacturi order by data_trimis desc limit {data}"
    cursor.execute(selectQueryFacturi)

    result = cursor.fetchall()
    result_list = [row[0] for row in result]
    
    cursor.close()

    return result_list

for i in nrFactTrimise:
    listaFactt=listaFacturi(i)
print("asta e listaaaa ",listaFactt)
print("aici e numaruuuul ", len(listaFactt))
# print(aba)

def stocarePDF():
    
    connection = pymysql.connect(
        host=mysql_config['host'],
        user=mysql_config['user'],
        password=mysql_config['password'],
        database=mysql_config['database']
    )
    cursor = connection.cursor()
    
    # director_fisiere = "C:/Dezvoltare/E-Factura/2023/eFactura/Bimed/eFacturaBimed/output conversie PDF/"
    director_fisiere = '/home/efactura/efactura_bimed/outputConversie/'

# Parcurgerea fișierelor din director și inserarea în baza de date
    for nume_fisier in os.listdir(director_fisiere):
        if nume_fisier.endswith('.xml'):
            cale_absoluta = os.path.join(director_fisiere, nume_fisier)
            
            with open(cale_absoluta, 'rb') as file:
                pdf_content = file.read()
            nume_fisier=nume_fisier.replace(".xml", "")
            
            

            insert_query = "INSERT INTO FisierePDF (nume_fisier, continut, data_introducere) VALUES (%s, %s, %s)"
            values = (nume_fisier, pdf_content, timestamp)
            cursor.execute(insert_query, values)
    connection.commit()
    cursor.close()


# def descarcarepdf(idSelectate):
    
#     connection = pymysql.connect(
#         host=mysql_config['host'],
#         user=mysql_config['user'],
#         password=mysql_config['password'],
#         database=mysql_config['database']
#     )
#     cursor = connection.cursor() 
    
#     print(idSelectate, 'ASTEA AICI SUNT IN STOCARE.PY')
#     downlPDFbaza = 'C:/Dezvoltare/E-Factura/2023/eFactura/Bimed/eFacturaBimed/download pdf baza de date'
#     destinatie = "C:/Dezvoltare/E-Factura/2023/eFactura/Bimed/eFacturaBimed/destinatie/"
#     # downlPDFbaza = '/home/efactura/efactura_bimed/downloadPdfBazaDate'
#     # destinatie = '/home/efactura/efactura_bimed/destinatie/'
#     idSelectate=idSelectate[1:]

#     stringID=""
#     for i in range(0, len(idSelectate)):
#         if i == len(idSelectate)-1:
#             stringID=stringID + str(idSelectate[i])
#         else:
#             stringID=stringID + str(idSelectate[i]) +  ','
#     print(stringID, ' STRINGID')
    
#     def stergeFisiere(directory_path, file_extension):
#         try:
#             for filename in os.listdir(directory_path):
#                 file_path = os.path.join(directory_path, filename)
#                 if filename.endswith(file_extension):
#                     os.remove(file_path)
#                     print(f"Fisierul {filename} a fost sters.")
#         except Exception as e:
#             print(f"Eroare la stergerea fișierelor: {str(e)}")

#     stergeFisiere(downlPDFbaza, '.pdf')
    
#     def make_archive(source, destination):
#         base = os.path.basename(destination)
#         name = base.split('.')[0]
#         format = base.split('.')[1]
#         archive_from = os.path.dirname(source)
#         archive_to = os.path.basename(source.strip(os.sep))
#         shutil.make_archive(name, format, archive_from, archive_to)
#         shutil.move('%s.%s'%(name,format), destination)

#     try:
#         query = "SELECT nume_fisier, continut FROM tabelaFisierepdf WHERE nume_fisier IN ("+str(stringID)+")"
#         print(query)
#         cursor.execute(query)
#         for (nume_fisier, continut) in cursor:
#             cale_fisier = os.path.join(downlPDFbaza, str(nume_fisier) + '.pdf')

#             with open(cale_fisier, 'wb') as file:
#                 file.write(continut)
#         # make_archive(downlPDFbaza, 'C:/Dezvoltare/E-Factura/2023/eFactura/Ferro/eFacturaFerro/destinatie/'+'rezultat.zip')
#         sqlSafeUpdates="set sql_safe_updates = 0"
#         cursor.execute(sqlSafeUpdates)
#         update_query = "UPDATE trimiterefacturi SET descarcata = 'Da' WHERE index_incarcare IN (" + stringID + ")"
#         print(update_query, '-------------------------------------')
#         cursor.execute(update_query)
#         make_archive(downlPDFbaza, destinatie + 'rezultat.zip')
        
#     except:
#         print("nu are valori")

#     cursor.close()


def descarcarepdf(idSelectate):
    
    connection = pymysql.connect(
        host=mysql_config['host'],
        user=mysql_config['user'],
        password=mysql_config['password'],
        database=mysql_config['database']
    )
    cursor = connection.cursor() 
    
    print(idSelectate, 'ASTEA AICI SUNT IN STOCARE.PY')
    # downlXMLbaza = 'C:/Dezvoltare/E-Factura/2023/eFactura/Bimed/eFacturaBimed/download pdf baza de date'
    # destinatie = "C:/Dezvoltare/E-Factura/2023/eFactura/Bimed/eFacturaBimed/destinatie/"
    downlXMLbaza = '/home/efactura/efactura_bimed/downloadPdfBazaDate'
    destinatie = '/home/efactura/efactura_bimed/destinatie/'
    idSelectate=idSelectate[1:]

    stringID=""
    for i in range(0, len(idSelectate)):
        if i == len(idSelectate)-1:
            stringID=stringID + str(idSelectate[i])
        else:
            stringID=stringID + str(idSelectate[i]) +  ','
    print(stringID, ' STRINGID')
    file_extension =('.pdf', '.xml')
    def stergeFisiere(directory_path, file_extension):
        
        try:
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                if filename.endswith(file_extension):
                    os.remove(file_path)
                    print(f"Fisierul {filename} a fost sters.")
        except Exception as e:
            print(f"Eroare la stergerea fișierelor: {str(e)}")

    stergeFisiere(downlXMLbaza, file_extension)
    
    def make_archive(source, destination):
        base = os.path.basename(destination)
        name = base.split('.')[0]
        format = base.split('.')[1]
        archive_from = os.path.dirname(source)
        archive_to = os.path.basename(source.strip(os.sep))
        shutil.make_archive(name, format, archive_from, archive_to)
        shutil.move('%s.%s'%(name,format), destination)

    try:
        query = "SELECT nume_fisier, continut FROM tabelaFisierepdf WHERE nume_fisier IN ("+str(stringID)+")"
        print(query)
        cursor.execute(query)
        for (nume_fisier, continut) in cursor:
            cale_fisier = os.path.join(downlXMLbaza, str(nume_fisier) + '.xml')

            with open(cale_fisier, 'wb') as file:
                file.write(continut)


        def conversie():
                # xmlANAF = 'C:/Dezvoltare/E-Factura/2023/eFactura/Expeditors/eFacturaExpeditors local/output conversie'
                # cale_fisier = 'C:/Dezvoltare/E-Factura/2023/eFactura/Bimed/eFacturaBimed/download pdf baza de date'
                cale_fisier = '/home/efactura/efactura_bimed/downloadPdfBazaDate'
                headerss = {"Content-Type": "text/plain"}

                # Creează un nou workbook Excel
                # workbook = Workbook()
                # sheet = workbook.active
                # sheet.title = 'Excepții'

                # Adaugă un antet pentru coloana INDEX_INCARCARE
                # sheet['A1'] = 'INDEX_INCARCARE'

                for filename in os.listdir(cale_fisier):
                    try:
                        if filename.endswith('.xml'):
                            xml_file_path = os.path.join(cale_fisier, filename)

                            with open(xml_file_path, 'rb') as xml_file:
                                xml_data = xml_file.read()

                            if 'CreditNote' in str(xml_data):
                                convert = 'https://webservicesp.anaf.ro/prod/FCTEL/rest/transformare/FCN/DA'
                            else:
                                convert = 'https://webservicesp.anaf.ro/prod/FCTEL/rest/transformare/FACT1/DA'

                            start_time = time.time()  # Momentul de start al procesării
        
                            response = None  # Inițializăm răspunsul cu None
                            max_retry_time = 16  # Numărul maxim de secunde pentru a efectua încercările
                            retry_interval = 3  # Intervalul de timp între încercări
                            
                            # Loop până când obținem un răspuns sau până când timpul maxim a fost depășit
                            while response is None and time.time() - start_time < max_retry_time:
                                try:
                                    response = requests.post(convert, data=xml_data, headers=headerss, timeout=30)
                                    # print(response.text)
                                except requests.exceptions.Timeout:
                                    # Dacă întâlnim un timeout, continuăm loop-ul și încercăm din nou
                                    pass
                                
                                # yield "\r\n"
        
                            # Așteaptă intervalul de timp specificat între încercări
                            time.sleep(retry_interval)

                            if response and response.status_code == 200:
                                filename_no_extension = os.path.splitext(filename)[0]
                                # with open(f'C:/Dezvoltare/E-Factura/2023/eFactura/Bimed/eFacturaBimed/download pdf baza de date/{filename_no_extension}.pdf', 'wb') as file:
                                with open(f'/home/efactura/efactura_bimed/downloadPdfBazaDate/{filename_no_extension}.pdf', 'wb') as file:
                                    # file.write(response.content)
                                    print(f'Fisierul {filename} a fost convertit cu succes')
                            else:
                                print("Eroare la efectuarea cererii HTTP:", response.status_code)
                                print(response.text)

                            # Adaugă numele fișierului în coloana INDEX_INCARCARE
                            # sheet.append([filename_no_extension])
                    except Exception as e:
                        print("A apărut o excepție la", filename, ":", str(e))
                        # Adaugă numele fișierului în coloana INDEX_INCARCARE pentru a înregistra excepția
                        # sheet.append([filename])
                # Salvează workbook-ul Excel
                # workbook.save('C:/Dezvoltare/E-Factura/2023/eFactura/Expeditors/eFacturaExpeditors local/output conversie PDF/excepții.xlsx')

            
        conversie()
        # time.sleep(5)

        print('aici facem conversia in PDF')        
        # make_archive(downlPDFbaza, 'C:\\Dezvoltare\\E-Factura\\2023\\eFactura\\Ferro\\eFacturaFerro\\destinatie\\'+'rezultat.zip')
        sqlSafeUpdates="set sql_safe_updates = 0"
        cursor.execute(sqlSafeUpdates)
        update_query = "UPDATE trimiterefacturi SET descarcata = 'Da' WHERE index_incarcare IN (" + stringID + ")"
        print(update_query, '-------------------------------------')
        cursor.execute(update_query)
        make_archive(downlXMLbaza, destinatie + 'rezultat.zip')
        
    except:
        print("nu are valori")

    cursor.close()


    
def interogareTabelaClienti():
    
    connection = pymysql.connect(
        host=mysql_config['host'],
        user=mysql_config['user'],
        password=mysql_config['password'],
        database=mysql_config['database']
    )
    cursor = connection.cursor()
    
    resultsclienti=[]
    # selectQuery = "SELECT * FROM CLIENTS where country in ('RO', 'România')"
    selectQuery = "SELECT * FROM CLIENTS where country not in ('RO', 'România')"
    cursor.execute(selectQuery)
 
    resultsclienti = []
 
    for row in cursor.fetchall():
        result_dict = {
            "id":row[0],
            "name": row[1],
            "country": row[2],
            "cust": row[3],
            "regno": row[4],
            "city": row[5],
            "street": row[6],
            "region": row[8],
        }
        resultsclienti.append(result_dict)
        
        cursor.close()
        # print(resultsclienti)
 
    return resultsclienti


def interogareTabelaClienti10():
    
    connection = pymysql.connect(
        host=mysql_config['host'],
        user=mysql_config['user'],
        password=mysql_config['password'],
        database=mysql_config['database']
    )
    cursor = connection.cursor()
    
    resultsclienti=[]
    # selectQuery = "SELECT * FROM CLIENTS where country in ('RO', 'România')"
    selectQuery = "SELECT * FROM CLIENTS where country not in ('RO', 'România')"
    cursor.execute(selectQuery)
 
    resultsclienti = []
 
    for row in cursor.fetchall():
        result_dict = {
            "id":row[0],
            "name": row[1],
            "country": row[2],
            "cust": row[3],
            "regno": row[4],
            "city": row[5],
            "street": row[6],
            "region": row[8],
        }
        resultsclienti.append(result_dict)
        # print(resultsclienti)
        cursor.close()
 
    return resultsclienti
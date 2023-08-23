from bs4 import BeautifulSoup


def htmlInsert(
            obj_list:list,
            classe_toFind:str,
            file_path='./front/main.html',
            html_tag_content='div class="photo"><img src="{img_path}" alt="Imagem 3"'
        ):
    """ Inserts new img tags to show the images within the obj_list """

    try:
        # Loading html
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Creating a BeautifulSoup object
        soup = BeautifulSoup(html_content, 'html.parser')

        # Looping through the images and loading it to the div string object
        element_to_modify = soup.find(class_=classe_toFind)

        for img in obj_list:

            # print(f"Image indexed: {img}")

            new_div = soup.new_tag(
                    html_tag_content.format(img_path=img)
                )
             
            # print(f"div to be inserted: {new_div}")
            
            element_to_modify.append(new_div)

            break
            # finding an existent tag too insert the new content searching it by the class

        with open(file_path, 'w') as file:
            file.write(str(soup))
            
    except NotImplementedError as ne:
        print("Error in htmlMng: ", str(ne), "\n")
        return False
    else:
        return True
    
def get_pages_list(url:str):
    """ Get all pages from an html table and returns a list of links """
    import requests

    # url = "URL_DA_PAGINA_AQUI"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", class_="wikitable")
    rows = table.select("tr")[1:]  # Seleciona todas as <tr> excluindo o cabeçalho
    link_text = []

    for row in rows:
        first_cell = row.select_one("td:nth-of-type(1)")
        link = first_cell.find("a")
        if link:
            link_text.append(link.get("href"))  # ou qualquer outra informação que você deseje extrair
            # print(link_text)

    return link_text

def table_list(ext_table_keys:object, call_table_links:object):
    """ Receives an object with lists of names and link that will be used to download the html tables
      in each link and trough it to an object/dictionary """
    import pandas as pd

    ext_tables={}

    # print([i for i in zip ( ext_table_keys, call_table_links )])
    # print(f"Len_Names: {len(ext_table_keys)} || Len_call: {len(call_table_links)} \ntable: {ext_table_keys} \nLinks: {call_table_links}")
    # return 0
    len_tb_keys = len(ext_table_keys)
    len_tb_links = len(call_table_links)

    # Checks if the lists are equal and if not, trimms the end of the biggest one for the later used zip() to work
    if len_tb_keys != len_tb_links:
        diference = abs( len_tb_keys - len_tb_links )

        if len_tb_keys > len_tb_links:
            ext_table_keys = ext_table_keys[:-diference]

        raise ValueError("Lists don't have the same length!")
    print(ext_table_keys, call_table_links)

    # for title, link in zip( ext_table_keys, call_table_links ):
    #     try :
    #         if pd.isnull(title) or pd.isnull(link):
    #             raise ValueError("Null or empty values occured")
            
    #         # print(f"title: {title}\nlink: {link}")
    #         # df = pd.read_html(link)[0]
    #         print(title)
    #         # ext_tables[title]=df

    #     except Exception as e:
    #         raise ValueError('Erro ao ler tabela',e,'\n','Tabelas não encontradas.')
        
    # return ext_tables

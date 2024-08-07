from bs4 import BeautifulSoup
from time import sleep
from pandas import DataFrame
from async_processing import process_links_async

def htmlInsert( 
            obj_list:list,
            classe_toFind:str,
            file_path='./front/main.html',
            html_tag_content='div class="photo"><img src="{img_path}" alt="Imagem 3"'
         ):
    """
    Insere uma lista de objetos em um arquivo HTML

    Returns:
        _type_: _description_
    """    

    try:
        # Loading html
        with open( file_path, 'r', encoding='utf-8' ) as file:
            html_content = file.read(  )

        # Creating a BeautifulSoup object
        soup = BeautifulSoup( html_content, 'html.parser' )

        # Looping through the images and loading it to the div string object
        element_to_modify = soup.find( class_=classe_toFind )

        for img in obj_list:

            # print( f"Image indexed: {img}" )

            new_div = soup.new_tag( 
                    html_tag_content.format( img_path=img )
                 )
             
            # print( f"div to be inserted: {new_div}" )
            
            element_to_modify.append( new_div )

            break
            # finding an existent tag too insert the new content searching it by the class

        with open( file_path, 'w' ) as file:
            file.write( str( soup ) )
            
    except NotImplementedError as ne:
        print( "Error in htmlMng: ", str( ne ), "\n" )
        return False
    else:
        return True
    
def get_pages_list( url:str ):
    '''
    Returns all tables in the given page of a website
    Args:
        url ( string ): url of the web page
    '''
    import requests

    # url = "URL_DA_PAGINA_AQUI"
    response = requests.get( url )
    soup = BeautifulSoup( response.content, "html.parser" )

    # Seleciona todas as <tr> excluindo o cabeçalho pela classe certa
    table = soup.find( "table", class_="wikitable" )
    if table == None:
        rows = soup.find("table", class_="fandom-table").select( "tr" )[1:]
    else:
        rows = table.select( "tr" )[1:]  
    
    link_text = []

    for row in rows:
        first_cell = row.select_one( "td:nth-of-type( 1 )" )
        link = first_cell.find( "a" )
        if link:
            link_text.append( link.get( "href" ) )  # ou qualquer outra informação que você deseje extrair
            # print( link_text )

    return link_text

def table_list( ext_table_keys:DataFrame, call_table_links:DataFrame ):
    """
    Returns a list of dictionaries containing data from each table on the webpage
    Args:
    ext_table_keys : dataFrame that contains keys to extract from each table
    call_table_links : dataFrame of urls where the tables are located
    """
    # import pandas as pd

    ext_tables={}

    
    len_tb_keys = len( ext_table_keys )
    len_tb_links = len( call_table_links )
    
    # print(f"len_tb_links {len_tb_links} | len_tb_keys {len_tb_keys}")

    # import pdb; pdb.set_trace()

    # Checks if the lists are equal and if not, trimms the end of the biggest one for the later used zip(  ) to work
    if len_tb_keys != len_tb_links:

        if len_tb_keys > len_tb_links:
            diference = abs(  len_tb_keys - len_tb_links  )
            ext_table_keys = ext_table_keys[:-diference]

        raise ValueError( "Lists don't have the same length!" )

    car_names_list = ext_table_keys.values.tolist()
    call_table_links_list = call_table_links.values.tolist()

    results = process_links_async(call_table_links_list, car_names_list)

    for car_name, table in results:
        ext_tables[car_name] = table

        
    return ext_tables



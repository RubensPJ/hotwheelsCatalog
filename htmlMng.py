from bs4 import BeautifulSoup


def htmlInsert(
            obj_list:list,
            classe_toFind:str,
            file_path='./front/main.html',
            html_tag_content='<div class="photo"><img src="{img_path}" alt="Imagem 3"></div>'
        ):

    try:
        # Loading html
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Creating a BeautifulSoup object
        soup = BeautifulSoup(html_content, 'html.parser')

        # Looping through the images and loading it to the div string object
        element_to_modify = soup.find(class_=classe_toFind)

        for img in obj_list:
            new_div = soup.new_tag(
                    html_tag_content.format(img_path=img)
                )
            
            element_to_modify.append(new_div)
            # finding an existent tag too insert the new content searching it by the class
        

        # # Removing example
        # for p_tag in soup.find_all('p'):
        #     p_tag.decompose()

        # Saving at the original place
        with open(file_path, 'w') as file:
            file.write(str(soup))
            
    except NotImplementedError as ne:
        print("Error in htmlMng:", str(ne), "\n")
        return False
    else:
        return True
    

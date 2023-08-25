import re

class URLProcessor:
    def remove_scale_param(self, url):
        new_url = re.sub(r'/scale-to-width-down/\d+', '', url)
        return new_url
    
    def only_image_urls(self, url):
        new_url = re.sub(r'https://static.wikia.nocookie\.net/hotwheels/images/([^"]+)')
        return new_url
    
'''
### USE CASE EXAMPLE ###

from url_filter import URLProcessor

# Instanciar a classe
url_processor = URLProcessor()

# Exemplo de URL
url = "https://static.wikia.nocookie.net/hotwheels/images/8/8b/Cod60.jpg/revision/latest/scale-to-width-down/75?cb=20081031024712"

# Chamar o método para remover o parâmetro
new_url = url_processor.remove_scale_param(url)

# Imprimir a nova URL
print(new_url)
'''
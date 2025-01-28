from dotenv import load_dotenv
load_dotenv()
import requests
from langchain.docstore.document import Document
from assistant.vector_store import init_chroma_vector_store
import json
from apis.shopify import Shopify
from bs4 import BeautifulSoup
import html2text
from langgraph.checkpoint.postgres import PostgresSaver
from time import sleep
from langchain_community.document_loaders import PyPDFLoader
from apis.shopify import Shopify
from app.models.Order import Order
from app.models.db_pool import pool

with pool.connection() as conn:
    checkpointer = PostgresSaver(conn)
    checkpointer.setup()

all_docs = []
models = ['cliff', 'steel', 'drop', 'hive', 'air', 'kip', 'virta']
for model in models:
    pdf_path = f"./data/manuals/{model}.pdf"
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    for doc in docs:
        doc.id = f"{model}_{doc.metadata['page']}"
        doc.metadata['source'] = f"{model}.pdf" 
    all_docs += docs

print(len(all_docs))
print("manuals initialized")
init_chroma_vector_store(all_docs, filename='manuals')

ignored_brands = ['prosaunas', 'delta', 'thermory', 'hotass']
shopify = Shopify()
p_data = shopify.products()
products = []
for product in p_data:
    for variant in product['variants']['edges']:
        title = variant['node']['displayName'].replace('- Default Title', '')
        price = variant['node']['price']
        sku = variant['node']['sku']
        handle = product['handle']
        resource = 'product'
        products.append({
                         'id': variant['node']['id'].split('/')[-1],
                         'resource': resource,
                         'title': title,
                         'price': price,
                         'sku': sku if sku is not None else 'placeholder',
                         'type': product['productType'],
                         'handle': handle})

for product in products:
    product['url'] = 'https://thesaunaheater.com/products/' + product['handle']
products = [p for p in products if not any(brand in p['title'].lower() for brand in ignored_brands)]


metadata_docs = [Document(page_content=json.dumps(p), metadata=p, id=p['id']) for p in products]
product_metadata_store = init_chroma_vector_store(metadata_docs, filename="products_metadata")

print("metadata store initialized")
used_urls, md_pages = [], []

def remove_with_class(soup, elem, cls):
    for div in soup.find_all(elem, class_=cls):
        div.decompose()
    return soup
    
def remove_duplicates(soup, elem, cls):
    for div in soup.find_all(elem, class_=cls)[1:]:
        div.decompose()
    return soup
    
def remove_sections_with_text(soup, target_text):
    for section in soup.find_all(True):  # Find all tags
        if section.find(string=lambda s: s and target_text.lower() in s.lower()):
            section.decompose()  # Remove the entire section if text is found
    return soup
    
for i, product in enumerate(products, 1):
    url = product['url']
    if all(brand not in url.lower() for brand in ignored_brands) and url not in used_urls:
        used_urls.append(url)
        response = requests.get(url)
        html_content = response.content
        
        soup = BeautifulSoup(html_content, "html.parser")
        
        main_content = soup.find('main')
        
        if main_content:
            for img in main_content.find_all('img'):
                img.decompose() 
            for svg in main_content.find_all('svg'):
                svg.decompose() 
           
            main_content = remove_sections_with_text(main_content, 'customer highlights')

            main_content = remove_with_class(main_content, 'div', 'qb__button-container-start')
            main_content = remove_with_class(main_content, 'div', 'jdgm-carousel-wrapper')
            main_content = remove_with_class(main_content, 'div', 'product-stock-level-wrapper')
            main_content = remove_duplicates(main_content, 'div', 'acc__modal')

            markdown_converter = html2text.HTML2Text()
            markdown_converter.ignore_links = True 
            markdown_content = markdown_converter.handle(main_content.prettify())
            if not 'page not found' in markdown_content.lower():
                md_pages.append({'content': markdown_content, 'id': product['id']})
            sleep(0.5) 
    if i % 100 == 0:
        print(f"{i} / {len(products)} fetched")

documents = [Document(page_content=m['content'], metadata={'id': m['id']}, id=m['id']) for m in md_pages]
page_store = init_chroma_vector_store(documents, filename="products")

shopify = Shopify()
orders = shopify.orders(1000)
for order in orders:
    if order['customer']['email']:
        Order.delete(order['id'].split('/')[-1])
        Order.create(order['id'].split('/')[-1], order['customer']['displayName'], order['name'], order['customer']['email'].lower(), json.dumps(order['events']))
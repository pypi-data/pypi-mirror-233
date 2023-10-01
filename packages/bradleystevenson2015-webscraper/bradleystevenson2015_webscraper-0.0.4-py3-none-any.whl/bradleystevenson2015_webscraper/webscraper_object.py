from bradleystevenson2015_database import database
import json
from .common_webscraper_functions import fetch_soup_from_page
from .parser import CreateFromPageParserFactory, ParserObjectFactory

class WebscraperObjectCollection:

    def __init__(self, webscraper_schema_filepath, database_path, database_schema_filepath, custom_objects):
        self.databaseObject = database.Database(database_path, database_schema_filepath)
        self._create_webscraper_objects(webscraper_schema_filepath, custom_objects)


    def _create_webscraper_objects(self, webscraper_schema_filepath, custom_objects):
        self.webscrapers = []
        file = open(webscraper_schema_filepath)
        data = json.load(file)
        file.close()
        for webscraper_object in data['objects']:
            self.webscrapers.append(WebscraperObjectFactory(webscraper_object, custom_objects).webscraper)


    def run(self, arguments):
        for webscraper in self.webscrapers:
            if webscraper.object_name in arguments:
                webscraper.create_from_web(self.databaseObject)
            else:
                webscraper.create_from_database(self.databaseObject)
        self.databaseObject.insert_into_database()


class WebscraperObject:

    def __init__(self, object_name, tables, create_from_page_parser=None):
        self.object_name = object_name
        self.tables = tables
        self.create_from_page_parser = create_from_page_parser

    def create(self, databaseObject, create_from_web):
        if create_from_web:
            self.create_from_web(self)
        else:
            self.create_from_database(self)

    def create_from_web(self, webscraperObjectCollection):
        pass

    def create_from_database(self, webscraperObjectCollection):
        for table_name in self.tables:
            webscraperObjectCollection.databaseObject.tables[table_name].generate_from_database()

    def create_from_page(self, url, webscraperObjectCollection):
        if self.create_from_page_parser is None:
            raise Exception("We have no way to create this object")
        data_dict = self.create_from_page_parser.parse(url)
        return webscraperObjectCollection.databaseObject.tables[self.tables[0]].append(data_dict)
    

class WebscraperMultiplePageObject(WebscraperObject):

    def __init__(self, object_name, table, base_url, iterator_table_name, parsers):
        self.base_url = base_url
        self.parsers = parsers
        self.table_name = table
        self.iterator_table_name = iterator_table_name
        super().__init__(object_name, [table])

    def create_from_web(self, webscraperObjectCollection):
        for data_dict in webscraperObjectCollection.databaseObject.tables[self.iterator_table_name].data:
            soup = fetch_soup_from_page(self.base_url + data_dict['url'])
            print(self.base_url + data_dict['url'])
            for parser in self.parsers:
                data = parser.parse_page(soup, data_dict, webscraperObjectCollection.databaseObject)
                for data_dict in data:
                    webscraperObjectCollection.databaseObject.tables[self.table_name].append(data_dict)

class WebscraperStaticPageObject(WebscraperObject):

    def __init__(self, object_name, table, urls, parsers):
        self.urls = urls
        self.parsers = parsers
        self.table_name = table
        super().__init__(object_name, [table])

    def create_from_web(self, webscraperObjectCollection):
        for url in self.urls:
            soup = fetch_soup_from_page(url)
            for parser in self.parsers:
                data = parser.parse_page(soup, {}, webscraperObjectCollection.databaseObject)
                for data_dict in data:
                    webscraperObjectCollection.databaseObject.tables[self.table_name].append(data_dict)

class WebscraperObjectFactory:

    def __init__(self, webscraper_object_dict, custom_objects):
        self.webscrapper_object_dict = webscraper_object_dict
        self.create_from_page_parser = None
        if 'create_from_page_parser' in webscraper_object_dict.keys():
            self.create_from_page_parser =  CreateFromPageParserFactory(webscraper_object_dict['create_from_page_parser']).create_from_page_parser
        if webscraper_object_dict['object_type'] == 'single_page':
            parsers = []
            for parser_dict in self.webscrapper_object_dict['parsers']:
                parsers.append(ParserObjectFactory(parser_dict).parser)
            self.webscraper = WebscraperStaticPageObject(webscraper_object_dict['object_name'], webscraper_object_dict['tables'][0], webscraper_object_dict['urls'], parsers)
        elif webscraper_object_dict['object_type'] == 'multiple_page':
            parsers = []
            for parser_dict in self.webscrapper_object_dict['parsers']:
                parsers.append(ParserObjectFactory(parser_dict).parser)
            self.webscraper = WebscraperMultiplePageObject(webscraper_object_dict['object_name'], webscraper_object_dict['tables'][0], webscraper_object_dict['base_url'], webscraper_object_dict['iterator_table_name'], parsers)
        elif webscraper_object_dict['object_type'] == 'custom_object':
            for custom_object in custom_objects:
                if custom_object.object_name == webscraper_object_dict['object_name']:
                    self.webscraper = custom_object
        else:
            raise Exception("No match for object type")
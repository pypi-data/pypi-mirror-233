from .common_webscraper_functions import fetch_soup_from_page, row_has_link, get_tr_of_stats_table, get_tr_of_table_with_id, get_text_of_element_with_attributes, get_url_of_element_with_attributes, does_html_object_exist, static_value, get_text_of_element_with_type


class CreateFromPageParserFactory:

    def __init__(self, create_from_page_parser_dict) -> None:
        self.create_from_page_parser = CreateFromPageParser(create_from_page_parser_dict['base_url'], DataDictParserFactory(create_from_page_parser_dict['parser']).data_dict_parser)


class CreateFromPageParser:

    def __init__(self, base_url, data_dict_parser) -> None:
        self.base_url = base_url
        self.data_dict_parser = data_dict_parser

    def parse(self, url, webscraperObjectCollection):
        soup = fetch_soup_from_page(self.base_url + url)
        data_dict = self.data_dict_parser.parse(soup, {}, webscraperObjectCollection)
        data_dict['url'] = url
        return data_dict

class TableParserObject:

    def __init__(self, all_object_selection_function, narrow_down_function, data_dict_parser):
        self.all_object_selection_function = all_object_selection_function
        self.narrow_down_function = narrow_down_function
        self.data_dict_parser = data_dict_parser

    def parse_page(self, soup, data_dict, webscraperObjectCollection):
        return_array = []
        for eligible_element in self.all_object_selection_function(soup):
            if self.narrow_down_function(eligible_element):
                return_array.append(self.data_dict_parser.parse(eligible_element, data_dict, webscraperObjectCollection))
        return return_array

class ParserObjectFactory:

    def _get_narrow_down_function(self, function_name):
        if function_name == 'row_has_link':
            return row_has_link
        else:
            raise Exception("No match for narrow down function")


    def __init__(self, parser_dict):
        self.parser_dict = parser_dict
        if parser_dict['parser_type'] == 'table':
            if 'table_id' in parser_dict.keys():
                self.parser = TableParserObject(get_tr_of_table_with_id(parser_dict['table_id']), self._get_narrow_down_function(parser_dict['narrow_down_function']), DataDictParserFactory(parser_dict['data_dict_parser']).data_dict_parser)
            else:
                self.parser = TableParserObject(get_tr_of_stats_table(), self._get_narrow_down_function(parser_dict['narrow_down_function']), DataDictParserFactory(parser_dict['data_dict_parser']).data_dict_parser)
        else:
            raise Exception("No match for parser type")


class DataDictParserFactory:

    def __init__(self, data_dict_parser_dict):
        return_dict = {}
        dict_values = {}
        object_urls = []
        object_urls_create_if_not_exist = []
        for field_dict in data_dict_parser_dict:
            if field_dict['parse_type'] == 'input_dict':
                dict_values[field_dict['field_name']] = field_dict['dict_key']
            elif field_dict['parse_type'] == 'url_of_object':
                object_urls.append(field_dict)
            elif field_dict['parse_type'] == 'url_of_object_create_if_not_exist':
                object_urls_create_if_not_exist.append(field_dict)
            else:
                return_dict[field_dict['field_name']] = FunctionParserFactory(field_dict).function
        self.data_dict_parser = DataDictParser(return_dict, dict_values, object_urls, object_urls_create_if_not_exist)

class DataDictParser:

    def __init__(self, function_dict, dict_values, object_urls, object_urls_create_if_not_exist):
        self.function_dict = function_dict
        self.dict_values = dict_values
        self.object_urls = object_urls
        self.object_urls_create_if_not_exist = object_urls_create_if_not_exist

    def parse(self, html_object, data_dict, webscraperObject):
        return_dict = {}
        for key in self.function_dict:
            return_dict[key] = self.function_dict[key](html_object)
        for key in self.dict_values:
            return_dict[key] = data_dict[self.dict_values[key]]
        for object_url in self.object_urls:
            return_dict[object_url['field_name']] = webscraperObject.databaseObject.tables[object_url['object_name']].get_primary_key_by_search_dict({'url': get_url_of_element_with_attributes(object_url['attributes'])(html_object)})
        for object_url in self.object_urls_create_if_not_exist:
            try:
                return_dict[object_url['field_name']] = webscraperObject.databaseObject.tables[object_url['object_name']].get_primary_key_by_search_dict({'url': get_url_of_element_with_attributes(object_url['attributes'])(html_object)})
            except Exception:
                return_dict[object_url['field_name']] = webscraperObject.get_webscraper_object_with_name(object_url['object_name']).create_from_page(get_url_of_element_with_attributes(object_url['attributes'])(html_object), webscraperObject)
        return return_dict


class FunctionParserFactory:

    def _get_function(self, function_name, attributes, field_dict):
        if function_name == 'get_text_of_element_with_attributes':
            if 'remove_strings' in field_dict.keys():
                return get_text_of_element_with_attributes(attributes, field_dict['remove_strings'])
            return get_text_of_element_with_attributes(attributes)
        elif function_name == 'get_url_of_element_with_attributes':
            return get_url_of_element_with_attributes(attributes)
        elif function_name == 'does_html_object_exist':
            return does_html_object_exist(attributes, field_dict['html_object'])
        elif function_name == 'get_text_of_element_with_type':
            return get_text_of_element_with_type(field_dict['element_type'])
        else:
            raise Exception("No match for function " + function_name)

    def __init__(self, field_dict):
        if field_dict['parse_type'] == 'dynamic':
            self.function = self._get_function(field_dict['function_name'], field_dict['attributes'], field_dict)
        elif field_dict['parse_type'] == 'static':
            self.function = static_value(field_dict['static_value'])
        else:
            raise Exception("No match for function parse_type")
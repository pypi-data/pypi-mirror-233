"""Module for XML collections of items."""

import os
import pandas as pd
from lxml import etree
import xmlcoll.base as xb


class Item(xb.Properties):
    """A class for storing and retrieving data about a data item.

    Args:
        ``properties`` (:obj:`dict`, optional): A dictionary of properties.

    """

    def __init__(self, name, properties=None):
        super().__init__()
        self.properties = {}
        self.name = name
        if properties:
            self.update_properties(properties)

    def get_name(self):
        """Method to retrieve name of item.

        Return:
            :obj:`str`: The name of the item.

        """

        return self.name


class Collection(xb.Properties):
    """A class for storing and retrieving data about data items.

    Args:
        ``items`` (:obj:`list`, optional): A list of individual
        :obj:`xmlcoll.coll.Item` objects.

    """

    def __init__(self, items=None):
        super().__init__()
        self.properties = {}
        self.collection = {}
        if items:
            for item in items:
                self.collection[item.get_name()] = item

    def add_item(self, item):
        """Method to add a item to a collection.

        Args:
            ``item`` (:obj:`xmlcoll.coll.Item`) The item to be added.

        Return:
            On successful return, the item has been added.

        """

        self.collection[item.get_name()] = item

    def remove_item(self, item):
        """Method to remove an item from a item collection.

        Args:
            ``item`` (:obj:`xmlcoll.coll.Item`) The item to be removed.

        Return:
            On successful return, the item has been removed.

        """

        self.collection.pop(item.get_name())

    def get(self):
        """Method to retrieve the item collection as a dictionary.

        Returns:
            :obj:`dict`: A dictionary of the items.

        """

        return self.collection

    def get_dataframe(self, index_label="name", tag_delimiter="_"):
        """Method to retrieve the collection data as a pandas dataframe.

        Args:
            ``index_label`` (:obj:`str`, optional): Index label for the
            dataframe.

            ``tag_delimiter`` (:obj:`str`, optional): Delimiter used
            to separate tags in combined column names.


        Returns:
            :obj:`pandas.DataFrame`: A pandas dataframe containing the
            collection data.  Columns are labeled by a string formed by
            concatenating property names and tags separated by the chosen
            delimiter.

        """
        result = pd.DataFrame()
        items = self.collection
        for key, val in items.items():
            data_line = {}
            props = val.get_properties()
            for prop in props:
                my_str = str()
                if isinstance(prop, tuple):
                    for i, my_prop in enumerate(prop):
                        my_str += my_prop
                        if i < len(prop) - 1:
                            my_str += tag_delimiter.strip()
                else:
                    my_str = prop
                data_line[my_str] = [props[prop]]

            df_add = pd.DataFrame(data_line, index=[key])
            df_add.index.name = index_label

            result = pd.concat([result, df_add])

        return result

    def update_from_dataframe(
        self, data_frame, index_label="name", tag_delimiter="_"
    ):
        """Method to update collection data from a pandas dataframe.

        Args:
            ``data_frame`` (:obj:`pandas.DataFrame`): The pandas dataframe.

            ``index_label`` (:obj:`str`, optional): Index label for the
            data frame.

            ``tag_delimiter`` (:obj:`str`, optional): Delimiter used
            to separate tags in combined column names.


        Returns:
            On successful return, the collection has been updated with
            the data in the data frame.

        """
        column_names = list(data_frame.columns.values)
        data_frame = data_frame.reset_index()
        my_cols = list(set(column_names) - set((index_label, "index")))

        for _index, row in data_frame.iterrows():
            item = Item(row[index_label])
            props = {}
            for col in my_cols:
                if not pd.isna(row[col]):
                    result = col.split(tag_delimiter)
                    if len(result) == 1:
                        c_str = result[0]
                    else:
                        c_str = (result[0],)
                        for i in range(1, len(result)):
                            c_str = c_str + (result[i],)
                    props[c_str] = row[col]
            item.update_properties(props)
            self.add_item(item)

    def write_to_xml(self, file, pretty_print=True):
        """Method to write the collection to XML.

        Args:
            ``file`` (:obj:`str`) The output file name.

            ``pretty_print`` (:obj:`bool`, optional): If set to True,
            routine outputs the xml in nice indented format.

        Return:
            On successful return, the item collection data have been
            written to the XML output file.

        """

        root = etree.Element("collection")
        xml = etree.ElementTree(root)

        self._add_properties(root, self)

        my_coll = self.get()

        items = etree.SubElement(root, "items")

        for val in my_coll.values():

            my_item = etree.SubElement(items, "item")

            my_name = etree.SubElement(my_item, "name")

            my_name.text = val.get_name()

            self._add_properties(my_item, val)

        xml.write(file, pretty_print=pretty_print)

    def _add_properties(self, my_element, my_object):
        my_props = my_object.get_properties()

        if len(my_props):
            props = etree.SubElement(my_element, "properties")
            for prop in my_props:
                if isinstance(prop, str):
                    my_prop = etree.SubElement(props, "property", name=prop)
                elif isinstance(prop, tuple):
                    my_prop = etree.SubElement(props, "property", name=prop[0])
                    for i in range(1, len(prop)):
                        my_tag = "tag" + str(i)
                        my_prop.attrib[my_tag] = prop[i]

                my_prop.text = str(my_props[prop])

    def update_from_xml(self, file, xpath=""):
        """Method to update a item collection from an XML file.

        Args:
            ``file`` (:obj:`str`) The name of the XML file from which to
             update.

            ``xpath`` (:obj:`str`, optional): XPath expression to select
            items.  Defaults to all items.

        Returns:
            On successful return, the item collection has been updated.

        """

        parser = etree.XMLParser(remove_blank_text=True)
        xml = etree.parse(file, parser)
        xml.xinclude()

        coll = xml.getroot()

        self._update_properties(coll, self)

        el_item = coll.xpath("//item" + xpath)

        for result in el_item:
            name = result.xpath(".//name")
            my_item = Item(name[0].text)
            self._update_properties(result, my_item)

            self.add_item(my_item)

    def _update_properties(self, my_element, my_object):
        el_props = my_element.xpath("properties")

        if len(el_props) > 0:
            props = el_props[0].xpath("property")

            my_props = {}
            for prop in props:
                attributes = prop.attrib
                my_keys = attributes.keys()
                if len(my_keys) == 1:
                    my_props[attributes[my_keys[0]]] = prop.text
                else:
                    tup = ()
                    for key in my_keys:
                        tup += (attributes[key],)
                    my_props[tup] = prop.text

            my_object.update_properties(my_props)

    def validate(self, file):
        """Method to validate a collection XML file.

        Args:
            ``file`` (:obj:`str`) The name of the XML file to validate.

        Returns:
            An error message if invalid and nothing if valid.

        """

        parser = etree.XMLParser(remove_blank_text=True)
        xml = etree.parse(file, parser)
        xml.xinclude()

        schema_file = os.path.join(
            os.path.dirname(__file__), "xsd_pub/xmlcoll.xsd"
        )
        xmlschema_doc = etree.parse(schema_file)

        xml_validator = etree.XMLSchema(xmlschema_doc)
        xml_validator.validate(xml)

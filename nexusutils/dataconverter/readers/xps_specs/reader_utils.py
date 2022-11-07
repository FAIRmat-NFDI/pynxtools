# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Generic Classes for reading xml file into python dictionary.
"""

import xml.etree.ElementTree as EmtT
import numpy as np
from typing import Tuple


class XmlSpecs(object):
    """
        Class for restructuring xml data file from
        specs vendor into python dictionary.
    """

    def __init__(self,
                 root_element: EmtT.Element,
                 vendor_name: str = "specs") -> None:
        """Collect mandatory inputs.

        Parameters
        ----------
        root_element : Root element xml XPS data file
        vendor_name :  Name of vendor of XPS machine
        """

        self._root_element = root_element

        self._root_path = f'/ENTRY[entry]/{vendor_name}'
        self.py_dict = dict()
        self.tail_part_frm_seq = ""
        self.tail_part_frm_struct = ""
        self.tail_part_frm_othr = ""


    def parse_xml(self) :
        """Start parsing process

        Parameters
        ----------
        """

        element = self._root_element
        child_num = len(element)
        parent_path = self._root_path
        skip_child = -1

        child_elmt_ind = 0
        while child_num > 0:
            self.pass_element_through_parsers(element,
                                              parent_path,
                                              child_elmt_ind,
                                              skip_child)
            child_num -= 1
            child_elmt_ind += 1
        print("Debug: print from : .................................................")

    def pass_element_through_parsers(self,
                                     element_: EmtT,
                                     parent_path: str,
                                     child_elmt_ind: int,
                                     skip_child: int) -> None:
        """
        Parse the element to parser according to element tag.
        Parameters
        ----------
        element_ : xml element to parse
        parent_path : Xpath of the parent element where the element_ belongs
        child_elmt_ind : Index of child element to track the children.
        skip_child : Tack the children who will be skipped to pass to
                     the parser
        Returns
        -------
        None
        """
        print("##################################")

        name_val_elmt_tag = ['ulong',
                             'double',
                             'string',
                             'boolean',
                             'enum',
                             'any']

        parent_element = element_

        element = parent_element[child_elmt_ind]
        element.attrib['__parent__'] = parent_element
        elmt_attr = element.attrib
        elmt_tag = element.tag

        if child_elmt_ind <= skip_child:
            pass

        # elif elmt_tag == "sequence" and \
        #        "ScanSeq" in elmt_attr.values():

        #    data_name, data = self.cumulate_counts_series(element)
        #    self.py_dict[f'{parent_path}/{data_name}'] = data

        elif elmt_tag == "sequence":
            # TODO: Debug here delete
            #if elmt_attr['name'] == "detectors":
                #print("................")
                #x = 100

            self.parse_sequence(element,
                                parent_path)

        elif elmt_tag == "struct":
            self.parse_struct(element,
                              parent_path)

        elif elmt_tag in name_val_elmt_tag:
            self.last_element_parser(element,
                                     parent_path)

        else:
            print("Needs to parse to different element tag parser")

    def parse_sequence(self,
                       element_: EmtT.Element,
                       parent_path: str) -> None:
        """
        Parameters
        ----------
        element_ : Element with sequence tag
        parent_path : Xpath of the parent element where the element_ belongs

        Returns
        -------
        None
        """

        child_num = len(element_)
        elmt_attr = element_.attrib
        elmt_tag = element_.tag
        skip_child = -1

        section_nm_reslvr = ""

        key_name = "name"
        if key_name in elmt_attr.keys():
            section_nm_reslvr = f'{elmt_attr[key_name]}'
            parent_path, self.tail_part_frm_seq = \
                self.check_last_part_repetition(parent_path,
                                                self.tail_part_frm_seq,
                                                section_nm_reslvr)

            # parent_path = f'{parent_path}/{section_nm_reslvr}'

        child_elmt_ind = 0
        while child_num > 0:

            self.pass_element_through_parsers(element_,
                                              parent_path,
                                              child_elmt_ind,
                                              skip_child)

            child_num -= 1
            child_elmt_ind += 1

    def parse_struct(self, 
                     element_: EmtT.Element,
                     parent_path: str) -> None:
        """

        Parameters
        ----------
        element_ : Element with struct tag
        parent_path : Xpath of the parent element where the element_ belongs

        Returns
        -------
        None
        """

        units = ["mV", "deg", "W", "kV", "ns"]
        # TODO add add a parser for a string for string

        child_num = len(element_)
        elmt_tag = element_.tag
        elmt_attr = element_.attrib

        # Resolving struct name section is here
        skip_child = -1
        section_nm_reslvr = ""
        parent_element = elmt_attr['__parent__']
        parent_attr = parent_element.attrib
        first_child = element_[0]
        second_child = element_[1]

        key_name = "name"
        key_value = "value"
        key_type_name = 'type_name'
        if key_name in elmt_attr.keys():
            section_nm_reslvr = elmt_attr[key_name]
            parent_path, self.tail_part_frm_struct = \
                self.check_last_part_repetition(parent_path,
                                                self.tail_part_frm_struct,
                                                section_nm_reslvr)

            # parent_path = f'{parent_path}/{section_nm_reslvr}'

        elif key_name not in elmt_attr.keys():

            if key_name in first_child.attrib.values() and \
                    key_value in second_child.attrib.values():

                section_nm_reslvr = self.restructure_value(
                                               first_child.text,
                                               first_child.tag)

                skip_child += 1
                # Separating the units
                for unit in units:

                    if f'_[{unit}]' in section_nm_reslvr:
                        # TODO: think section_nm_reslvr have a few parts and take the last part as unit
                        section_nm_reslvr, _ = section_nm_reslvr.split('_')
                        self.py_dict[f'{parent_path}/'
                                     f'{section_nm_reslvr}@unit'] = unit

                parent_path, self.tail_part_frm_struct = \
                    self.check_last_part_repetition(parent_path,
                                                    self.tail_part_frm_struct,
                                                    section_nm_reslvr)
                # parent_path = f'{parent_path}/{section_nm_reslvr}'

            elif key_name in first_child.attrib.values() and \
                    first_child.tag == "string":

                skip_child += 1
                child_txt = self.restructure_value(first_child.text,
                                                   first_child.tag)

                section_nm_reslvr = f'{elmt_attr[key_type_name]}_{child_txt}'

                parent_path, self.tail_part_frm_struct = \
                    self.check_last_part_repetition(parent_path,
                                                    self.tail_part_frm_struct,
                                                    section_nm_reslvr)
                # parent_path = f'{parent_path}/{section_nm_reslvr}'

            else:
                section_nm_reslvr = self.restructure_value(elmt_attr[key_type_name], "string")
                parent_path, self.tail_part_frm_struct = \
                    self.check_last_part_repetition(parent_path,
                                                    self.tail_part_frm_struct,
                                                    section_nm_reslvr)

        else:
            parent_path, self.tail_part_frm_struct = \
                self.check_last_part_repetition(parent_path,
                                                self.tail_part_frm_struct,
                                                section_nm_reslvr)
            # parent_path = f'{parent_path}{section_nm_reslvr}'

        child_elmt_ind = 0
        while child_num > 0:
            self.pass_element_through_parsers(element_,
                                              parent_path,
                                              child_elmt_ind,
                                              skip_child)
            child_num -= 1
            child_elmt_ind += 1

    def last_element_parser(self,
                            element_: EmtT.Element,
                            parent_path: str) -> None:
        """

        Parameters
        ----------
        element_ : Element with a tag among 'ulong', 'double', 'string',
                   'boolean', 'enum', 'any'
        parent_path : Xpath of the parent element where the element_ belongs

        Returns
        -------
        None
        """

        child_num = len(element_)
        elmt_attr = element_.attrib
        section_nm_reslvr = ""
        if child_num == 0:
            if "name" in elmt_attr.keys():
                section_nm_reslvr = f'{elmt_attr["name"]}'
                value = self.restructure_value(element_.text,
                                               element_.tag)

                parent_path, self.tail_part_frm_othr = \
                    self.check_last_part_repetition(parent_path,
                                                    self.tail_part_frm_othr,
                                                    section_nm_reslvr)
                self.py_dict[f'{parent_path}'] = value
            else:
                self.py_dict[f'{parent_path}'] \
                    = self.restructure_value(element_.text,
                                             element_.tag)
        elif child_num == 1 \
                and 'any' == element_.tag:
            child_elmt = element_[0]
            self.py_dict[f'{parent_path}'] \
                = self.restructure_value(child_elmt.text,
                                         child_elmt.tag)

    def check_last_part_repetition(self,
                                   parent_path: str,
                                   pre_tail_part: str,
                                   new_tail_part: str) -> Tuple[str, str]:
        """
         Check for the data from the same group, for example repetition of the
         experiments under the same physical circumstances, make number of
         them with ..._1, ..._2.
        Parameters
        ----------
        self : XmlSpecs object
        parent_path : Xpath of the parent element
        pre_tail_part : The tail part added in the previous step
        new_tail_part : The tail part obtained from present element

        Returns
        -------
        parent_path : Newly obtained or replaced parent Xpath
        pre_tail_part : Newly obtained or replaced tail_path
        """

        if new_tail_part == pre_tail_part:
            previous_key = f'{parent_path}/{new_tail_part}'
            previous_val = self.py_dict[previous_key]
            self.py_dict[f'{parent_path}/{new_tail_part}_0'] = previous_val
            pre_tail_part = f'{new_tail_part}_1'
            parent_path = f'{parent_path}/{pre_tail_part}'

            del self.py_dict[previous_key]

            return parent_path, pre_tail_part

        if new_tail_part in pre_tail_part:
            try:
                ind = pre_tail_part[pre_tail_part.rindex("_"):]
                ind = int(ind)
                pre_tail_part = f'{new_tail_part}_{ind +1}'
                parent_path = f'{parent_path}/{pre_tail_part}'
                return parent_path, pre_tail_part
            except ValueError:
                parent_path = f'{parent_path}/{new_tail_part}'
                pre_tail_part = new_tail_part

                return parent_path, pre_tail_part
            except TypeError:
                parent_path = f'{parent_path}/{new_tail_part}'
                pre_tail_part = new_tail_part

                return parent_path, pre_tail_part

        parent_path = f'{parent_path}/{new_tail_part}'
        pre_tail_part = new_tail_part

        return parent_path, pre_tail_part

    @staticmethod
    def restructure_value(value_text: str,
                          element_tag: str) -> str:
        """
            Collect the value_text transform it to the data_type according
            to the type name provided by element_tag.
        Parameters
        ----------
        value_text : text data that would be 'unsigned long', 'double', 'string',
                    'boolean', 'enum/string'
        element_tag : tag name among 'unsigned long', 'double', 'string',
                    'boolean', 'enum/string'

        Returns
        -------

        """

        data_ty = {
            "double": np.double,
            "ulong": np.uint,
            "boolean": np.bool_
        }
        string_ty = ["string", "enum"]

        if not value_text:
            return None

        elif element_tag in string_ty:
            value_text = ' '.join(value_text.split()
                                  ).replace(' ', '_')
            return value_text

        elif element_tag in data_ty.keys():
            value_text = value_text.split()
            numpy_value = data_ty[element_tag](value_text)[...]
            if np.shape(numpy_value) == (1,):
                return numpy_value[0]
            return numpy_value

    def cumulate_counts_series(self,
                               scan_seq_elem: EmtT.Element,
                               counts_length: int =None,
                               cumulative_counts: np.ndarray = None,) -> np.ndarray:
        """
        Sum the counts over different scans. Each ScanSeaq contains
        multiple scans under the same physical environment. The
        multiple scans are usually taken to make the peaks visible and
        distinguishable.

        Parameters
        ----------
        scan_seq_elem : Element with ScanSeq tag
        counts_length : Number of count (length of 1D numpy array)
                        contain in each scan
        cumulative_counts : Cumulative counts up to last scan  from the
                            same ScanSeq

        Returns
        -------
        np.ndarray : Cumulative up to last scans from the same ScanSeq
        """

        elmt_attr = scan_seq_elem.attrib
        child_num = len(scan_seq_elem)
        name = "count"

        child_elmt_ind = 0
        while child_num >= 0:

            if scan_seq_elem.attrib['type_name'] == "CountsSeq":
                num_of_counts = int(scan_seq_elem.attrib['length'])
                if not counts_length:
                    counts_length = num_of_counts
                if counts_length != num_of_counts:
                    raise ValueError(f'Count number from all the '
                                     f'scans must be equals!!')

            if scan_seq_elem.attrib['type_name'] == 'Counts':
                counts_data = self.restructure_value(scan_seq_elem.text,
                                                     scan_seq_elem.tag)

                if cumulative_counts is None:
                    cumulative_counts = counts_data
                else:
                    cumulative_counts = cumulative_counts + counts_data

            if child_num > 0:
                child_element = scan_seq_elem[child_elmt_ind]
                name, cumulative_counts = self.cumulate_counts_series(
                                                        child_element,
                                                        counts_length,
                                                        cumulative_counts)

            child_num = child_num - 1
            child_elmt_ind = child_elmt_ind + 1

        return name, cumulative_counts

    @property
    def data_dict(self) -> dict:
        """
            Getter property
        Parameters
        ----------

        Returns
        -------
        python dictionary
        """

        print("DEBUG : this is test get_dict_function")
        return self.py_dict


class XpsDataFileParser(object):
    """
        Class intended for receiving any type of XPS data file. So far it
        accepts xml file from specs vendor.
    """

    __prmt_file_ext__ = ['xml']
    __vendors__ = ['specs']
    __prmt_vndr_cls = {'xml': {
                                'specs': XmlSpecs
                               }
                       }

    __file_err_msg__ = (f'Need a xps data file with the following'
                        f'\n extension {__prmt_file_ext__}')

    __vndr_err_msg__ = (f'Need a xps data file from the following'
                        f'\n {__vendors__} vendors')

    def __init__(self, file_paths: str = "") -> None:
        """
            Receive XPS file path.
        Parameters
        ----------
        file_paths : XPS file path.
        """

        self.files = file_paths

        if not self.files:
            raise ValueError(XpsDataFileParser.__file_err_msg__)

    def get_dict(self) -> dict:

        """
            Return python dict fully filled data from xps file.
        Returns
        -------
        python dictionary
        """

        for file in self.files:
            file_ext = file.rsplit(".")[-1]
            if file_ext in XpsDataFileParser.__prmt_file_ext__:

                if file_ext == 'xml':
                    self.root_element = EmtT.parse(file).getroot()
                    vendor = XpsDataFileParser.check_for_vendors(self.root_element)

                    try:
                        parser_class = (XpsDataFileParser.
                                        __prmt_vndr_cls[file_ext]
                                        [vendor])
                        parser_obj = parser_class(root_element=self.root_element,
                                                  vendor_name=vendor)
                        parser_obj.parse_xml()
                        return parser_obj.data_dict

                    except ValueError:
                        ValueError(XpsDataFileParser.__vndr_err_msg__)
                    except KeyError:
                        KeyError(XpsDataFileParser.__vndr_err_msg__)
            else:
                raise ValueError(XpsDataFileParser.__file_err_msg__)

    @classmethod
    def check_for_vendors(cls, root_element: EmtT) -> str:
        """
            Check for the vendor name of the XPS data file.
        Parameters
        ----------
        root_element : xml root element.

        Returns
        -------
        Vendor name
        """

        # check for "specs" vendor in xml file
        vendor = "specs"
        child_element = root_element[0]
        child_attr = child_element.attrib

        for key in child_attr.keys():
            if vendor in child_attr[key]:
                return vendor
        raise None



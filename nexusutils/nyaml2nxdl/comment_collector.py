from typing import List, Type, Any, Tuple, Union
import xml.etree.ElementTree as ET
from nexusutils.nyaml2nxdl.nyaml2nxdl_helper import nx_name_type_resolving, LineLoader

__all__ = ['Comment', 'CommentCollector', 'XMLComment', 'YAMLComment']


class CommentCollector:
    """CommentCollector will store a full comment ('Comment') object in
    _comment_chain.
    """

    def __init__(self, input_file: str = None,
                 loaded_obj: object = None,
                 file_ext: str = None):
        """
        """
        self._comment_chain: List[Type[Comment]] = []
        self._next_comment = None
        self._next_comment_id = None
        self.file = input_file
        self._comment_tracker = 0
        self._comment_hash = {}

        if self.file and not loaded_obj:
            if self.file.split('.')[-1] == 'xml':
                self.Comment = XMLComment
            if self.file.split('.')[-1] == 'yaml':
                self.Comment = YAMLComment
                with open(self.file, "r", encoding="utf-8") as plain_text_yaml:
                    loader = LineLoader(plain_text_yaml)
                    self.Comment.__yaml_dict__ = loader.get_single_data()
        elif self.file and loaded_obj:
            if self.file.split('.')[-1] == 'yaml':
                self.Comment = YAMLComment
                self.Comment.__yaml_dict__ = loaded_obj
            else:
                raise ValueError("Incorrect inputs for CommentCollector e.g. Wrong file extension.")

        else:
            raise ValueError("Incorrect inputs for CommentCollector")

    def extract_all_comment_blocks(self):
        """
        """
        id_ = 0
        single_comment = self.Comment(comment_id=id_)
        self._next_comment = single_comment
        self._next_comment_id = single_comment.cid
        with open(self.file, mode='r', encoding='UTF-8') as f:
            lines = f.readlines()
            # Make an empty line for last comment if no enpty lines in original file
            lines.append('')
            for line_num, line in enumerate(lines):
                if single_comment.is_storing_single_comment():
                    # If the last comment comes without post nxdl fields, groups and attributes
                    if line_num < (len(lines) - 1):
                        # Line number in file starts from 1
                        single_comment.process_each_line(line, (line_num + 1))
                    else:
                        # For processing post comment
                        single_comment.process_each_line(line + 'post_comment', (line_num + 1))
                        self._comment_chain.append(single_comment)
                else:
                    self._comment_chain.append(single_comment)
                    single_comment = self.Comment(last_comment=single_comment)
                    single_comment.process_each_line(line, (line_num + 1))

    def get_comment(self):
        """
            Return comment from comment_chain that must come earlier in order.
        """
        return self._comment_chain[self._comment_tracker]

    def get_coment_by_line_info(self, comment_locs: tuple):
        """
            Get comment using line information.
        """
        if comment_locs in self._comment_hash:
            return self._comment_hash[comment_locs]
        else:
            line_annot, line_loc = comment_locs
            for cmnt in self._comment_chain:
                if line_annot in cmnt:
                    line_loc_ = cmnt.get_line_number(line_annot)
                    if line_loc == line_loc_:
                        self._comment_hash[comment_locs] = cmnt
                        return cmnt

    def reload_comment(self):
        """
        Update self._comment_tracker after done with last comment.
        """
        self._comment_tracker += 1

    def walk_next_comment(self):
        comment = self._comment_chain[self._next_comment_id]

        if comment.cid != self._next_comment_id:
            raise ValueError(f"Somthing worng in comment order in "
                             f"{self._next_comment.__name__}")
        else:
            self._next_comment_text = comment

    def __contains__(self, comment_locs: tuple):
        """
        Confirm wether the comment corresponds to key_line and line_loc
            is exist or not.
            comment_locs is equvalant to (line_annotation, line_loc) e.g.
            (__line__doc and 35)
        """
        if not isinstance(comment_locs, tuple):
            raise TypeError("Comment_locs should be 'tuple' containing line annotation "
                            "(e.g.__line__doc) and line_loc (e.g. 35).")
        line_annot, line_loc = comment_locs
        for cmnt in self._comment_chain:
            if line_annot in cmnt:
                line_loc_ = cmnt.get_line_number(line_annot)
                if line_loc == line_loc_:
                    self._comment_hash[comment_locs] = cmnt
                    return True
        return False

    def __getitem__(self, ind):
        """Get comment from  self_obj._comment_chain by index.
        """
        if ind >= len(self._comment_chain):
            raise IndexError(f'Oops! Coment index {ind} in {__class__} is out of range!')
        return self._comment_chain[ind]


class Comment:

    def __init__(self,
                 comment_id: int = -1,
                 last_comment: 'Comment' = None) -> None:
        """Comment object can be considered as a block element that includes
            document element (an entity for what the comment is written).
        """
        self._elemt: Any = None
        self._elemt_text: str = None
        self._is_elemt_found: bool = None
        self._is_elemt_stored: bool = None

        self._comnt: str = ''
        # If Multiple comments for one element or entity
        self._comnt_list: list[str] = []
        self.last_comment: 'Comment' = last_comment if last_comment else None
        if comment_id >= 0 and last_comment:
            self.cid = comment_id
            self.last_comment = last_comment
        elif comment_id == 0 and not last_comment:
            self.cid = comment_id
            self.last_comment = None
        elif last_comment:
            self.cid: int = (self.last_comment.cid + 1)
            self.last_comment = last_comment
        else:
            raise ValueError(f"Neither last comment nor comment id dound")
        self._comnt_start_found: bool = False
        self._comnt_end_found: bool = False
        self.is_storing_single_comment = lambda: not (self._comnt_end_found and self._is_elemt_stored)
        # TODO try to create a class level total comment and everytime update it
        self.total_comments: int = None

    def get_last_comment(self):
        return self.last_comment

    def get_comment_text(self) -> Union[List, str]:
        self._comnt

    def append_comment(self, text: str) -> None:
        pass

    def store_element(self, *keyargs) -> None:
        pass


class XMLComment(Comment):

    def __init__(self, comment_id: int = -1, last_comment: 'Comment' = None) -> None:
        super().__init__(comment_id, last_comment)

    def process_each_line(self, text, line_num):
        """Take care of each line of text. Through which function the text
        must be passed should be decide here.
        """
        text = text.strip()
        # TODO pass empty text as comment might contain empty line
        if text:
            self.append_comment(text)
            if self._comnt_end_found and not self._is_elemt_found:
                if self._comnt:
                    self._comnt_list.append(self._comnt)
                    self._comnt = ''

            if self._comnt_end_found:
                self.store_element(text)

    def append_comment(self, text: str) -> None:
        """
        """

        # Comment in single line
        if '<!--' == text[0:4]:
            self._comnt_start_found = True
            self._comnt_end_found = False
            self._comnt = self._comnt + text.replace('<!--', '')
            if '-->' == text[-4:]:
                self._comnt_end_found = True
                self._comnt_start_found = False
                self._comnt = self._comnt.replace('-->', '')

        elif '-->' == text[0:4] and self._comnt_start_found:
            self._comnt_end_found = True
            self._comnt_start_found = False
            self._comnt = self._comnt + '\n' + text.replace('-->', '')
        elif self._comnt_start_found:
            self._comnt = self._comnt + '\n' + text

    def store_element(self, text: str) -> None:
        """
        """

        def collect_xml_attributes(text_part):
            for part in text_part:
                part = part.strip()
                if part and '">' == ''.join(part[-2:]):
                    self._is_elemt_stored = True
                    self._is_elemt_found = False
                    part = ''.join(part[0:-2])
                elif part and '"/>' == ''.join(part[-3:]):
                    self._is_elemt_stored = True
                    self._is_elemt_found = False
                    part = ''.join(part[0:-3])
                elif part and '/>' == ''.join(part[-2:]):
                    self._is_elemt_stored = True
                    self._is_elemt_found = False
                    part = ''.join(part[0:-2])
                elif part and '>' == part[-1]:
                    self._is_elemt_stored = True
                    self._is_elemt_found = False
                    part = ''.join(part[0:-1])
                elif part and '"' == part[-1]:
                    part = ''.join(part[0:-1])

                if '="' in part:
                    lf_prt, rt_prt = part.split('="')
                else:
                    continue
                if ':' in lf_prt:
                    continue
                self._elemt[lf_prt] = str(rt_prt)
        if not self._elemt:
            self._elemt = {}
        # First check for comment part has been collected prefectly
        if '</' == text[0:2]:
            return
        elif '<' == text[0] and not '<!--' == text[0:4]:
            self._is_elemt_found = True
            text = text.replace('<', '', 1)
            text_part = text.split(' ')
            # collect tag
            self._elemt['tag'] = text_part[0]
            self._elemt['attrib'] = {}
            collect_xml_attributes(text_part[1:])

        elif self._is_elemt_found:
            text_part = text.split(' ')
            collect_xml_attributes(text_part)

    def get_element_info(self) -> dict:
        """
            The method returns info dict that includes:
        'tag' and 'attrib' keys.
        """
        return self._elemt

    def get_comment_text(self) -> Union[List, str]:
        """
            This method returns list of commnent text. As some xml element might have
            multiple separated comment intended for a single element.
        """
        return self._comnt_list


class YAMLComment(Comment):
    """

    NOTE:
     1. Do not delete any element form yaml dictionary (for loaded_obj. check: Comment_collector
     class. because this loaded file has been exploited in nyaml2nxdl forward tools.)
    """
    # Class level variable. The main reason behind that to follow structure of
    # abstract class 'Comment'
    __yaml_dict__: dict = {}
    __yaml_line_info: dict = {}
    __comment_escape_char = {'--': '-\\-'}

    def __init__(self, comment_id: int = -1, last_comment: 'Comment' = None) -> None:
        super().__init__(comment_id, last_comment)
        self.collect_yaml_line_info(YAMLComment.__yaml_dict__, YAMLComment.__yaml_line_info)

    def process_each_line(self, text, line_num):
        """Take care of each line of text. Through which function the text
        must be passed should be decide here.
        """
        text = text.strip()
        self.append_comment(text)
        if self._comnt_end_found and not self._is_elemt_found:
            if self._comnt:
                self._comnt_list.append(self._comnt)
                self._comnt = ''

        if self._comnt_end_found:
            line_key = ''
            if ':' in text:
                ind = text.index(':')
                line_key = '__line__' + ''.join(text[0:ind])

            for l_num, l_key in self.__yaml_line_info.items():
                if line_num == int(l_num) and line_key == l_key:
                    self.store_element(line_key, line_num)
                    break
                # Comment comes very end of the file
                elif text == 'post_comment' and line_key == '':
                    line_key = '__line__post_comment'
                    self.store_element(line_key, line_num)

    def has_post_comment(self):
        """
        Ensure is this a post coment or not.
        Post comment means the comment that come at the very end without having any
        nxdl element(class, group, filed and attribute.)
        """

        if '__line__post_comment' in self._elemt.keys():
            return True
        return False

    def append_comment(self, text: str) -> None:
        """
            Collects all the line of the same comment and
        append them with that single comment.
        """
        # check for escape char
        text = self.replace_scape_char(text)
        # Empty line after last line of comment
        if not text and self._comnt_start_found:
            self._comnt_end_found = True
            self._comnt_start_found = False
        # For empty line inside doc or yaml file.
        elif not text:
            return
        # TODO: keep comment block with '#' do not replace that
        elif '# ' == ''.join(text[0:2]):
            self._comnt_start_found = True
            self._comnt_end_found = False
            self._comnt = '' if not self._comnt else self._comnt + '\n'
            self._comnt = self._comnt + ''.join(text[2:])
        elif '#' == text[0]:
            self._comnt_start_found = True
            self._comnt_end_found = False
            self._comnt = '' if not self._comnt else self._comnt + '\n'
            self._comnt = self._comnt + ''.join(text[1:])
        elif 'post_comment' == text:
            self._comnt_end_found = True
            self._comnt_start_found = False
        # for any line after 'comment block' found
        elif self._comnt_start_found:
            self._comnt_start_found = False
            self._comnt_end_found = True

    def store_element(self, line_key: str, line_number: int):
        """
        """
        self._elemt = {}
        self._elemt[line_key] = int(line_number)
        self._is_elemt_found = False
        self._is_elemt_stored = True

    def get_comment_text(self):
        return self._comnt_list

    def get_line_number(self, line_key):
        """
        """
        return self._elemt[line_key]

    def get_line_info(self):
        """
            Return line annotation and line number from a comment.
        """
        for line_anno, line_loc in self._elemt.items():
            return line_anno, line_loc

    def __contains__(self, line_key):
        """For Checking whether __line__NAME is in _elemt dict or not."""
        return line_key in self._elemt

    def replace_scape_char(self, text):
        """Replace escape char according to __comment_escape_char dict
        """
        for ecp_char, ecp_alt in YAMLComment.__comment_escape_char.items():
            if ecp_char in text:
                text = text.replace(ecp_char, ecp_alt)
        return text

    def get_element_location(self) -> Union[Tuple, None]:
        """
        """
        if len(self._elemt) > 1:
            raise ValueError(f"Comment element should be one but got "
                             "{self._elemt}")

        for key, val in self._elemt.items():
            return key, val

    # TODO Try to make this function static
    # @staticmethod
    def collect_yaml_line_info(self, yaml_dict, line_info_dict):
        """Collect __line__key and corresponding value from
        a yaml file dictonary in another dictionary.
        """
        for line_key, line_n in yaml_dict.items():
            if '__line__' in line_key:
                line_info_dict[line_n] = line_key

        for _, val in yaml_dict.items():
            if isinstance(val, dict):
                self.collect_yaml_line_info(val, line_info_dict)


if __name__ == "__main__":
    file = ("/home/rubel/Nomad-FAIRmat/NomadGH/GH_Clone/nexus_definitions/base_classes"
            "/NXdata.nxdl.xml")
    collector = CommentCollector(file)
    collector.extract_all_comment_blocks()

    for comment in collector._comment_chain:
        print('comment text : ', comment.get_comment_text())
        print('comment line : ', comment.get_element_info(), '\n')

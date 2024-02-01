import re
# from collections import OrderedDict
# from faker import Faker
# from googletrans import Translator


class FormElement():
    _caller_prefix="FormElement"

    def __init__(self,agent,input_webElement):
        self._agent=agent
        self._web_element=input_webElement
        self._str,self.str_tokenized=self._gen_element_str()
        self._labels=[]
        self._possible_labels=[]
        self._pattern=None
        self._value=None
    def get_web_element(self):
        return self._web_element

    def set_web_element(self,web_element):
        self._web_element=web_element

    def get(self, attribute):
        return self._web_element.get_attribute(attribute)

    def _gen_element_str(self):
        eleid=self.get("id")
        elename = self.get("name")
        eleaction = self.get("action")
        eleplaceholder = self.get("placeholder")
        eletype = self.get("type")
        elevalue = self.get("value")
        elestr = "%s|%s|%s|%s|%s|%s" % (eleid, elename, eletype, eleaction, eleplaceholder, elevalue)
        eleset = set([eleid, elename, eletype, eleaction, eleplaceholder, elevalue]) - set([None]) - set(["undefined"]) - set( [""])
        return "%s|" % "|".join(eleset), list(eleset)
    def get_prop(self,property):
        return self._web_element.get_property(property)

    def get_labels(self, stringified=False):
        return self._labels if not stringified else "|".join(self._labels)

    def add_label(self, label):
        self._labels.append(label)

    def get_possible_labels(self, stringified=False):
        return self._possible_labels if not stringified else "|".join(self._possible_labels)

    def add_possible_label(self, label):
        self._possible_labels.append(label)

    def get_pattern(self):
        return self._pattern

    def set_pattern(self, pattern):
        self._pattern = pattern

    def get_element_str(self, tokenized=False):
        return self._str if not tokenized else self._str_tokenized

    def is_required(self):
        self._required = self._driver.is_required(self._web_element) \
                         or re.search(r"required|\*", self.get_labels(stringified=True), re.IGNORECASE) \
                         or re.search(r"required|\*", self.get("outerHTML"), re.IGNORECASE)
        return self._required

    def _get_input_length(self):
        input_length = None
        maxlength = self.get("maxlength")
        input_size = self.get_prop("size")
        maxlength = int(maxlength) if maxlength else maxlength
        input_size = int(input_size) if input_size else input_size
        if maxlength and maxlength <= 50 and maxlength > 0:
            input_length = maxlength
        if input_length is None and input_size and input_size <= 50 and input_size > 0:
            input_length = input_size
        if input_length is None:
            input_length = 12
        return input_length

class Form():
    _caller_prefix="Form"

    def __init__(self,agent,form):
        self._agent=agent
        self._form=form
        self._str,self._str_tokenized=self._gen_form_str()
        self._has_captcha=self._detect_captcha()


    def _gen_form_str(self):
        '''
        :return: a representation string
        '''
        elid = self._form.get_attribute("id")
        elname = self._form.get_attribute("name")
        elaction = self._form.get_attribute("action")
        elclass = self._form.get_attribute("class")
        elstr = "%s|%s|%s|%s" % (elid, elname, elaction, elclass)
        elset = set([elid, elname, elaction, elclass]) - set([None]) - set(["undefined"]) - set([""])
        return "%s|" % "|".join(elset), frozenset(elset)

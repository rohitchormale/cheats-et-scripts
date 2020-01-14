#!/usr/bin/env python

"""

This small utility is useful to build complex, nested dictionary/list templates.
This template can be filled by looking up values in another dictionary, similar to string templates.

e.g.

template = {
  "key1": "%(key1)s",
  "key2": "%(key2)s",
  "key3": [
    "foo",
    "bar",
    {
      "key4": "%(key1)s",
      "key5": "%(key1)s"
    }
  ],
  "key6": {
    "key7": "%(key7)s",
    "key8": "%(key8)s",
    "%(key9)s": [
      "foo",
      {
        "key10": "%(key10)s",
        "key11": "%(key11)s",
        "key12": "%(key12)s"
      },
      "bar",
      ["foo", "%(key14)s", {"foo": "bar", "%(key15)s": "%(key16)s"}]
    ]
  },
  "key13": "%(key13missing)s"
}

values = {
  "key1": "key1",
  "key2": "key2",
  "key3": "key3",
  "key4": "key4",
  "key5": "key5",
  "key6": "key6",
  "key7": "key7",
  "key8": "key8",
  "key9": "key9",
  "key10": "key10",
  "key11": "key11",
  "key12": "key12"
  "key14": "key14"
  "key15": "key15"
  "key16": "key16"
}

@author: Rohit Chormale
"""



import re

def fill_template(template, values, key_lookup=True, lookup_regex="%\((.*?)\)s"):
    """Fill complex dictionary templates with values from another dict.
  
    Parameters:
    template (dict): Dictionary template with placeholders to fill up
    values (dict): Dictionary of placeholder-values. Each placeholder in template will be replaced by related value in this dictionary 
    key_lookup (boolean): By default, both key and values having placeholders will be filled up. To disable, key fill up, set this option 'False'
    lookup_regex (string): Provide custom regex for placeholder. Default placeholder pattern will be '%(placeholder)s'
    Returns:
    dict: Template by filling up values
    """

    def lookup(text):
        try:
            placeholder = re.compile(lookup_regex).search(text).group(1)
        except AttributeError:
            placeholder = None
        if placeholder is not None and placeholder in values:
            return values[placeholder]
        return text

    def fill_list(list_template):
        temp = []
        for i in list_template:
            if isinstance(i, str) and i.strip() != "":
                temp.append(lookup(i))
            elif isinstance(i, dict):
                filled_dict = fill_dict(i)
                temp.append(filled_dict)
            elif isinstance(i, list):
                filled_list = fill_list(i)
                temp.append(filled_list)
            else:
                temp.append(i)
        return temp


    def fill_dict(dict_template):
        temp = {}
        for i, j in dict_template.items():
            k = lookup(i) if key_lookup else i
            if isinstance(j, str) and j.strip() != "":
                temp[k] = lookup(j)
            elif isinstance(j, dict):
                filled_dict = fill_dict(j)
                temp[k] = filled_dict
            elif isinstance(j, list):
                filled_list = fill_list(j) 
                temp[k] = filled_list
            else:
                temp[k] = j
        return temp

    if isinstance(template, list):
        return fill_list(template)
    elif isinstance(template, tuple):
        output = fill_list(template)
        return tuple(output)
    elif isinstance(template, dict):
        return fill_dict(template)
    else:
        return lookup(template)



import unittest
class FillDictTemplate(unittest.TestCase):
    def test_fill_template(self):
        template = {
            "key1": "%(key1)s",
            "key2": "%(key2)s",
            "key3": ["foo", "bar", {"key4": "%(key1)s", "key5": "%(key1)s"}],
            "key6": {"key7": "%(key7)s", "key8": "%(key8)s", "%(key9)s": ["foo", {"key10": "%(key10)s", "key11": "%(key11)s", "key12": "%(key12)s"}, "bar"]},
            "key13": "%(key13missing)s"
        }

        values = {
          "key1": "key1", "key2": "key2", "key3": "key3", "key4": "key4", "key5": "key5", "key6": "key6", "key7": "key7",
            "key8": "key8", "key9": "key9", "key10": "key10", "key11": "key11", "key12": "key12"
        }
        output = {
            "key1": "key1",
            "key2": "key2",
            "key3": ["foo", "bar", {"key4": "key1", "key5": "key1"}],
            "key6": {"key7": "key7", "key8": "key8", "key9": ["foo", {"key10": "key10","key11": "key11", "key12": "key12"}, "bar"]},
            "key13": "%(key13missing)s"
        }
        self.assertDictEqual(fill_template(template, values), output)


if __name__ == "__main__":
    unittest.main()



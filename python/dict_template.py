#!/usr/bin/env python3
"""

This small utility is useful to build complex, nested dictionaries templates.
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
      "bar"
    ]
  }
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
}

output = {
  "key1": "key1",
  "key2": "key2",
  "key3": [
    "foo",
    "bar",
    {
      "key4": "key1",
      "key5": "key1"
    }
  ],
  "key6": {
    "key7": "key7",
    "key8": "key8",
    "key9": [
      "foo",
      {
        "key10": "key10",
        "key11": "key11",
        "key12": "key12"
      },
      "bar"
    ]
  },
  "key13": "(key13missing)s"
}


@author: Rohit Chormale
"""

import re


def fill_dict_template(template, values, key_lookup=True, lookup_regex="%\((.*?)\)s"):
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

    temp = {}
    for i, j in template.items():
        k = lookup(i) if key_lookup else i
        if isinstance(j, str) and j.strip() != "":
            temp[k] = lookup(j)
        elif isinstance(j, list):
            subtemp = []
            for l in j:
                if isinstance(l, dict):
                    filled_dict = fill_dict_template(l, values)
                    subtemp.append(filled_dict)
                else:
                    subtemp.append(l)
            temp[k] = subtemp
        elif isinstance(j, dict):
            temp[k] = fill_dict_template(j, values)
        else:
            temp[k] = j
    return temp


import unittest
class FillDictTemplate(unittest.TestCase):
    def test_fill_dict_template(self):
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
        self.assertDictEqual(fill_dict_template(template, values), output)


if __name__ == "__main__":
    unittest.main()

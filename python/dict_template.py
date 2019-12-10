#!/usr/bin/env python3
"""

This small utility is useful to build complex, nested dictionaries templates.
This template can be filled by looking up values in another dictionary, similar to string templates.

e.g.

template = {
  "key1": "(key1)s",
  "key2": "(key2)s",
  "key3": [
    "foo",
    "bar",
    {
      "key4": "(key1)s",
      "key5": "(key1)s"
    }
  ],
  "key6": {
    "key7": "(key7)s",
    "key8": "(key8)s",
    "key9": [
      "foo",
      {
        "key10": "(key10)s",
        "key11": "(key11)s",
        "key12": "(key12)s"
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


def placeholder_lookup(placeholder):
    """Extract placeholder from given string if present."""
    try:
        return re.compile("\((.*?)\)s").search(placeholder).group(1)
    except AttributeError:
        return None


def fill_dict_template(template, values):
    """fill complex dictionary templates with values from another dict."""
    temp = {}
    for i, j in template.items():
        if isinstance(j, str) and j.strip() != "":
            placeholder = placeholder_lookup(j)
            if placeholder is not None and placeholder in values:
                temp[i] = values[placeholder]
            else:
                temp[i] = j
        elif isinstance(j, list):
            subtemp = []
            for k in j:
                if isinstance(k, dict):
                    filled_dict = fill_dict_template(k, values)
                    subtemp.append(filled_dict)
                else:
                    subtemp.append(k)
            temp[i] = subtemp
        elif isinstance(j, dict):
            temp[i] = fill_dict_template(j, values)
        else:
            temp[i] = j
    return temp


import unittest
class FillDictTemplate(unittest.TestCase):
    def test_fill_dict_template(self):
        template = {
            "key1": "(key1)s",
            "key2": "(key2)s",
            "key3": ["foo", "bar", {"key4": "(key1)s", "key5": "(key1)s"}],
            "key6": {"key7": "(key7)s", "key8": "(key8)s", "key9": ["foo", {"key10": "(key10)s","key11": "(key11)s", "key12": "(key12)s"}, "bar"]},
            "key13": "(key13missing)s"
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
            "key13": "(key13missing)s"
        }
        self.assertDictEqual(fill_dict_template(template, values), output)


if __name__ == "__main__":
    unittest.main()

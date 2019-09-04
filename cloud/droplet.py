#!/usr/bin/env python3
"""
DO 'test' droplet management tool.

Usage: droplet.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  add       Add new droplet with defaults
  defaults  Show defaults set to create new droplet
  remove    Remove default droplet 'blogtest', if available
  slugs     See all available image slugs
  sshkeys   Show all available ssh keys

"""

import requests
import json
import time
import os
import sys
import click
from pprint import pprint


api_token = os.environ.get("DO_KEY")
if not api_token:
    print("Add API KEY in system environmental variables.")
    sys.exit(1)
auth = "Bearer %s" % api_token
HEADERS = {"Content-Type": "application/json", "Authorization": auth}
api_base_url = "https://api.digitalocean.com/v2"
IMG_DEFAULTS = {
    "name": "test",
    "floating_ip": "",
    "region": "blr1",
    "ssh_keys": [],
    "backup": False,
    "ipv6": False,
    "user_data": None,
    "private_networking": True,
    "volume": None,
    "tags": [],
    "size": "s-1vcpu-1gb",
    "image": "ubuntu-18-04-x64",
    # "image": "ubuntu-16-04-x64",
    # "image": "debian-8-x64",
    # "image": "centos-7-x64",
}


def image_slugs():
    """Return set of image slugs"""
    url = "%s/images?per_page=999" % api_base_url
    resp = requests.get(url=url, headers=HEADERS)
    jdata = json.loads(resp.content)
    images = jdata["images"]
    slugs = [image["slug"] for image in images]
    slugs = [slug for slug in slugs if slug]
    return sorted(set(slugs))


def ssh_keys():
    """List SSH key data"""
    url = "%s/account/keys" % api_base_url
    resp = requests.get(url=url, headers=HEADERS)
    jdata = json.loads(resp.content)
    ssh_keys = jdata["ssh_keys"]
    temp = {i["name"]: i["id"] for i in ssh_keys}
    return temp


def droplet_status(droplet_id):
    """Check STATUS of newly added droplet. Is it still active or not. Return Boolean True/False"""
    url = "%s/droplets/%s" % (api_base_url, droplet_id)
    resp = requests.get(url=url, headers=HEADERS)
    jdata = json.loads(resp.content)
    return jdata["droplet"]["status"]


def add_droplet(**kwargs):
    """Add droplet with given config"""
    droplet_id = droplet_id_by_name(kwargs["name"])
    if droplet_id:
        print("Droplet already exist. Aborting...")
        return None

    print("Adding droplet - %(name)s | %(image)s | %(size)s | %(region)s" % kwargs)
    url = "%s/droplets" % api_base_url
    resp = requests.post(url=url, headers=HEADERS, json=kwargs)
    jdata = json.loads(resp.content)
    droplet_id = jdata["droplet"]["id"]
    if not droplet_id:
        print("Failed to create droplet")
        return None

    print("Checking newly added droplet status...")
    while droplet_status(droplet_id) != "active":
        print("Not active yet")
        time.sleep(6)
    print("Status Active...")
    time.sleep(4)

    if not kwargs.get("floating_ip"):
        return
    print("Assigning floating ip...")
    url = "%s/floating_ips/%s/actions" % (api_base_url, kwargs["floating_ip"])
    data = {"type": "assign", "droplet_id": droplet_id}
    resp = requests.post(url=url, headers=HEADERS, json=data)
    jdata = json.loads(resp.content)
    return jdata


def droplet_id_by_name(name):
    """Add droplet with given config"""
    print("Checking droplet with existing name...")
    url = "%s/droplets" % api_base_url
    resp = requests.get(url=url, headers=HEADERS)
    jdata = json.loads(resp.content)
    droplet_ids = {i["name"]: i["id"] for i in jdata["droplets"]}
    droplet_id = droplet_ids.get(name)
    return droplet_id


def remove_droplet(droplet_id):
    """Delete droplet"""
    print("Deleting droplet - %s" % droplet_id)
    url = "%s/droplets/%s" %(api_base_url, droplet_id)
    resp = requests.delete(url=url, headers=HEADERS)
    return resp


def see_defaults():
    return IMG_DEFAULTS


###################
# CLICK commands
###################


@click.group()
def main():
    pass


@main.command()
@click.option("--image", default=IMG_DEFAULTS["image"])
def add(image):
    """Add new droplet with defaults"""
    IMG_DEFAULTS["image"] = image
    if not IMG_DEFAULTS["ssh_keys"]:
        print("SSH key access is not enabled.")
    resp = add_droplet(**IMG_DEFAULTS)
    print("Droplet %(name)s added successfully" % IMG_DEFAULTS)


@main.command()
@click.option("--name", default=IMG_DEFAULTS["name"])
def remove(name):
    """Remove default droplet 'blogtest', if available"""
    print("Removing droplet named - %s" % name)
    droplet_id = droplet_id_by_name(name)
    if not droplet_id:
        print("Droplet '%s' doesn't exist" % name)
        return
    resp = remove_droplet(droplet_id)
    print(resp.text)


@main.command()
def defaults():
    """Show defaults set to create new droplet"""
    temp = see_defaults()
    pprint(temp)


@main.command()
@click.option("--name", default="")
def slugs(name):
    """See all available image slugs"""
    slug_set = image_slugs()
    if not name:
        return pprint(slug_set)

    temp = list(filter(lambda slug: name in slug, slug_set))
    if not temp:
        print("No such image")
        return
    pprint(temp)


@main.command()
def sshkeys():
    """Show all available ssh keys"""
    pprint(ssh_keys())


if __name__ == "__main__":
    main()


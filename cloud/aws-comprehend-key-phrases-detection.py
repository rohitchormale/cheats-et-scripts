#!/usr/bin/env python
# -*- coding: utf-8 -*-


import boto3
ACCESS_KEY = ""
SECRET_KEY = ""
REGION = "us-east-1"


def get_key_phrases(content_list=[], lang="en"):
    """Get key phrases using AWS Comprehend ordered by confidence level in descending order.

    Args:
        content_list: list of strings to detect key phrases
        lang: language of text
    Returns:
        List of key phrases

    """
    key_phrases = []
    if not content_list or not isinstance(content_list, list):
        return key_phrases
    try: 
        client = boto3.client('comprehend', region_name=REGION, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        response = client.batch_detect_key_phrases(TextList=content_list, LanguageCode=lang)
        result_list = response['ResultList']
        for result in result_list:
            key_phrases += result['KeyPhrases']
        return sorted(key_phrases, key=lambda k: k['Score'], reverse=True)
    except Exception as e:
        print(e)
        return key_phrases


def scrap_content(url):
    """Extract content from webpage

    This function visits url using requests module and strips html tags from body content.

    Args:
        url: web url to extract content

    Returns:
        string
    """
    import re
    import requests
    response = requests.get(url)
    pattern = re.compile('<.*?>')
    content = re.sub(pattern, '', response.content)
    print(content)
    return content


content = [
    "Companies are trying to move beyond selling products to creating lasting relationships with customers. Many are seeking new revenue streams by selling software and other products as a service, similar to the model used by Salesforce.com Inc. Automakers such as General Motors, for example, look to interact directly with customers via connected-vehicle systems that help find nearby restaurants or parking lots. Manufacturers are looking beyond selling physical equipment to services that can monitor the health of that equipment in real time. Caterpillar Inc. is nurturing a growing line of subscription data services, analyzing data from sensors connected to their machines to help customers run building projects more profitably. To take advantage of the subscription model, CIOs must move away from large, centralized systems and embrace a microservices architecture, in which software applications are deployed as a set of independent, reusableservices, said Tien Tzuo, founder and chief executive of Zuora Inc., a decade-old company that provides cloud-based software to help companies manage subscription services. Doing so can allow firms to spin up new applications more quickly, and provide flexibility around where and how they run.",
    "Mr. Tzuo spoke with CIO Journal on Friday about how companies are shifting to subscription-based business models. Edited excerpts follow. WSJ: What kinds of firms are making the switch to subscription models?" 
    "The technology vertical is probably farthest along. Adobe&#8230;their shift to subscriptions is giving the whole software sector courage to do the same thing. We see a lot in media. We’re also seeing quite a bit in manufacturing: Caterpillar, Ford, General Motors. These are companies with physical products that they’re realizing are smart products, and they’re finding all these new revenue streams that they now can create and sell and monetize. What are the biggest hurdles for companies trying to make the shift to subscriptions? The way you build product is different. Modern companies are iterating based on what customers are doing and making quick decisions. There’s an acceleration, and you need the data, what people are clicking on. What should we be looking at, and how do you personalize down to the individual user?",
    "What CIOs are struggling with is they just spent 20 years standardizing these systems of record, built around an SAP or an Oracle core. Now the business is coming in and saying we need to iterate, we need to be agile and we need to experiment with a bunch of things. The way the IT organization works now … they say, OK, we can put it in our backlog, and in 12 months we can deliver something to you. The business says, I can’t do that. I need something now. There’s an agility there that IT needs to start to support, which means this whole infrastructure that they’ve standardized on is actually holding them back. How do CIOs begin to facilitate the switch? A company that’s more of a digital company will do a wholesale replacement of the quote-to-cash process. They’ll rip it out of Oracle and SAP and they’ll put it on a modern stack like us. A company like Caterpillar or General Motors says we’re still going to sell a lot of cars, but we (also) need a connected-car platform. So they’ll put a subscription management platform on the side of their core business. We’ll still use (the core system) to sell cars or to sell tractors, but let’s put in the digital platform or the subscription platform here. How does corporate IT architecture begin to shift over the next few years? You’re starting to hear a lot of people talking about microservices. Silicon Valley companies have always talked about that, but now you’re hearing it in enterprise IT. The general pattern is that the big monolithic system is not going to work. It just won’t scale. So how do you build systems that are independent and have their own data stores and can be hosted anywhere?",
    "We would argue that there should be a three-cloud architecture. We would say the anchor systems are your customer relationship management system, your financials &#8212; because at the end of the day you do need financials &#8212; and then you have what we call a subscriber management system. In these modern business models, you need a hub that shows your key subscribers and what they purchased. Your interactions with customers now are not some customer buying 50 widgets of something, and if you log in we save your payment information on file. Your customers say this is the subscription I have with you right now. It’s about modifying these plans, which is very different. That system then orchestrates provisioning and fulfillment, it orchestrates the accounting system, it generates all the invoices and payments that are related to all those plan changes. Having a three-cloud architecture, and then having things bolt around one of these three clouds is a stronger way to go. How far along would you say customers are in switching to microservices?  It’s very early. This is going to take five to 10 years. They’re probably trying to building new things on microservices, but they still have a lot of legacy stuff. As subscription happens, how does the role of the CIO change? The biggest thing is the classic model of IT, saying can you give me all of your requirements and I build something for you over time, just doesn’t work anymore. I don’t know what I want. I don’t know which connected car service will make a lot of money. I don’t know what the right pricing and packaging is that I’m going to hit on. I can’t even tell you all of the things I’m going to launch in the next 12 to 18 months. So when (business units) go to the IT organization and want to support something, they need to be able to do things in chunks and iterate really quickly, and so their systems have to really be able to support that."
    ]


if __name__ == "__main__":
    print(get_key_phrases(content))


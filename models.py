from boto.dynamodb2.table import Table, Item
from boto.dynamodb2.exceptions import ConditionalCheckFailedException, ItemNotFound
from copy import deepcopy
import boto.dynamodb2
from boto.dynamodb2.layer1 import DynamoDBConnection

import jsonpickle

import time
import json
import uuid

##############################
# Global vars, consts, extra #
##############################

dynamodb = boto.dynamodb2.connect_to_region(
                 'us-west-2',
                 aws_access_key_id='AKIAJ5R42GRJL4SYJVUA',
                 aws_secret_access_key='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')

# Tables
customers = Table("PolitiHack_Customers2", connection=dynamodb)
votes = Table("PolitiHack_Votes", connection=dynamodb)

# Use boolean for the tables
customers.use_boolean()

# Base class for all object models
class Model(object):
    def __init__(self, item):
        self.item = item

    # Factory methods
    @staticmethod
    def load_from_db(cls, key, consistent=True):
        if not issubclass(cls, Model):
            raise ValueError("Class must be a subclass of Model")

        # None keys cause dynamodb exception
        if key is None:
            return None

        item = None
        try:
            if cls == Customer:
                item = cls(cls.TABLE.get_item(phone_number=key))
            else:
                item = cls(cls.TABLE.get_item(phone_number_and_bill_id=key))
        except ItemNotFound:
            return None

        return item

    @staticmethod
    def load_from_data(cls, data):
        if not issubclass(cls, Model):
            raise ValueError("Class must be a subclass of Model")

        return cls(Item(cls.TABLE, data))

    # Attribute access
    def __getitem__(self, key):
        return self.item[key]

    def get(self, key, default=None):
        return self.item[key] if key in self.item else default

    def __setitem__(self, key, val):
        self.item[key] = val

    def __contains__(self, key):
        return key in self.item

    def update(self, atts):
        for key, val in atts.items():
            self[key] = val

    def get_data(self, version=None):
        return self.item._data

    # Database Logic
    def save(self):
        # Defauult dynamodb behavior returns false if no save was performed
        if not self.item.needs_save():
            return True

        try:
            return self.item.partial_save()
        except ConditionalCheckFailedException:
            return False

    def create(self):
        return self.item.save()

    def delete(self):
        return self.item.delete()

class CFields():
    PHONE_NUMBER = "phone_number"
    ZIP_CODE = "zip_code"
    PROMPTED = "prompted"
    BILL_ID = "bill_id"

class Customer(Model):
    FIELDS = CFields
    TABLE_NAME = "PolitiHack_Customers"
    TABLE = customers
    KEY = CFields.PHONE_NUMBER

    def __init__(self, item):
        super(Customer, self).__init__(item)

    @staticmethod
    def create_new(attributes={}):
        # Default Values
        return Model.load_from_data(Customer, attributes)

class VFields():
    PHONE_NUMBER_AND_BILL_ID = "phone_number_and_bill_id"
    VOTED_YES = "voted_yes"

class Vote(Model):
    FIELDS = VFields
    TABLE_NAME = "PolitiHack_Votes"
    TABLE = votes
    KEY = CFields.PHONE_NUMBER

    def __init__(self, item):
        super(Vote, self).__init__(item)

    @staticmethod
    def create_new(attributes={}):
        return Model.load_from_data(Vote, attributes)

def equality_helper(person, congress):
    if person and congress is "Yay" or not person and congress is not "Yay":
        return True
    return False

def get_stats(phone_number):
    voted_same = 0
    total_votes = 0
    customer = Model.load_from_db(Customer, phone_number)
    if customer.get(CFields.ZIP_CODE) is not None:
        congress_votes = sunlight.get_votes_by_congressman(customer[CFields.ZIP_CODE])
        for item in votes.scan():
            if item[VFields.PHONE_NUMBER_AND_BILL_ID].split("_")[0] == phone_number:
                bill_id = item.split("_")[0]
                if congress_votes.get(bill_id) is not None:
                    if equality_helper(item[VFields.VOTED_YES], congress_votes.get(bill_id)):
                        voted_same += 1
                    total_votes += 1

    if total_votes != 0:
        return voted_same / total_votes
    return -1

import os

from ontology.ont_sdk import OntologySdk
import json
import time

from Cryptodome.Random.random import randint
from celery import Celery
from ontology.smart_contract.native_contract.ontid import Attribute
from ontology.utils.contract_event import ContractEventParser
from data import config


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class ONTManager(object):

    def __init__(self):

        self.sdk = OntologySdk()
        self.wallet_path = config.WALLET_PATH
        self.password = config.WALLET_PASSOWRD
        self.gas_limit = config.GAS_LIMIT
        self.gas_price = config.GAS_PRICE

        self.sdk.rpc.connect_to_test_net()

        if not os.path.exists(self.wallet_path):
            self.sdk.wallet_manager.create_wallet_file(self.wallet_path)
            self.identity = self.create_ont_id()
            self.sdk.wallet_manager.save()
            print('created ont_id: ' + self.identity.ont_id)
            print('please restart and get test ONG and ONT at https://developer.ont.io/applyOng')
        else:
            self.sdk.wallet_manager.open_wallet(self.wallet_path)
            self.identity = self.sdk.wallet_manager.get_default_identity()
            if not config.ONT_ID_REGISTERED:
                self.registry_ont_id(self.identity.ont_id)
                print('registry_ont_id: ' + self.identity.ont_id)
                print('please set ONT_ID_REGISTERED to True')
            else:
                print('using ont_id: ' + self.identity.ont_id)

    def create_ont_id(self):
        return self.sdk.wallet_manager.create_identity(config.IDENTITY_LABEL, self.password)

    def registry_ont_id(self, ont_id):
        ctrl_acct = self.sdk.wallet_manager.get_control_account_by_index(self.identity.ont_id, 0, self.password)
        payer_acct = ctrl_acct
        tx_hash = self.sdk.native_vm.ont_id().registry_ont_id(
            ont_id,
            ctrl_acct,
            payer_acct,
            self.gas_limit,
            self.gas_price
        )
        self.sdk.wallet_manager.save()
        return tx_hash

    def get_notify(self, tx_hash):
        """

        :param tx_hash:
        :return:
        """
        ont_mgr = ONTManager()
        event = ont_mgr.sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        hex_contract_address = ont_mgr.sdk.native_vm.ont_id().contract_address
        if event:
            notify = ContractEventParser.get_notify_list_by_contract_address(event, hex_contract_address)
            return notify
        return None

    def get_ddo(self, ont_id):
        """

        :param ont_id:
        :return:
        """
        ont_mgr = ONTManager()
        ddo = ont_mgr.sdk.native_vm.ont_id().get_ddo(ont_id)
        return ddo

    def add_attribute(self, ont_id, attrib_key: str = '', attrib_type: str = '', attrib_value: str = ''):
        """

        :param ont_id:
        :param attrib_key:
        :param attrib_type:
        :param attrib_value:
        :return:
        """
        ont_mgr = ONTManager()
        attribute = Attribute(
            attrib_key=attrib_key,
            attrib_type=attrib_type,
            attrib_value=attrib_value
        )
        ctrl_acct = ont_mgr.sdk.wallet_manager.get_control_account_by_index(
            ont_id=ont_mgr.identity.ont_id,
            index=0,
            password=ont_mgr.password
        )
        payer_acct = ctrl_acct
        tx_hash = ont_mgr.sdk.native_vm.ont_id().add_attribute(
            ont_id=ont_id,
            ctrl_acct=ctrl_acct,
            attributes=attribute,
            payer=payer_acct,
            gas_limit=ont_mgr.gas_limit,
            gas_price=ont_mgr.gas_price
        )
        return tx_hash

    def remove_attribute(self, ont_id):
        """

        :param ont_id:
        :return:
        """
        ont_mgr = ONTManager()
        ctrl_acct = ont_mgr.sdk.wallet_manager.get_control_account_by_index(
            ont_id=ont_mgr.identity.ont_id,
            index=0,
            password=ont_mgr.password
        )
        payer_acct = ctrl_acct
        tx_hash = ont_mgr.sdk.native_vm.ont_id().remove_attribute(
            ont_id=ont_id,
            operator=ctrl_acct,
            attrib_key='work_data',
            payer=payer_acct,
            gas_limit=ont_mgr.gas_limit,
            gas_price=ont_mgr.gas_price
        )
        return tx_hash

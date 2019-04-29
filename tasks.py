import json
import time

from Cryptodome.Random.random import randint
from celery import Celery
from ontology.smart_contract.native_contract.ontid import Attribute
from ontology.utils.contract_event import ContractEventParser

from managers import ONTManager
from models import set_work_ont_id_and_tx_hash, set_work_tx_hash, set_work_tx_hash_and_ont_status
from models import PUBLISH, UNPUBLISH, PENDING_REVIEW, DELETED, TEMP
from ontology.exception.exception import SDKException


app = Celery('tasks')
app.config_from_object('data:config', namespace='CELERY')


@app.task
def reg_new_ont_id(work_data, ont_id):
    """

    :param work_data:
    :param ont_id:
    :return:
    """

    ont_mgr = ONTManager()

    print('reg_new_ont_id(): ', work_data, ont_id)

    new_ont_id = ont_mgr.create_ont_id().ont_id
    tx_hash = ont_mgr.registry_ont_id(new_ont_id)
    set_work_ont_id_and_tx_hash(work_id=work_data['work_id'], ont_id=new_ont_id, tx_hash=tx_hash)
    ont_id = new_ont_id

    get_create_notify(work_data=work_data, tx_hash=tx_hash, ont_id=ont_id)


@app.task
def get_notify(work_id, tx_hash, ont_id, ont_status):
    """

    :param work_id:
    :param tx_hash:
    :param ont_id:
    :return:
    """

    time.sleep(randint(7, 12))

    ont_mgr = ONTManager()
    print('get_notify(): ' + tx_hash)
    notify = ont_mgr.get_notify(tx_hash=tx_hash)
    if notify:
        print('notify', notify)
        ddo = ont_mgr.get_ddo(ont_id=ont_id)
        print('ddo', ddo)
        set_work_tx_hash_and_ont_status(work_id=work_id, ont_id=ont_id, tx_hash='', ont_status=ont_status)
    else:
        get_notify.delay(work_id=work_id, tx_hash=tx_hash, ont_id=ont_id, ont_status=ont_status)


@app.task
def get_create_notify(work_data, tx_hash, ont_id):
    """

    :param tx_hash:
    :param ont_id:
    :return:
    """

    ont_mgr = ONTManager()

    print('get_create_notify(): ' + json.dumps(work_data) + ' ' + tx_hash + ' ' + ont_id)

    if tx_hash:
        # 是新建的ont_id，等待区块写入
        time.sleep(randint(7, 12))

        notify = ont_mgr.get_notify(tx_hash=tx_hash)
        print('notify', notify)
        ddo = ont_mgr.get_ddo(ont_id=ont_id)
        print('ddo', ddo)

    # 如果没有tx_hash，表示不是新建，直接设置属性
    work_data_json = json.dumps(work_data)
    tx_hash = ont_mgr.add_attribute(
        ont_id=ont_id,
        attrib_key='work_data',
        attrib_type='string',
        attrib_value=work_data_json
    )
    set_work_tx_hash_and_ont_status(work_id=work_data['work_id'], ont_id=ont_id, tx_hash=tx_hash, ont_status=PENDING_REVIEW)

    get_notify.delay(work_id=work_data['work_id'], tx_hash=tx_hash, ont_id=ont_id, ont_status=PUBLISH)


@app.task
def get_delete_notify(work_id, ont_id):
    """

    :param ont_id:
    :return:
    """

    ont_mgr = ONTManager()

    print('get_delete_notify(): ' + str(work_id) + ' ' + ont_id)
    try:
        tx_hash = ont_mgr.remove_attribute(ont_id=ont_id)
        set_work_tx_hash_and_ont_status(work_id=work_id, ont_id=ont_id, tx_hash=tx_hash, ont_status=PENDING_REVIEW)
        get_notify.delay(work_id=work_id, tx_hash=tx_hash, ont_id=ont_id, ont_status=UNPUBLISH)
    except SDKException:
        set_work_tx_hash_and_ont_status(work_id=work_id, ont_id=ont_id, tx_hash='', ont_status=UNPUBLISH)

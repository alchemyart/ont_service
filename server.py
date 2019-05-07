import logging
import time
from concurrent import futures

import grpc
import json

import ont_pb2
import ont_pb2_grpc
from managers import ONTManager
from tasks import get_create_notify, get_delete_notify, reg_new_ont_id
from models import set_work_ont_id_and_tx_hash
from data import config
import requests


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class ONTService(ont_pb2_grpc.ONTServiceServicer):

    def __init__(self):
        self.ont_mgr = ONTManager()

    def CreateONTID(self, request, context):
        """
        作品上架 创建新的 ont_id
        :param request:
        :param context:
        :return:
        """

        print("C_2_S CreateONTID: >>>>> ", request)

        if not request.data:
            response = ont_pb2.ResponseData(
                return_code=-1,
                message="request data incorrect",
                data=''
            )
        else:
            work_data = json.loads(request.data)

            ont_id = work_data['ont_id']
            tx_hash = ''
            if not ont_id:
                reg_new_ont_id.delay(work_data=work_data, ont_id=ont_id)
                print('reg_new_ont_id(), work_data, ont_id', work_data, ont_id)
            else:
                get_create_notify.delay(work_data=work_data, tx_hash=tx_hash, ont_id=ont_id)
                print('get_create_notify(), work_data, tx_hash', work_data, tx_hash)

            response = ont_pb2.ResponseData(
                return_code=0,
                message="success",
                data=tx_hash
            )

        print("S_2_C CreateONTID: <<<<< ", response)

        return response

    def DeleteONTID(self, request, context):

        print("C_2_S DeleteONTID: >>>>> ", request)

        if not request.data:
            response = ont_pb2.ResponseData(
                return_code=-1,
                message="request data incorrect",
                data=''
            )
        else:
            work_data = json.loads(request.data)

            work_id = work_data['work_id']
            ont_id = work_data['ont_id']

            get_delete_notify.delay(work_id=work_id, ont_id=ont_id)

            response = ont_pb2.ResponseData(
                return_code=0,
                message="success",
                data=""
            )

        print("S_2_C DeleteONTID: <<<<< ", response)

        return response

    def ContractONTIDRegister(self, request, context):

        print("C_2_S ContractOntidRegister: >>>>> ", request)

        request_data = json.loads(request.data)

        result = requests.post(config.ONT_API_URL + '/api/v1/contract/ontid/register', json={
                'phone_cn': str('86*') + str(request_data['mobile']),
                'password': str(request_data['password']),
            })
        print(result.status_code, result.json())

        if result.status_code == 200:
            response = ont_pb2.ResponseData(
                return_code=0,
                message="success",
                data=result.json()
            )
        else:
            response = ont_pb2.ResponseData(
                return_code=-1,
                message="failed",
                data=result.status_code
            )

        print("S_2_C ContractOntidRegister: <<<<< ", response)

        return response

    def ContractPutBatch(self, request, context):

        print("C_2_S ContractPutBatch: >>>>> ", request)

        request_data = json.loads(request.data)

        print(request_data)

        result = requests.post(config.ONT_API_URL + '/api/v1/contract/put/batch', json=request_data)
        print(result.status_code, result.json())

        if result.status_code == 200:
            response = ont_pb2.ResponseData(
                return_code=0,
                message="success",
                data=result.json()
            )
        else:
            response = ont_pb2.ResponseData(
                return_code=-1,
                message="failed",
                data=result.status_code
            )

        print("S_2_C ContractPutBatch: <<<<< ", response)

        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ont_pb2_grpc.add_ONTServiceServicer_to_server(ONTService(), server)
    server.add_insecure_port('[::]:9090')
    server.start()

    print("listen: 9090")

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()

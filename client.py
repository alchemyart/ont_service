import logging

import grpc
import json


def run():
    import ont_pb2
    import ont_pb2_grpc
    with grpc.insecure_channel('127.0.0.1:9090') as channel:
        client = ont_pb2_grpc.ONTServiceStub(channel)

        work_data = {
            "work_id": 1,
            "ont_id": '',
            "trust anchor": "aaa",
            "crypto_function": "SHA256",
            "work": "hash",
            "uploadTime": "bbb",
            "work name": "ccc",
            "owner_id": "ddd",
            "group": "eee",
            "description": "fff",
            "awards": "ggg",
        }

        work_data_json = json.dumps(work_data)

        response = client.CreateONTID(ont_pb2.RequestData(
            data=work_data_json,
        ))
        print(response.return_code, response.message, response.data)

        # response = client.GetNotifyListByTXHash(ont_pb2.RequestData(
        #     data="ba08385a50644bf3de3136445b4553123ae8b9a1c488b01ac72a147b535ab0e9",
        # ))
        # print(response.return_code, response.message, response.data)

        # response = client.DeleteONTID(ont_pb2.RequestData(
        #     data="2",
        # ))
        # print(response.return_code, response.message, response.data)

        # response = client.GetCreateNotify(ont_pb2.RequestData(
        #     data=json.dumps({
        #         'tx_hash': '',
        #         'new_ont_id': '',
        #     }),
        # ))
        # print(response.return_code, response.message, response.data)


if __name__ == '__main__':
    logging.basicConfig()
    run()

import logging

import grpc
import json
import hashlib


def run():
    import ont_pb2
    import ont_pb2_grpc
    with grpc.insecure_channel('127.0.0.1:9090') as channel:
        client = ont_pb2_grpc.ONTServiceStub(channel)

        # work_data = {
        #     "work_id": 1,
        #     "ont_id": '',
        #     "trust anchor": "aaa",
        #     "crypto_function": "SHA256",
        #     "work": "hash",
        #     "uploadTime": "bbb",
        #     "work name": "ccc",
        #     "owner_id": "ddd",
        #     "group": "eee",
        #     "description": "fff",
        #     "awards": "ggg",
        # }
        #
        # work_data_json = json.dumps(work_data)
        #
        # response = client.CreateONTID(ont_pb2.RequestData(
        #     data=work_data_json,
        # ))
        # print(response.return_code, response.message, response.data)

        # response = client.GetNotifyListByTXHash(ont_pb2.RequestData(
        #     data="ba08385a50644bf3de3136445b4553123ae8b9a1c488b01ac72a147b535ab0e9",
        # ))
        # print(response.return_code, response.message, response.data)

        # response = client.DeleteONTID(ont_pb2.RequestData(
        #     data="2",
        # ))
        # print(response.return_code, response.message, response.data)

        # 注册 ontid
        # response = client.ContractONTIDRegister(ont_pb2.RequestData(
        #     data=json.dumps({
        #         'mobile': '13564618707',
        #         'password': '12345678',
        #     }),
        # ))

        hash_256 = hashlib.sha256()
        hash_str = 'https://pre-cdn.ggac.net/media/work/image/2019/04/ef02ff84-6250-11e9-9d03-0242c0a82002.jpg'
        hash_256.update(hash_str.encode('utf-8'))
        filehash = hash_256.hexdigest()

        filedetail = {
            'detail': [{
                'textline': ['2D', 'text'],
                'imageList': [filehash]
            }]
        }

        print(filedetail)

        filedetailjson = json.dumps(filedetail)
        filedetailhash = hashlib.sha256(filedetailjson.encode('utf-8')).hexdigest()

        print(filedetailhash)

        response = client.ContractPutBatch(ont_pb2.RequestData(
            data=json.dumps({
                'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJhdWQiOiJkaWQ6b250OkFVRG11NEoyVzF2cUpIRHRMUDhVeEhhdWoyZUtzUUh4dTYiLCJpc3MiOiJkaWQ6b250OkFhdlJRcVhlOVByYVY1dFlnQnF2VjRiVXE4TFNzdmpjV1MiLCJleHAiOjE1NTcyOTg1OTgsImlhdCI6MTU1NzIxMjE5OCwianRpIjoiYzMzM2EwNzBhYWY0NGE1NzkzMjU1NjlkYjIyMDNhMzQiLCJjb250ZW50Ijp7InR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJvbnRpZCI6ImRpZDpvbnQ6QVBHWDJ2Rm1Rck5RUVRkR0tjSGJOTURRNlVxOTNCbXRMaiJ9fQ.MDE5MWFkNDU1NWQyZDAwZTJjZWZmNTM3NGU5ZjEyMDU2ZjBkYmMyNzFmODgzMWY5OTI3NmVjZTRiYTlmYjQwMjM2NjE4NjE4ZTI3YTUwNjJjZWE3NGJjODcyMTNkMjU2NGIxM2VhNzhkZDBjMDNkMjcwNTU3M2Q2ODI0ZmMxOTZhOA',
                'user_ontid': 'did:ont:APGX2vFmQrNQQTdGKcHbNMDQ6Uq93BmtLj',
                'file_list': [
                    {
                        'filehash': filedetailhash,
                        'type': 'INDEX',
                        'detail': filedetail
                    },
                    {
                        'filehash': filehash,
                        'type': "IMAGE",
                        'detail': [
                            {
                                'imgUrl': hash_str
                            }
                        ]
                    },
                ]
            }),
        ))
        print(response.return_code, response.message, response.data)


if __name__ == '__main__':
    logging.basicConfig()
    run()

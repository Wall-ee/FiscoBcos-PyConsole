from client_config import client_config
from client.bcosclient import (
    BcosClient,
    BcosError
)
import os
from client.common.compiler import Compiler
from eth_utils import to_checksum_address
from client.datatype_parser import DatatypeParser

import tornado.web
import tornado.ioloop
import json
import time
import hashlib
import datetime

client = BcosClient()
info = client.init()
# 从文件加载abi定义
if os.path.isfile(client_config.solc_path) or os.path.isfile(client_config.solcjs_path):
    Compiler.compile_file("contracts/HelloWorld.sol")
    Compiler.compile_file("contracts/SimpleInfo.sol")

abi_file ="contracts/SimpleInfo.abi"
data_parser = DatatypeParser()
data_parser.load_abi_file(abi_file)
contract_abi = data_parser.contract_abi

# 部署合约
print("\n>>Deploy:---------------------------------------------------------------------")
with open("contracts/SimpleInfo.bin", 'r') as load_f:
    contract_bin = load_f.read()
    load_f.close()

# todo 这是部署合约的步骤，不使用上链接口可注释掉，避免每次启动本文件都生成一个区块。
result = client.deploy(contract_bin)
print("deploy", result)
print("new address : ", result["contractAddress"])
contract_name = os.path.splitext(os.path.basename(abi_file))[0]

# todo 合约地址可以放入缓存中 以合约名为key，不需要每次重启都部署合约，每次部署合约会添加一次交易。
to_address = result['contractAddress'] #use new deploy address
# to_address = "0xcda895ec53a73fbc3777648cb4c87b38e252f876" #use new deploy address
doQueryTest =False
'''
useful helper:
int(num,16)  hex -> int
hex(num)  : int -> hex
'''


# 发送交易上链接口
class TransHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        # 发送交易并获取交易执行结果。参数：合约地址、合约abi、参数列表、合约binary code
        if args[0] == 'rawTrans':
            print(self.request.body)
            requestData = json.loads(self.request.body.decode('utf-8'))
            hash = hashlib.sha1()
            hash.update(json.dumps(requestData, ensure_ascii=False).encode('utf-8'))
            requestData['hashCode'] = hash.hexdigest()
            requestData['time'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            transData = json.dumps(requestData, ensure_ascii=False)

            args = [transData, 1024, to_checksum_address('0x7029c502b4F824d19Bd7921E9cb74Ef92392FB1c')]
            receipt = client.sendRawTransactionGetReceipt(to_address, contract_abi, "set", args)
            txhash = receipt['transactionHash']
            # print("receipt:",receipt)
            self.write(txhash)


# 查询接口
class QueryHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        # 首页数据
        if args[0] == 'index':
            # {'blockNumber': '0x16', 'failedTxSum': '0x0', 'txSum': '0x16'}
            res = client.getTotalTransactionCount()
            high_block_num = blockNumber = int(res.get("blockNumber", "0x0"), 16)
            txSum = int(res.get("txSum", "0x0"), 16)
            failedTxSum = int(res.get("failedTxSum", "0x0"), 16)
            pbftView = int(client.getPbftView(), 16)
            print("首页数据:", blockNumber, txSum, failedTxSum, pbftView)
            consensusStatus = client.getConsensusStatus()
            highestblockNumber = consensusStatus[0].get("highestblockNumber")
            nodeList = consensusStatus[1]
            for i in nodeList:
                i["highestblockNumber"] = highestblockNumber
                i["static"] = "正常"
            block_list = []
            all_transaction_list = []
            transaction_list = []

            for x in range(high_block_num):
                # if get_block_Number >= 0:
                res = client.getBlockByNumber(high_block_num)
                transactions = res.get("transactions")
                for i in transactions:
                    i["blockNumber"] = int(i.get("blockNumber"), 16)
                    i["transactionIndex"] = int(i.get("transactionIndex"), 16)
                    i["time"] = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime(int(str(int(res.get("timestamp"), 16))[0:10])))
                all_transaction_list += transactions
                high_block_num -= 1
            print(all_transaction_list)

            now_time = time.time()
            data_list = []
            for i in range(15):
                data_list.append(time.strftime('%m-%d', time.localtime(now_time)))
                now_time -= 86400
            data_list = data_list[::-1]
            count_list = [0 for _ in range(15)]

            for one_transaction in all_transaction_list:
                try:
                    index = data_list.index(one_transaction.get("time").split(" ")[0][5:])
                    count_list[index] += 1
                except:
                    pass
            for j in range(4):
                get_blockNumber = blockNumber - j
                if get_blockNumber > 0:
                    block_msg = client.getBlockByNumber(get_blockNumber)
                    # print("【{}】".format(block_msg))
                    one_block_msg = {
                        "block_num": get_blockNumber,
                        "block_hash": block_msg.get("hash"),
                        "time": time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime(int(str(int(block_msg.get("timestamp"), 16))[0:10]))),
                        "transaction_num": len(block_msg.get("transactions"))
                    }
                    one_transaction_msg = {
                        "transaction_hash": block_msg.get("transactions")[0].get("hash", ""),
                        "from": block_msg.get("transactions")[0].get("from", ""),
                        "to": block_msg.get("transactions")[0].get("to", ""),
                        "time": time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime(int(str(int(block_msg.get("timestamp"), 16))[0:10]))),
                    }
                    block_list.append(one_block_msg)
                    transaction_list.append(one_transaction_msg)

            result = {
                "blockNumber": blockNumber,
                "txSum": txSum,
                "failedTxSum": failedTxSum,
                "pbftView": pbftView,
                "nodeList": nodeList,
                "block_list": block_list,
                "transaction_list": transaction_list,
                "data_list": data_list,
                "count_list": count_list
            }
            self.write(json.dumps(result))
        # 区块列表数据
        elif args[0] == 'block_list':
            block_list = []
            blockNumber = self.get_query_argument('blockNumber', '')
            blockHash = self.get_query_argument('blockHash', '')
            if blockNumber != '':
                res = client.getBlockByNumber(blockNumber)
                number = int(res.get("number"), 16)
                add_time = time.strftime("%Y-%m-%d %H:%M:%S",
                        time.localtime(int(str(int(res.get("timestamp"), 16))[0:10]))),
                transaction_num = len(res.get("transactions"))
                block_hash = res.get("hash")
                parentHash = res.get("parentHash")
                block_list.append(
                    {
                        "number": number,
                        "add_time": add_time[0],
                        "transaction_num": transaction_num,
                        "block_hash": block_hash,
                        "parentHash": parentHash
                    }
                )
                result = {
                    "block_num": 1,
                    "block_list": block_list
                }
                self.write(json.dumps(result))
            elif blockHash != '':
                res = client.getBlockByHash(blockHash)
                number = int(res.get("number"), 16)
                add_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                         time.localtime(int(str(int(res.get("timestamp"), 16))[0:10]))),
                transaction_num = len(res.get("transactions"))
                block_hash = res.get("hash")
                parentHash = res.get("parentHash")
                block_list.append(
                    {
                        "number": number,
                        "add_time": add_time[0],
                        "transaction_num": transaction_num,
                        "block_hash": block_hash,
                        "parentHash": parentHash
                    }
                )
                result = {
                    "block_num": 1,
                    "block_list": block_list
                }
                self.write(json.dumps(result))
            else:
                res = client.getTotalTransactionCount()
                blockNumber = int(res.get("blockNumber", "0x0"), 16)
                page = self.get_query_argument('page', '')
                get_block_Number = blockNumber - 10 * (int(page) - 1)
                for i in range(10):
                    if get_block_Number >= 0:
                        res = client.getBlockByNumber(get_block_Number)
                        number = int(res.get("number"), 16)
                        add_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                                 time.localtime(int(str(int(res.get("timestamp"), 16))[0:10]))),
                        transaction_num = len(res.get("transactions"))
                        block_hash = res.get("hash")
                        parentHash = res.get("parentHash")
                        block_list.append(
                            {
                                "number": number,
                                "add_time": add_time[0],
                                "transaction_num": transaction_num,
                                "block_hash": block_hash,
                                "parentHash": parentHash
                            }
                        )
                    get_block_Number -= 1
                result = {
                    "block_num": blockNumber + 1,
                    "block_list": block_list
                }
                self.write(json.dumps(result))
        # 交易列表数据
        elif args[0] == 'transaction_list':
            transaction_list = []
            blockNumber = self.get_query_argument('blockNumber', '')
            transactionHash = self.get_query_argument('transactionHash', '')
            if blockNumber != '':
                res = client.getBlockByNumber(blockNumber)
                transactions = res.get("transactions")
                for i in transactions:
                    i["blockNumber"] = int(i.get("blockNumber"), 16)
                    i["transactionIndex"] = int(i.get("transactionIndex"), 16)
                    i["time"] = time.strftime("%Y-%m-%d %H:%M:%S",
                        time.localtime(int(str(int(res.get("timestamp"), 16))[0:10])))

                transaction_list = transactions
                result = {
                    "transaction_num": 1,
                    "transaction_list": transaction_list
                }
                self.write(json.dumps(result))
            elif transactionHash != '':
                res = client.getTransactionByHash(transactionHash)
                blockNumber = int(res.get("blockNumber", ""), 16)
                block_res = client.getBlockByNumber(blockNumber)
                transactionTime = time.strftime("%Y-%m-%d %H:%M:%S",
                        time.localtime(int(str(int(block_res.get("timestamp"), 16))[0:10])))

                transaction_list.append(
                    {
                        "hash": res.get("hash", ""),
                        "from": res.get("from", ""),
                        "to": res.get("to", ""),
                        "blockNumber": int(res.get("blockNumber", ""), 16),
                        "transactionIndex": int(res.get("transactionIndex", ""), 16),
                        "time": transactionTime
                    }
                )
                result = {
                    "transaction_num": 1,
                    "transaction_list": transaction_list
                }
                self.write(json.dumps(result))
            else:
                res = client.getTotalTransactionCount()
                high_block_num = blockNumber = int(res.get("blockNumber", "0x0"), 16)
                transactionNumber = int(res.get("txSum", "0x0"), 16)
                page = int(self.get_query_argument('page', ''))
                # get_block_Number = blockNumber - 10 * (int(page) - 1)
                for x in range(blockNumber):
                    # if get_block_Number >= 0:
                    res = client.getBlockByNumber(blockNumber)
                    transactions = res.get("transactions")
                    for i in transactions:
                        i["blockNumber"] = int(i.get("blockNumber"), 16)
                        i["transactionIndex"] = int(i.get("transactionIndex"), 16)
                        i["time"] = time.strftime("%Y-%m-%d %H:%M:%S",
                                                  time.localtime(int(str(int(res.get("timestamp"), 16))[0:10])))
                    transaction_list += transactions
                    blockNumber -= 1
                result = {
                    "high_block_num": high_block_num,
                    "transaction_num": transactionNumber,
                    "transaction_list": transaction_list[10*(page-1):10*page]
                }
                self.write(json.dumps(result))
        # 区块详情数据
        elif args[0] == 'block_detail':
            blockHash = self.get_query_argument('blockHash', '')
            txresponse = client.getBlockByHash(blockHash)
            self.write(txresponse)
        # 交易详情以及交易回执数据
        elif args[0] == 'transaction_detail':
            transactionHash = self.get_query_argument('transactionHash', '')
            txresponse = client.getTransactionByHash(transactionHash)
            input = data_parser.parse_transaction_input(txresponse['input'])

            transactionReceipt = client.getTransactionReceipt(transactionHash)
            receiptInput = data_parser.parse_transaction_input(transactionReceipt['input'])

            if input is None:
                chain_data = ''
            else:
                chain_data = input.get('args')[0]
            if receiptInput is None:
                receipt_data = ''
            else:
                receipt_data = receiptInput.get('args')[0]
            result = {
                "txresponse": txresponse,
                "transactionReceipt": transactionReceipt,
                "chain_data": chain_data,
                "receipt_data": receipt_data
            }
            self.write(json.dumps(result))


application = tornado.web.Application([
    (r'/sendTrans/(.*)', TransHandler),
    (r'/query_info/(.*)', QueryHandler)
])

if __name__ == "__main__":
    application.listen(5555)
    tornado.ioloop.IOLoop.instance().start()
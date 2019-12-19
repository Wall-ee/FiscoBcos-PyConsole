from flask import Flask, request
import json
from process_logic import (
    get_index_data,
    get_block_list_data,
    get_transaction_list_data,
    get_transaction_detail_data,
    send_transaction_get_txhash,
    get_block_detail_data,
    get_data_parser
)

app = Flask(__name__,
            static_url_path="",
            static_folder="./static",)

data_parser, abi_file = get_data_parser()

# 获取主页的数据，包括预览，交易量图，最近的区块和交易
@app.route('/query_info/index', methods=['GET'])
def get_index():
    result = get_index_data()
    return json.dumps(result)


# 获取区块列表，根据区块高度或者区块哈希搜索或者根据页数取10个区块列表
@app.route('/query_info/block_list', methods=['GET'])
def get_block_list():
    blockNumber = request.args.get('blockNumber', '')
    blockHash = request.args.get('blockHash', '')
    page = request.args.get('page', '')
    result = get_block_list_data(blockNumber, blockHash, page)
    return json.dumps(result)


# 获取交易列表，根据区块高度或者交易哈希搜索或者根据页数取10个交易列表
@app.route('/query_info/transaction_list', methods=['GET'])
def get_transaction_list():
    blockNumber = request.args.get('blockNumber', '')
    transactionHash = request.args.get('transactionHash', '')
    page = request.args.get('page', '')
    result = get_transaction_list_data(blockNumber, transactionHash, page)
    return json.dumps(result)


# 根据区块哈希，获取区块的详情
@app.route('/query_info/block_detail', methods=['GET'])
def get_block_detail():
    blockHash = request.args.get('blockHash', '')
    txresponse = get_block_detail_data(blockHash)
    return json.dumps(txresponse)


# 根据交易哈希，获取交易详情和交易回执
@app.route('/query_info/transaction_detail', methods=['GET'])
def get_transaction_detail():
    transactionHash = request.args.get('transactionHash', '')
    result = get_transaction_detail_data(transactionHash)
    return json.dumps(result)


# 上传json格式数据，发送交易上链
@app.route('/sendTrans/rawTrans', methods=['POST'])
def send_transaction():
    requestData = json.loads(request.get_data().decode())
    txhash = send_transaction_get_txhash(requestData)
    # print("receipt:",receipt)
    return txhash


if __name__ == "__main__":
    app.run(port=5555, debug=True, host="0.0.0.0")

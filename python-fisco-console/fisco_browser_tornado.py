import tornado.web
import tornado.ioloop
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

data_parser, abi_file = get_data_parser()


# 发送交易上链接口
class TransHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        # 发送交易并获取交易执行结果。参数：合约地址、合约abi、参数列表、合约binary code
        if args[0] == 'rawTrans':
            requestData = json.loads(self.request.body.decode('utf-8'))
            txhash = send_transaction_get_txhash(requestData)
            self.write(txhash)


# 查询接口
class QueryHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        # 首页数据
        if args[0] == 'index':
            # {'blockNumber': '0x16', 'failedTxSum': '0x0', 'txSum': '0x16'}
            result = get_index_data()
            self.write(json.dumps(result))
        # 区块列表数据
        elif args[0] == 'block_list':
            blockNumber = self.get_query_argument('blockNumber', '')
            blockHash = self.get_query_argument('blockHash', '')
            page = self.get_query_argument('page', '')
            result = get_block_list_data(blockNumber, blockHash, page)
            self.write(json.dumps(result))
        # 交易列表数据
        elif args[0] == 'transaction_list':
            blockNumber = self.get_query_argument('blockNumber', '')
            transactionHash = self.get_query_argument('transactionHash', '')
            page = self.get_query_argument('page', '')
            result = get_transaction_list_data(blockNumber, transactionHash, page)
            self.write(json.dumps(result))
        # 区块详情数据
        elif args[0] == 'block_detail':
            blockHash = self.get_query_argument('blockHash', '')
            txresponse = get_block_detail_data(blockHash)
            self.write(txresponse)
        # 交易详情以及交易回执数据
        elif args[0] == 'transaction_detail':
            transactionHash = self.get_query_argument('transactionHash', '')
            result = get_transaction_detail_data(transactionHash)
            self.write(json.dumps(result))


application = tornado.web.Application([
    (r'/sendTrans/(.*)', TransHandler),
    (r'/query_info/(.*)', QueryHandler)
])

if __name__ == "__main__":
    application.listen(5555)
    tornado.ioloop.IOLoop.instance().start()
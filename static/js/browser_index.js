var app = new Vue({
    el: '#app',
    data: {
        blockNumber: 0,
        txSum: 0,
        failedTxSum: 0,
        pbftView:0,
        nodeList: [],
        block_list: [],
        transaction_list: []
    },
    created () {
        this.getData();
    },
    methods:{
        getData: function(){
            axios({
                method: 'get',
                url: "/query_info/index",
                headers: {
                    'Content-Type': 'application/json; charset=UTF-8',
                    'encoding': 'UTF-8',
                },
            })
                .then((response) => {
                    this.result_data = response.data;
                    this.blockNumber = this.result_data["blockNumber"]
                    this.txSum = this.result_data["txSum"]
                    this.failedTxSum = this.result_data["failedTxSum"]
                    this.pbftView = this.result_data["pbftView"]
                    this.nodeList = this.result_data["nodeList"]
                    this.block_list = this.result_data["block_list"]
                    this.transaction_list = this.result_data["transaction_list"]
                    this.data_list = this.result_data["data_list"]
                    this.count_list = this.result_data["count_list"]
                    option = {
                        title : {
                            text: '最近15天的交易量',
                            x: 'center',
                            align: 'right'
                        },
                        tooltip: {
                            trigger: 'item',
                            formatter: '{a} {c}'
                        },
                        xAxis: {
                            type: 'category',
                            boundaryGap: false,
                            data: this.data_list
                        },
                        yAxis: {
                            type: 'value'
                        },
                        series: [{
                            name: '交易量：',
                            data: this.count_list,
                            type: 'line'
                        }]
                    };
                    var myChart = echarts.init(document.getElementById('homeId'));
                    myChart.setOption(option);
                })
                .catch(function (error) {
                    console.log(error)
                });
        }
    }
});

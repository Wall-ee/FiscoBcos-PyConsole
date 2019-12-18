var app = new Vue({
    el: '#app',
    data: {
        query: window.location.search,
        transaction_detail: '',
        chain_data: '',
        receipt_data: '',
    },
    created () {
        this.get_transaction_detail();
    },
    methods:{
        get_transaction_detail: function(){
            console.log('发送请求')
            axios({
                method: 'get',
                url: "/query_info/transaction_detail" + this.query,
                headers: {
                    'Content-Type': 'application/json; charset=UTF-8',
                    'encoding': 'UTF-8',
                },
            })
                .then((response) => {
                    this.transaction_detail = response.data["txresponse"]
                    this.chain_data = response.data["chain_data"]
                    this.transactionReceipt = response.data["transactionReceipt"]
                    this.receipt_data = response.data["receipt_data"]
                    $('#id-div-detail').jsonViewer(this.transaction_detail)
                    $('#id-div-transactionReceipt').jsonViewer(this.transactionReceipt)
                    if(this.chain_data == '' && this.receipt_data == ''){

                    }else {
                        $('#chain_data').jsonViewer(JSON.parse(this.chain_data))
                        $('#receipt_data').jsonViewer(JSON.parse(this.receipt_data))
                    }

                })
                .catch(function (error) {
                    console.log(error)
                });
        },
        change_tab(number){
            if(number === 1){
                $('#id-div-one').css("display", "")
                $('#id-div-two').css("display", "none")
                $('#pane-first').css("display", "")
                $('#pane-second').css("display", "none")
                $("#tab-first").addClass("is-active");
                $("#tab-second").removeClass("is-active");
            }else if (number === 2){
                $('#id-div-one').css("display", "none")
                $('#id-div-two').css("display", "")
                $('#pane-first').css("display", "none")
                $('#pane-second').css("display", "")
                $("#tab-second").addClass("is-active");
                $("#tab-first").removeClass("is-active");
            }
        }
    }
});

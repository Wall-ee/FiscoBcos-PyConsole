var app = new Vue({
    el: '#app',
    data: {
        page: 1,
        blockNumber: '',
        transactionHash: '',
        transaction_list: [],
        transaction_num: 0,
        page_num: 0,
        high_block_num: 0,
    },
    created () {
        this.get_transaction_list();
    },
    methods:{
        get_transaction_list: function(){
            axios({
                method: 'get',
                url: "/query_info/transaction_list?page=" + this.page,
                headers: {
                    'Content-Type': 'application/json; charset=UTF-8',
                    'encoding': 'UTF-8',
                },
            })
                .then((response) => {
                    this.transaction_num = response.data["transaction_num"]
                    this.high_block_num = response.data["high_block_num"]
                    this.transaction_list = response.data["transaction_list"]
                    this.page_num = Math.ceil(this.transaction_num/10)
                    console.log(typeof this.transaction_num, this.transaction_num, this.page_num, this.high_block_num)

                })
                .catch(function (error) {
                    console.log(error)
                });
        },
        change_page(page){
            this.page = page
            if(this.page > 1){
                $("#id-button-left").removeAttr("disabled");
            }else if(this.page == 1){
                $("#id-button-left").attr("disabled", "disabled");
            }
            console.log("页数" , this.page)
        },
        subtract_page(){
            this.page -= 1
            if(this.page > 1){
                $("#id-button-left").removeAttr("disabled");
            }else if(this.page == 1){
                $("#id-button-left").attr("disabled", "disabled");
            }
            if(this.page < this.page_num){
                $("#id-button-right").removeAttr("disabled");
            }
            axios({
                method: 'get',
                url: "/query_info/transaction_list?page=" + this.page,
                headers: {
                    'Content-Type': 'application/json; charset=UTF-8',
                    'encoding': 'UTF-8',
                },
            })
                .then((response) => {
                    this.transaction_num = response.data["transaction_num"]
                    this.transaction_list = response.data["transaction_list"]
                    this.page_num = Math.ceil(this.transaction_num/10)
                    console.log(typeof this.block_num, this.block_num, this.page_num)

                })
                .catch(function (error) {
                    console.log(error)
                });
            console.log(this.page)
        },
        add_page(){
            this.page += 1
            // if(this.page > 1){
            //     $("#id-button-left").removeAttr("disabled");
            // }else if(this.page == 1){
            //     $("#id-button-left").attr("disabled", "disabled");
            // }
            if(this.page > 1){
                $("#id-button-left").removeAttr("disabled");
            }
            if(this.page == this.page_num){
                $("#id-button-right").attr("disabled", "disabled");
            }
            axios({
                method: 'get',
                url: "/query_info/transaction_list?page=" + this.page,
                headers: {
                    'Content-Type': 'application/json; charset=UTF-8',
                    'encoding': 'UTF-8',
                },
            })
                .then((response) => {
                    this.transaction_num = response.data["transaction_num"]
                    this.transaction_list = response.data["transaction_list"]
                    this.page_num = Math.ceil(this.transaction_num/10)
                    console.log(typeof this.block_num, this.block_num, this.page_num)

                })
                .catch(function (error) {
                    console.log(error)
                });
        },
        isNumber(val) {
            var regPos = /^\d+(\.\d+)?$/; //非负浮点数
            if(regPos.test(val)) {
                return true;
            } else {
                return false;
                }
            },
        search_block(){
            $("#id-button-right").attr("disabled", "disabled");
            num_or_hash = $("#id-input-text").val()
            a = this.isNumber(num_or_hash)
            if(a){
                this.blockNumber = num_or_hash
                console.log(this.blockNumber, this.high_block_num)
                if(this.blockNumber < 0 || this.blockNumber > this.high_block_num){
                    alert("输入正确的块高或哈希")
                }else {
                    console.log(num_or_hash, "number")
                    axios({
                        method: 'get',
                        url: "/query_info/transaction_list?blockNumber=" + this.blockNumber,
                        headers: {
                            'Content-Type': 'application/json; charset=UTF-8',
                            'encoding': 'UTF-8',
                        },
                    })
                        .then((response) => {
                            this.transaction_num = response.data["transaction_num"]
                            this.transaction_list = response.data["transaction_list"]
                            this.page_num = Math.ceil(this.transaction_num/10)
                            console.log(typeof this.block_num, this.block_num, this.page_num)

                        })
                        .catch(function (error) {
                            console.log(error)
                        });
                }
            }else {
                this.transactionHash = num_or_hash
                if (this.transactionHash.length != 66) {
                    alert("输入正确的块高或哈希")
                } else {
                    axios({
                        method: 'get',
                        url: "/query_info/transaction_list?transactionHash=" + this.transactionHash,
                        headers: {
                            'Content-Type': 'application/json; charset=UTF-8',
                            'encoding': 'UTF-8',
                        },
                    })
                        .then((response) => {
                            this.transaction_num = response.data["transaction_num"]
                            this.transaction_list = response.data["transaction_list"]
                            this.page_num = Math.ceil(this.transaction_num/10)
                            console.log(typeof this.block_num, this.block_num, this.page_num)

                        })
                        .catch(function (error) {
                            console.log(error)
                        });
                    console.log(num_or_hash, "hash")
                }
            }
        }
    }
});

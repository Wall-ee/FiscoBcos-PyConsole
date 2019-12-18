var app = new Vue({
    el: '#app',
    data: {
        query: window.location.search,
        block_detail: '',
        block_detail_str: ''
    },
    created () {
        this.get_block_detail();
    },
    methods:{
        get_block_detail: function(){
            console.log('发送请求')
            axios({
                method: 'get',
                url: "/query_info/block_detail" + this.query,
                headers: {
                    'Content-Type': 'application/json; charset=UTF-8',
                    'encoding': 'UTF-8',
                },
            })
                .then((response) => {
                    this.block_detail = response.data
                    $('#id-div-detail').jsonViewer(this.block_detail)
                    console.log('124', this.block_detail, typeof this.block_detail)

                })
                .catch(function (error) {
                    console.log(error)
                });
        },
    }
});

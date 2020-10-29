<script>
export default {
  name: 'getapikey',
  created : function(){
    sessionStorage.setItem('key', this.$route.query.oauth_verifier)
    console.log('created')
    this.axios.get("/setapikey", {
        params: {
          oauth_verifier: this.$route.query.oauth_verifier
        }
      })
      .then(() =>{
        location.href='http://127.0.0.1:8888/followersearch'
      })
      .catch((e) => {
        console.log(e.response)
      });
  }
}
</script>

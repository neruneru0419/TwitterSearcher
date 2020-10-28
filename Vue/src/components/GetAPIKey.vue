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
      .catch((e) => {
        console.log(e)
      });
  }
}
</script>

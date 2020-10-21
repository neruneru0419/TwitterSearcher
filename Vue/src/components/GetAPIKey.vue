<script>
export default {
  name: 'getapikey',
  created : function(){
    sessionStorage.setItem('key', this.$route.query.oauth_verifier)
    this.axios.get("http://127.0.0.1:8888/getapikey", {
        params: {
          oauth_verifier: this.$route.query.oauth_verifier
        }
      })
      .catch((e) => {
        console.log(e)
      });
    location.href='/followersearch'
  }
}
</script>

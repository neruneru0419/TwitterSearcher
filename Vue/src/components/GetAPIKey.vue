<script>
export default {
  name: "getapikey",
  created: function () {
    sessionStorage.setItem("oauthVerifier", this.$route.query.oauth_verifier);
    console.log("created");
    this.axios
      .get("/setapikey", {
        params: {
          oauth_verifier: this.$route.query.oauth_verifier,
        },
      })
      .then((response) => {
        location.href=response.data
      })
      .catch((e) => {
        console.log(e.response);
      });
  },
};
</script>

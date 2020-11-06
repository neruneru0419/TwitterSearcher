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
      .then(() => {
        console.log("hoge");
      })
      .catch((e) => {
        console.log(e.response);
      });
  },
};
</script>

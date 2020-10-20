<template>
  <b-container>
    <div>
      <h1>
        Tweet Searcher
      </h1>
    </div>
    <p>アプリの説明ほげほげ</p>
    <!--ここのボタンTwitterのアイコンにしたい-->
    <p><b-button variant="primary" onclick="location.href='http://127.0.0.1:8888/oauth'">ログインせず始める</b-button></p>
  </b-container>
</template>

<script>

export default {
  name: "Login",
  data(){
    return {
      user_name: '',
      url: "http://twitter.com/",
      names: "",
      icons: "",
      twData: "",
      loading: false,
      loaded: false
    }
  },
  methods: {
    getUserData(){
      this.loading = true
      this.axios.get("http://127.0.0.1:8888/get_userdata", {
        params: {
          user_name: this.user_name
        }
      })
      .then((response) =>{
        console.log(response.data.tw_data[0])
        this.twData = response.data.tw_data
        this.loading = false
        this.loaded = true
      })
      .catch((e) => {
        console.log(e)
      });
    },
    sortTweetData(){
      this.twData.sort(function(a, b) {
        return b.status-a.status
      })
      console.log(this.twData)
    },
    sortUserData(){
      this.twData.sort(function(a, b) {
        return b.follower-a.follower
      })
      console.log(this.twData)
    }
  }
  //ツイート数でソート
}
</script>

<style>
  #app {
    text-align: center;
  }
  h1{
    margin: 0 auto;
  }
</style>
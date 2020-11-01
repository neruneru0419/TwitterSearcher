<template>
  <div class="Login">
    <Header></Header>
    <b-container>
        <h1>
          Tweet Searcher
        </h1>
      <p>フォロワーだったりツイートの検索ツール</p>
      <p><b-button variant="primary" onclick="location.href='/oauth'">ログインして始める</b-button></p>
    </b-container> 
  </div>
</template>

<script>
import Header from "./Header"
export default {
  components: {
    Header
  },
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
  }
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
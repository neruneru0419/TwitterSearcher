<template>
  <b-container>
    <div>
      <h1>
        Tweet Searcher
      </h1>
    </div>
    <p>フォロワーだったりツイートの検索ツール</p>
    <p><b-button variant="primary" onclick="location.href='/oauth'">ログインして始める</b-button></p>
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
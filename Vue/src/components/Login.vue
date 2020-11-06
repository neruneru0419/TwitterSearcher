<template>
  <div class="Login">
    <Header></Header>
    <b-container>
        <h1>Tweet Searcher</h1>
      <p>TwitterSearcherはTwitterのフォロワーだったりツイートの検索ツールです。</p>
      <p>このサイトはTwitterアカウントが必要です。</p>
        <h2>フォロワー検索</h2>
        <p>対象のアカウントのフォロワーについて調べることができます。</p>
        <p><b-button variant="primary" href='/oauth?redirectURL=/followersearch'>ログインしてフォロワー検索を始める</b-button></p>
        <h2>ツイート検索</h2>
        <p>対象のアカウントのツイートについて調べることができます。</p>
        <p><b-button variant="primary" href='/oauth?redirectURL=/tweetsearch'>ログインしてツイート検索を始める</b-button></p>
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


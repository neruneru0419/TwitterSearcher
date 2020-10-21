<template>
  <div>
    <Header></Header>
    <b-container>
      <b-form-group label="アカウント名" description="TwitterIDを入力してください">
        <b-form-input v-model="user_name" placeholder="@"></b-form-input>
      </b-form-group>
      <b-form-group label="カウント数" description="ツイートを何件取得するか入力してください">
        <b-form-input v-model="tweetCount" placeholder=""></b-form-input>
      </b-form-group>
      <b-form-group label="検索ワード" description="ツイート内容を入力してください">
        <b-form-input v-model="searchWord" placeholder=""></b-form-input>
      </b-form-group>
      <p>
        <b-button variant="primary" @click="getTweetData(user_name)">ツイート取得</b-button>
      </p>

      <div id="loading" v-if="loading">
        <b-alert variant="primary" show>
          <p>loading...</p>
          <div class="spinner-border" role="status">
            <span class="sr-only">Loading...</span>
          </div>
        </b-alert>
      </div>
      <div id="twData" class="w-100" v-if="loaded">
        <div id="accounts">
          <div v-for="i in twData" :key="i.id">
              <b-card>
                <b-card-text>
                  {{i.tweet}}
                  <p>
                    リツイート数{{i.retweet_count}}
                    いいね数{{i.favorite_count}}
                  </p>
                </b-card-text>
              </b-card>
          </div>
        </div>
      </div>
      <b-form-group label="表示順" description="検索結果の表示方法を選択してください">
        <b-form-select v-model="selectedDisplayFormat" :options="options"></b-form-select>
      </b-form-group>
      
    </b-container>
  </div>
</template>

<script>
import Header from "./Header"
export default {
  components: {
    Header
  },
  name: "tweetSearch",
  data(){
    return {
      user_name: '',
      url: "http://twitter.com/",
      twData: "",
      query: "",
      tweetCount: 200,
      searchWord: "",
      loading: false,
      loaded: false,
      selected: null,
      options: [
        {value: 'デフォルト', text: 'デフォルト' },
        {value: 'リツイート数が多い順', text: 'リツイート数が多い順' },
        {value: 'いいね数が多い順', text: 'いいね数が多い順' },
        {value: 'ツイートアクティビティが多い順', text: 'ツイートアクティビティが多い順' },
      ]
    }
  },
  mounted() {
    if (localStorage.key) {
      this.query = sessionStorage.getItem("key");
    }
  },
  methods: {
    getTweetData(){
      this.loading = true
      this.axios.get("/tweetdata", {
        params: {
          user_name: this.user_name,
          tweet_count: this.tweetCount,
          search_word: this.searchWord,
          oauth_verifier: this.query
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
#twData {
  text-align: left;
  overflow: auto;
  height: 600px;
  width: 1000px;
},
#loading{
  width: 10%;
  margin: 0 auto;
  max-width: 500px;
}
</style>
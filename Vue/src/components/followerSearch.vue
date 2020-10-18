<template>
  <div>
    <Header></Header>
    <b-container>
       <p><b-button variant="primary" onclick="location.href='http://127.0.0.1:8888/oauth'">ログインして始める</b-button></p>

      <b-form-group label="アカウント名" description="TwitterIDを入力してください">
        <b-form-input v-model="user_name" placeholder="@"></b-form-input>
      </b-form-group>
      <b-form-group label="カウント数" description="フォロワーを何人取得するか入力してください">
        <b-form-input v-model="followerCount" placeholder=""></b-form-input>
      </b-form-group>
      <!--<p>
        相互フォロー

        <router-link to="/result">
        <b-button variant="primary">grfd</b-button>
        </router-link>
      </p>
      -->
      <p>
        {{query}}
        <b-button variant="primary" @click="getUserData(user_name)">フォロワー取得</b-button>
      </p>
      <div id="loading" v-if="loading">
        <b-alert variant="primary" show>
          <p>loading...</p>
          <div class="spinner-border" role="status">
            <span class="sr-only">Loading...</span>
          </div>
        </b-alert>
      </div>
      <div id="errorScreen" v-if="errorCode == 34">
        <b-alert variant="danger" show>
          <p>アカウントが見つかりませんでした</p>
        </b-alert>
      </div>
      <div id="twData" class="w-100" v-if="loaded">
        <div id="accounts">
          <div v-for="i in twData" :key="i.id">
            <img :src="i.user_icon" />
            <a :href="url + i.screen_name">
              {{i.user_name}}
            </a>
            <p>ツイート数{{i.status}} フォロー数{{i.friends}} フォロワー数{{i.follower}}</p>
          </div>
        </div>
      </div>
      <p v-if="loaded">Tweet Searcher</p>
      <b-form-group label="表示順" description="検索結果の表示方法を選択してください">
        <b-form-select v-model="selectedDisplayFormat" :options="options"></b-form-select>
      </b-form-group>
      <p>
        <b-button variant="primary" @click="sortData(user_name)">ソート</b-button>
      </p>
    </b-container>
  </div>
</template>

<script>
import Header from "./Header"
export default {
  components: {
    Header
  },
  name: 'followerSearch',
  data(){
    return {
      errorCode: Number,
      followerCount: null,
      user_name: '',
      url: "http://twitter.com/",
      icons: "",
      twData: Object,
      loading: false,
      loaded: false,
      query : "",
      selectedDisplayFormat: String,
      options: [
        {value: 'デフォルト', text: 'デフォルト' },
        {value: 'フォロワー数が多い順', text: 'フォロワー数が多い順' },
        {value: 'フォロー数が多い順', text: 'フォロー数が多い順' },
        {value: 'フォロワー-フォロー数が多い順', text: 'フォロワー-フォロー数が多い順' },
        {value: 'ツイート数が多い順', text: 'ツイート数が多い順' },
      ]
    }
  },
   mounted() {
     console.log("hoge")
    if (localStorage.key) {
      this.query = sessionStorage.getItem("key");
    }
  },
  methods: {
    getUserData(){
      this.loading = true
      this.axios.get("http://127.0.0.1:8888/followerdata", {
        params: {
          user_name: this.user_name,
          oauth_verifier: this.query
        }
      })
      .then((response) =>{
        console.log(response.data.tw_data[0])
        console.log(response.data.tw_data[0].code)
        this.twData = response.data.tw_data
        this.loading = false
        this.loaded = true
        this.errorCode = response.data.tw_data[0].code
      })
      .catch((e) => {
        console.log(e)
      });
    },
    sortData(){
      
      if (this.selectedDisplayFormat == "フォロー数が多い順") {
        this.twData.sort(function(a, b) {
          return b.friends - a.friends
        })
      }
      else if (this.selectedDisplayFormat == "フォロワー数が多い順") {
        this.twData.sort(function(a, b) {
          return b.follower - a.follower
        })
      }
      else if (this.selectedDisplayFormat == "フォロワー-フォロー数が多い順") {
        this.twData.sort(function(a, b) {
          return (b.follower - b.friends) - (a.follower - a.friends)
        })
      }
      else if (this.selectedDisplayFormat == "ツイート数が多い順") {
        this.twData.sort(function(a, b) {
          return b.status-a.status
        })
      }
    }
  }
  //ツイート数でソート
}
</script>

<style>
#twData {
  text-align: left;
  overflow: auto;
  height: 300px;
},
#loading{
  width: 10%;
  margin: 0 auto;
  max-width: 500px;
}
</style>
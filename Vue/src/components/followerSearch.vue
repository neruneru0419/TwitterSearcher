<template>
  <div>
    <Header></Header>
    <b-container>

      <b-form-group label="アカウント名" description="TwitterIDを入力してください">
        <b-form-input v-model="user_name" placeholder="@"></b-form-input>
      </b-form-group>
      <b-form-group label="カウント数" description="フォロワーを何人取得するか入力してください">
        <b-form-input v-model="followerCount" placeholder=""></b-form-input>
      </b-form-group>
      <p>
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
      <Result :twData="twData" :loaded="loaded"></Result>
      <b-form-group label="表示順" description="検索結果の表示方法を選択してください">
        <b-form-select v-model="selectedDisplayFormat" :options="options"></b-form-select>
      </b-form-group>
      <p>
        <b-button variant="primary" @click="sortData(user_name)">並び替え</b-button>
      </p>
    </b-container>
  </div>
</template>

<script>
import Header from "./Header"
import Result from "./Result"
export default {
  components: {
    Header,
    Result
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
      verifier : "",
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
      this.verifier = sessionStorage.getItem("key");
    }
  },
  methods: {
    getUserData(){
      this.loading = true
      this.axios.get("http://127.0.0.1:8888/followerdata", {
        params: {
          user_name: this.user_name,
          oauth_verifier: this.verifier
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
  //ツイート数でソート1
}
</script>

<style>
/* #twData {
  text-align: left;
  overflow: auto;
  height: 500px;
}
#loading{
  width: 10%;
  margin: 0 auto;
  max-width: 500px;
} */
</style>
<template>
  <b-container>
    <b-button variant="primary" onclick="location.href='http://127.0.0.1:8888/oauth'">Twitter認証</b-button>
    <p><b-input v-model="user_name" type="text" placeholder="アカウント名"></b-input></p>
    <p>
        {{hoge}}
      <b-button variant="primary" @click="getUserData(user_name)">フォロワー取得</b-button>
    </p>
    {{hoge}}
    <div id="loading" v-if="loading">
      <b-alert variant="primary" show>
        <p>loading...</p>
        <div class="spinner-border" role="status">
          <span class="sr-only">Loading...</span>
        </div>
      </b-alert>
    </div>
    <div id="twData" v-if="loaded">
      <div id="accounts">
      <p v-for="i in twData" :key="i.id">
        <img :src="i.user_icon" />
        <a :href="url + i.screen_name">
          {{i.user_name}}
        </a>
      </p>
      </div>
    </div>
    <b-button variant="primary" @click="sortUserData()" v-if="loaded">フォロワー数で並び替え</b-button>
    <b-button variant="primary" @click="sortTweetData()" v-if="loaded">ツイート数で並び替え</b-button>
  </b-container>
</template>

<script>
export default {
  name: "home",
  props: {
    hoge: String
  },
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
#twData {
  text-align: left;
  overflow: auto;
  height: 600px;
  width: 1000px;
},
#accounts {
  text-align: left;
},
#loading{
  width: 10%;
  margin: 0 auto;
  max-width: 500px;
}
</style>
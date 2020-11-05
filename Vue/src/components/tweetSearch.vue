<template>
  <div class="tweetSearch">
    <Header></Header>
    <h2 class="my-3">ツイート検索</h2>
    <b-container>
      <b-form-group label="アカウント名" description="TwitterIDを入力してください">
        <b-form-input v-model="user_name" placeholder=""></b-form-input>
      </b-form-group>
      <p>
        <b-button variant="primary" @click="getTweetData(user_name)">ツイート取得</b-button>
      </p>
      <Loading :loading="loading" :statusCode="statusCode"></Loading>

      <div v-if="!loading && statusCode==200">
        <div id="twData" class="w-100" :per-page="perPage" :current-page="currentPage" style="height:600px; overflow-y:scroll; text-align: left;">
          <div v-for="i in twData.slice((currentPage*perPage) - perPage, currentPage*perPage)" :key="i.id">
              <b-card>
                <a :href="'http://twitter.com/' + i.screen_name">
                    <img :src="i.user_icon" />
                </a>
                {{i.user_name}}
                <a :href="'http://twitter.com/' + i.screen_name">
                    @{{i.screen_name}}
                </a>
                <b-card-text>
                  {{i.tweet}}
                  <p>
                    {{parseDataTime(i.created_at)}}
                  </p>
                  <p>
                    リツイート数{{i.retweet_count}}
                    いいね数{{i.favorite_count}}
                  </p>
                </b-card-text>
              </b-card>
          </div>
        </div>
        <b-pagination
            v-model="currentPage"
            onclick="document.getElementById('twData').scrollTo(100, 0);"
            :total-rows="rows"
            :per-page="perPage"
            aria-controls="twData"
            limit=10
        ></b-pagination>
      </div>
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
import Loading from "./Loading"
export default {
  components: {
    Header,
    Loading
  },
  name: "tweetSearch",
  data(){
    return {
      user_name: '',
      twData: "",
      verifier: "",
      loading: false,
      statusCode: Number,
      selectedDisplayFormat: String,
      perPage: 20,
      currentPage: 1,
        options: [
          {value: 'デフォルト', text: 'デフォルト' },
          {value: 'リツイート数が多い順', text: 'リツイート数が多い順' },
          {value: 'いいね数が多い順', text: 'いいね数が多い順' },
        ]
      }
  },
  mounted() {
    if (sessionStorage.key) {
      this.verifier = sessionStorage.getItem("oauthVerifier");
    }
  },
  computed: {
    rows() {
      return this.twData.length
    }
  },
  methods: {
    getTweetData(){
      this.loading = true
      this.axios.get("/tweetdata", {
        params: {
          user_name: this.user_name,
          oauth_verifier: this.verifier
        }
      })
      .then((response) =>{
        console.log(response.data)
        this.loading = false
        this.twData = response.data.tw_data
        this.statusCode = response.status
      })
      .catch((e) => {
        console.log(e)
        this.loading = false
        this.statusCode = e.response.status
      });
    },
    sortData(){
      if (this.selectedDisplayFormat == "リツイート数が多い順") {
        this.twData.sort(function(a, b) {
          return b.retweet_count - a.retweet_count
        })
      }
      else if (this.selectedDisplayFormat == "いいね数が多い順") {
        this.twData.sort(function(a, b) {
          return b.favorite_count - a.favorite_count
        })
      }
      this.currentPage = 1
      document.getElementById('twData').scrollTo(100, 0)
    },
    parseDataTime(created_at){
        //午後5:37 · 2020年10月26日
        this.date = new Date(created_at)
        this.hour = this.date.getHours()
        this.minute = this.date.getMinutes()
        this.year = this.date.getFullYear()
        this.month = this.date.getMonth()
        this.day = this.date.getDate()
        this.datetime = this.hour + ":" + this.minute + " " + this.year + "年" + this.month + "月" + this.day + "日"
        return this.datetime
    }
  }
}
</script>


<template>
  <div class="followerSearch">
    <Header></Header>
    <h2 class="my-3">フォロワー検索</h2>
    <b-container>
      <b-form-group
        label="アカウント名"
        description="TwitterIDを入力してください"
      >
        <b-form-input v-model="user_name" placeholder=""></b-form-input>
      </b-form-group>
      <p>
        <b-button variant="primary" @click="getUserData(user_name)"
          >フォロワー取得</b-button
        >
      </p>
      <Loading :loading="loading" :statusCode="statusCode"></Loading>
      <div v-if="!loading && statusCode == 200">
        <div
          id="twData"
          class="w-100"
          :per-page="perPage"
          :current-page="currentPage"
          style="height: 600px; overflow-y: scroll; text-align: left"
        >
          <div
            v-for="i in twData.slice(
              currentPage * perPage - perPage,
              currentPage * perPage
            )"
            :key="i.id"
          >
            <b-card>
              <a :href="'http://twitter.com/' + i.screen_name">
                <img :src="i.user_icon" />
              </a>
              {{ i.user_name }}
              <a :href="'http://twitter.com/' + i.screen_name">
                @{{ i.screen_name }}
              </a>
              <b-card-text>
                ツイート数{{ i.status }} フォロー数{{
                  i.friends
                }}
                フォロワー数{{ i.follower }}
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
          limit="10"
        ></b-pagination>
      </div>
      <b-form-group
        label="表示順"
        description="検索結果の表示方法を選択してください"
      >
        <b-form-select
          v-model="selectedDisplayFormat"
          :options="options"
        ></b-form-select>
      </b-form-group>
      <p>
        <b-button variant="primary" @click="sortData(user_name)"
          >並び替え</b-button
        >
      </p>
    </b-container>
  </div>
</template>

<script>
import Header from "./Header";
import Loading from "./Loading";
export default {
  components: {
    Header,
    Loading,
  },
  name: "followerSearch",
  data() {
    return {
      statusCode: Number,
      user_name: "",
      verifier: "",
      twData: Object,
      loading: false,
      selectedDisplayFormat: String,
      perPage: 20,
      currentPage: 1,
      options: [
        { value: "フォロワー数が多い順", text: "フォロワー数が多い順" },
        { value: "フォロー数が多い順", text: "フォロー数が多い順" },
        {value: "フォロワー-フォロー数が多い順",text: "フォロワー-フォロー数が多い順",},
        { value: "ツイート数が多い順", text: "ツイート数が多い順" },
      ],
    };
  },
  mounted() {
    if (sessionStorage.key) {
      this.verifier = sessionStorage.getItem("oauthVerifier");
    }
  },
  computed: {
    rows() {
      return this.twData.length;
    },
  },
  methods: {
    getUserData() {
      this.loading = true;
      this.axios
        .get("/followerdata", {
          params: {
            user_name: this.user_name,
            oauth_verifier: this.verifier,
          },
        })
        .then((response) => {
          this.twData = response.data.tw_data;
          this.loading = false;
          this.loaded = true;
          this.statusCode = response.status;
        })
        .catch((e) => {
          console.log(e.response);
          this.loading = false;
          this.loaded = true;
          this.statusCode = e.response.status;
        });
    },
    sortData() {
      if (this.selectedDisplayFormat == "フォロー数が多い順") {
        this.twData.sort(function (a, b) {
          return b.friends - a.friends;
        });
      } else if (this.selectedDisplayFormat == "フォロワー数が多い順") {
        this.twData.sort(function (a, b) {
          return b.follower - a.follower;
        });
      } else if (
        this.selectedDisplayFormat == "フォロワー-フォロー数が多い順"
      ) {
        this.twData.sort(function (a, b) {
          return b.follower - b.friends - (a.follower - a.friends);
        });
      } else if (this.selectedDisplayFormat == "ツイート数が多い順") {
        this.twData.sort(function (a, b) {
          return b.status - a.status;
        });
      }
      this.currentPage = 1;
      document.getElementById("twData").scrollTo(100, 0);
    },
  },
};
</script>


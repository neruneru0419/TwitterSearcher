<template>
  
  <div class="overflow-auto" v-if="loaded && statusCode==200">
    <div id="twData" class="w-100" :per-page="perPage" :current-page="currentPage">
      <div id="accounts">
        <div v-for="i in twData.slice((currentPage*perPage) - perPage, currentPage*perPage)" :key="i.id">
          <b-card>
            <img :src="i.user_icon" />
            <a :href="'http://twitter.com/' + i.screen_name">
              {{i.user_name}}
            </a>
            <b-card-text>
              ツイート数{{i.status}} フォロー数{{i.friends}} フォロワー数{{i.follower}}
            </b-card-text>
          </b-card>
        </div>
      </div>
    </div>
    <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="perPage"
      aria-controls="twData"
      limit=10
    ></b-pagination>
  </div>
</template>

<script>
  export default {
    props: ["twData", "loaded", "statusCode"],
    data() {
      return {
        perPage: 20,
        currentPage: 1
      }
    },
    computed: {
      rows() {
        return this.twData.length
      }
    }
  }
</script>
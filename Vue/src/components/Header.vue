<template>
  <div>
    <b-navbar toggleable="sm" type="dark" variant="info" class=shadow >
      <b-navbar-brand active to="/">Tweet Searcher</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item active :href="redirectURL"><font-awesome-icon :icon="['fab','twitter']"/>ログイン</b-nav-item>
          <b-nav-item active to="/followersearch">フォロワー検索 </b-nav-item>
          <b-nav-item active to="/tweetsearch">ツイート検索</b-nav-item>
          
        </b-navbar-nav>
      </b-collapse>
        <b-navbar-nav class="ml-auto">
          <b-nav-item active href="https://github.com/neruneru0419/TwitterSearcher"><font-awesome-icon :icon="['fab','github']"/></b-nav-item>
        </b-navbar-nav>
    </b-navbar>
  </div>
</template>"
<script>
export default {
  computed: {
      redirectURL() {
        return "oauth?redirectURL=" + this.$route.path
      }
  },
};
</script>





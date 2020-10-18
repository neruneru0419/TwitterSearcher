<template>
  <div>
  <b-navbar toggleable="lg" type="dark" variant="info" class=shadow >
    <b-navbar-brand href="http://127.0.0.1:8080">Tweet Searcher</b-navbar-brand>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item active to="/followersearch">フォロワー検索 </b-nav-item>
        <b-nav-item active to="/tweetsearch">ツイート検索</b-nav-item>
        
      </b-navbar-nav>

      <b-navbar-nav class="ml-auto">
        <b-nav-item active href="http://twitter.com/nerun_neruneru"><font-awesome-icon :icon="['fab','twitter']"/></b-nav-item>
        <b-nav-item active href="http://github.com/neruneru0419"><font-awesome-icon :icon="['fab','github']"/></b-nav-item>
      </b-navbar-nav>

    </b-collapse>
  </b-navbar>
</div>
</template>

<style>
h1{
  margin: 0 auto;
}
</style>
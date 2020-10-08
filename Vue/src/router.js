import Vue from 'vue'
import Router from 'vue-router'
import Login from './components/Login.vue'
import TweetSearch from './components/tweetSearch.vue'
import FollowerSearch from './components/followerSearch.vue'
import Result from './components/Result.vue'


Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'login',
      component: Login
    },
    {
      path: '/tweetSearch',
      name: 'tweetSearch',
      component: TweetSearch
    },
    {
      path: '/followerSearch',
      name: 'followerSearch',
      component: FollowerSearch
    },
    {
      path: '/result',
      name: 'result',
      component: Result,
      props: {
        hoge: ""
      }
    }
  ]
})
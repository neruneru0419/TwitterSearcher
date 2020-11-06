import Vue from 'vue'
import Router from 'vue-router'
import Login from './components/Login.vue'
import TweetSearch from './components/tweetSearch.vue'
import FollowerSearch from './components/followerSearch.vue'
import getAPIKey from './components/GetAPIKey.vue'
import NotFound from './components/NotFound.vue'


Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
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
      path: '/getapikey',
      name: 'getapikey',
      component: getAPIKey
    },
    {
      path : '*',
      component: NotFound
    }

  ]
})

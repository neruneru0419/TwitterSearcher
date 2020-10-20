<template>
  <div id="app">
    <ul>
      <li v-for="(item, key) in getItems" :key="key">{{item}}</li>
    </ul>
    <paginate
    :page-count="getPageCount"
    :page-range="3"
    :margin-pages="2"
    :click-handler="clickCallback"
    :prev-text="'＜'"
    :next-text="'＞'"
    :container-class="'pagination'"
    :page-class="'page-item'">
  </paginate>
</div>
</template>

<script>


export default {
   el: '#app',
   data(){
     return {
      items: ["hoge", "huga", "hoge","hoge", "huga", "hoge","hoge", "huga", "hoge","hoge", "huga", "hoge","hoge", "huga", "hoge","hoge", "huga", "hoge","hoge", "huga", "hoge","hoge", "huga", "hoge","hoge", "huga", "hoge","hoge", "huga", "hoge","hoge", "huga", "hoge","hoge", "huga", "hoge","hoge", "huga", "hoge","hoge", "huga", "hoge"],
      parPage: 10,
      currentPage: 1
      }
   },
   methods: {
    clickCallback: function (pageNum) {
       this.currentPage = Number(pageNum);
    }
   },
   computed: {
     getItems: function() {
      let current = this.currentPage * this.parPage;
      let start = current - this.parPage;
      return this.items.slice(start, current);
     },
     getPageCount: function() {
      return Math.ceil(this.items.length / this.parPage);
     }
   }

 }
</script>
<template>
  <div class="Loading">
    <div id="loading" v-if="loading">
      <b-alert variant="primary" show>
        <p>loading...</p>
        <div class="spinner-border" role="status">
          <span class="sr-only">loading...</span>
        </div>
      </b-alert>
    </div>
    <div id="errorScreen" v-if="!loading && statusCode == 404">
      <b-alert variant="danger" show>
        <p>アカウントが見つかりませんでした。</p>
      </b-alert>
    </div>
    <div id="errorScreen" v-if="!loading && statusCode == 429">
      <b-alert variant="danger" show>
        <p>API制限です。時間を開けてもう一度お試しください。</p>
      </b-alert>
    </div>
    <div id="errorScreen" v-if="!loading && statusCode == 500">
      <b-alert variant="danger" show>
        <p>エラーが発生しました。</p>
      </b-alert>
    </div>
  </div>
</template>
<script>
export default {
  props: ["loading", "statusCode"],
};
</script>>
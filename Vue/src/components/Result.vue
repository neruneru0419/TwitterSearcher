<template>
  
  
</template>

<script>
  export default {
    props: ["twData", "loading", "statusCode"],
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
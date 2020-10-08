
<template>
    <div>
    <input type="text" v-model="msg">
    <button @click="get_followers(1)">get_follower
    </button>
    </div>
</template>

<script>
import twitter from "twitter"
export default {
    data(){
        return {
            client: new twitter({
                consumer_key: "tCTqrsqbW5ZbvuS2dP0GIMf3X",
                consumer_secret: "UsHI1qAN4TkeewaBEhtN8kvR8Lxt3VcCVQNo55C9fB0ZlqJFrn",
                access_token_key: "844798590211960832-smJduPo67q8iwAMfhJNyY9Ego6NEYJM",
                access_token_secret: "aaI4vr26MepDOCWmjNrUDeOJVYbCJoVAM2vRhdPQ0Bwo0"
            })
        }
    },
    methods: {
        get_followers(now_cursor){
            this.data = {screen_name: "Nerun_Neruneru",
                        count: 200, 
                        }
            if (now_cursor != 1){
                this.data.cursor = now_cursor;
            }
            this.client.get('followers/list', this.data, function(error, tweet) {
                if (!error) {
                    this.next_cursor = tweet.next_cursor;
                    for (this.i = 0; this.i < tweet.users.length; this.i++){
                        console.log(tweet.users[this.i].name);
                    }
                    if (now_cursor == 0){
                        return
                    }else{
                        this.get_followers(this.next_cursor)
                    }
                }
            })
        }
    }
}
    



//get_followers(client, 1)
</script>
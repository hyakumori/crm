<template>
  <v-content>
    <v-container grid-list-xs class="pa-0">
      <a
        :href="
          `https://slack.com/oauth/v2/authorize?scope=incoming-webhook,chat:write,channels:read&client_id=1201426909361.1188806865714&redirect_uri=${redirectUri}`
        "
        ><img
          alt="Add to Slack"
          height="40"
          width="139"
          src="https://platform.slack-edge.com/img/add_to_slack.png"
          srcset="
            https://platform.slack-edge.com/img/add_to_slack.png    1x,
            https://platform.slack-edge.com/img/add_to_slack@2x.png 2x
          "
      /></a>
    </v-container>
  </v-content>
</template>

<script>
export default {
  data() {
    return {
      redirectUri:
        process.env.SLACK_REDIRECT_URI || "http://localhost:8080/slack/oauth",
    };
  },
};
</script>

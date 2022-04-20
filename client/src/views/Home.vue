<template>
  <div>
    <iframe :src="iframe_url" v-if="iframe_url" class="metabase-iframe" />
  </div>
</template>

<script>
import querystring from 'querystring'
import { ReactiveRestApi } from '@unrest/vue-storage'

const storage = ReactiveRestApi()

export default {
  name: "HomeView",
  __route: { path: "/" },
  computed: {
    iframe_url() {
      const agency = this.$store.local.getActiveAgency()
      if (!agency) {
        return null
      }
      console.log(agency.id)
      const params = {
        dashboard: 50,
        cal_itp_id: agency.id,
      }
      const qs = querystring.stringify(params)
      return storage.get("metabase/?"+qs)?.iframe_url
    },
  },
}
</script>

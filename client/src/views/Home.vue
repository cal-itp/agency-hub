<template>
  <div>
    <div class="metabase-iframe">
      <iframe :src="iframe_url" v-if="iframe_url" />
      <div class="loader">
        <div class="loader__spinner" />
        Loading...
      </div>
    </div>
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
      const dashboard = this.$store.local.getActiveDashboard()
      if (!agency || !dashboard) {
        return null
      }
      console.log(agency.id)
      const params = {
        dashboard: dashboard.id,
        cal_itp_id: agency.id,
      }
      const qs = querystring.stringify(params)
      return storage.get("metabase/?"+qs)?.iframe_url
    },
  },
}
</script>

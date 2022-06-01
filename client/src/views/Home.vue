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
  __route: {
    path: "/",
    meta: { authRequired: true },
  },
  computed: {
    iframe_url() {
      const { agency, dashboard, url_number } = this.$store.local
      if (!agency || !dashboard) {
        return null
      }
      const params = {
        dashboard: dashboard.id,
        agency_id: agency.id,
        url_number,
      }
      const qs = querystring.stringify(params)
      return storage.get("metabase/?"+qs)?.iframe_url
    },
  },
}
</script>

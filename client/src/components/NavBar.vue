<template>
  <header class="navbar">
    <section class="navbar__section -left">
      <router-link class="navbar__brand" to="/">
        Agency Hub
      </router-link>
    </section>
    <section class="navbar__section -right">
      <template v-if="$auth.user">
        <unrest-dropdown v-if="dashboard_items?.length" :items="dashboard_items" class="btn -text">
          {{ $store.local.getActiveDashboard().name }}
        </unrest-dropdown>
        /
        <unrest-dropdown v-if="agency_items?.length" :items="agency_items" class="btn -text">
          {{ $store.local.getActiveAgency().name }}
        </unrest-dropdown>
        <template v-if="url_number_items?.length">
          /
          <unrest-dropdown :items="url_number_items" class="btn -text">
            ({{ $store.local.getActiveUrlNumber() }})
          </unrest-dropdown>
        </template>
      </template>
      <unrest-auth-menu />
    </section>
  </header>
</template>

<script>
import { sortBy, range } from 'lodash'

export default {
  computed: {
    agency_items() {
      const agencies = sortBy(this.$auth.user?.agencies || [], 'name')
      return agencies.map(agency => ({
        text: agency.name,
        click: () => this.$store.local.setActiveAgency(agency),
      }))
    },
    dashboard_items() {
      return this.$store.dashboard.getAll()?.map((dashboard) => ({
        text: dashboard.name,
        click: () => this.$store.local.setActiveDashboard(dashboard),
      }))
    },
    url_number_items() {
      const dashboard = this.$store.local.getActiveDashboard()
      const agency = this.$store.local.getActiveAgency()
      if (!dashboard || !agency || !dashboard.url_number || agency.url_count < 2) {
        return
      }
      return range(agency.url_count).map(url_number => ({
        text: `(${url_number})`,
        click: () => this.$store.local.setActiveUrlNumber(url_number),
      }))
    }
  },
}
</script>

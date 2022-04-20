<template>
  <header class="navbar">
    <section class="navbar__section -left">
      <router-link class="navbar__brand" to="/">
        Agency Hub
      </router-link>
    </section>
    <section class="navbar__section -right">
      <unrest-dropdown v-if="dashboard_items?.length" :items="dashboard_items" class="btn -text">
        Dashboard: {{ $store.local.getActiveDashboard().name }}
        <i class="fa fa-chevron-down" />
      </unrest-dropdown>
      <unrest-dropdown v-if="agency_items?.length" :items="agency_items" class="btn -text">
        Agency: {{ $store.local.getActiveAgency().name }}
        <i class="fa fa-chevron-down" />
      </unrest-dropdown>
      <unrest-auth-menu />
    </section>
  </header>
</template>

<script>
import { sortBy } from 'lodash'

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
  },
}
</script>

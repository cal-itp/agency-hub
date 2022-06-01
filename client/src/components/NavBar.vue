<template>
  <header class="navbar">
    <section class="navbar__section -left">
      <router-link class="navbar__brand" to="/">
        Agency Hub
      </router-link>
      <agency-alerts />
    </section>
    <section class="navbar__section -right">
      <div v-if="show_fields" class="navbar__options">
        <div>
          <vue-multiselect
            v-if="dashboards.length > 0"
            v-model="$store.local.dashboard"
            :allowEmpty="false"
            :options="dashboards"
            label="name"
            />
        </div>
        /
        <div>
          <vue-multiselect
            v-if="agencies.length > 0"
            v-model="$store.local.agency"
            :allowEmpty="false"
            :options="agencies"
            label="name"
          />
        </div>
        <template v-if="url_number_items?.length">
          /
          <vue-multiselect
            v-if="url_numbers?.length > 1"
            v-model="$store.local.url_number"
            :options="url_numbers"
            :searchable="false"
          />
        </template>
      </div>
      <unrest-auth-menu />
    </section>
  </header>
</template>

<script>
import VueMultiselect from 'vue-multiselect'
import { sortBy, range } from 'lodash'

import AgencyAlerts from '@/components/AgencyAlerts.vue'

export default {
  components: { AgencyAlerts, VueMultiselect },
  computed: {
    show_fields() {
      return this.$auth.user?.id && !this.$route.path.startsWith('/registration/')
    },
    agencies() {
      return sortBy(this.$auth.user?.agencies || [], a => a.name.toLowerCase())
    },
    dashboards() {
      return sortBy(this.$store.dashboard.getAll() || [], 'name')
    },
    agency_items() {
      const agencies = sortBy(this.$auth.user?.agencies || [], 'name')
      return agencies.map(agency => ({
        text: agency.name,
        click: () => this.$store.local.agency = agency,
      }))
    },
    url_numbers() {
      const { dashboard, agency } = this.$store.local
      return dashboard?.url_number && range(agency.url_count)
    }
  },
}
</script>

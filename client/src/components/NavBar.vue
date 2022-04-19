<template>
  <header class="navbar">
    <section class="navbar__section -left">
      <router-link class="navbar__brand" to="/">
        Agency Hub
      </router-link>
    </section>
    <section class="navbar__section -right">
      <unrest-dropdown v-if="agency_items?.length" :items="agency_items" class="btn -text">
        Agency: {{ $store.local.getActiveAgency().name }}
        <i class="fa fa-chevron-down" />
      </unrest-dropdown>
      <unrest-auth-menu />
    </section>
  </header>
</template>

<script>
export default {
  computed: {
    agency_items() {
      return this.$auth.user?.agencies.map(a => ({
        text: a.name,
        click: () => this.$store.local.setActiveAgency(a),
      }))
    },
  },
}
</script>

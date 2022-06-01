<template>
  <div class="navbar-notices" @click="open=true">
    <i :class="css.icon" />
    <div v-if="total" :class="css.badge">
      {{ total }}
    </div>
  </div>
  <unrest-modal v-if="open" @close="open=false">
    {{ message }}
    <table class="table table-striped" v-if="results?.feeds?.length > 1">
      <thead>
        <tr>
          <th>URL Number</th>
          <th>Errors</th>
          <th>Url</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="feed in results.feeds" :key="feed.url_number">
          <td>{{ feed.url_number }}</td>
          <td>{{ feed.notices }}</td>
          <td>{{ feed.raw_url }}</td>
        </tr>
      </tbody>
    </table>
  </unrest-modal>
</template>

<script>
import { sum } from 'lodash'

export default {
  data() {
    return { open: false }
  },
  computed: {
    results() {
      const { agency } = this.$store.local
      if (agency) {
        return this.$store.notices.watch(agency.id)
      }
      return null
    },
    total() {
      if (this.results && ! this.results.error) {
        return sum(this.results.feeds.map(r => r.notices))
      }
      return null
    },
    message() {
      if (!this.results) {
        return "Loading..."
      }
      if (this.results?.error) {
        return "An unknown error has occurred."
      }
      const count = this.total || 'no'
      return `There were ${ count } validation errors yesterday.`
    },
    css() {
      if (!this.results) {
        return { icon: "loader__spinner" }
      }
      console.log(this.results.error)
      if (this.results.error) {
        return { icon: 'fas fa-lg fa-exclamation-circle -red' }
      }
      const pass = this.total < 5
      const color = pass ? "green" : "red"
      return {
        icon: 'fas fa-lg fa-bell',
        badge: `navbar-notices__badge -${color}`,
      }
    }
  }
}
</script>
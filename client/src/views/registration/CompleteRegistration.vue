<template>
  <div class="modal -relative app__content">
    <div class="modal-content">
      <div v-if="error" class="alert -error">{{ error }}</div>
      <div v-else>
        Processing...
      </div>
    </div>
  </div>
</template>

<script>
import { getClient } from '@unrest/vue-storage'

export default {
  __route: {
    path: '/registration/complete/:activation_code/'
  },
  data() {
    return { error: null }
  },
  mounted() {
    const url = `registration/complete/${this.$route.params.activation_code}`
    getClient().get(url).then((response) => {
      if (response.success) {
        this.$auth.refetch().then(() => this.$router.replace('/registration/password/'))
      } else {
        this.error = response.error || "An unknown error has occurred"
      }
    })
  }
}
</script>

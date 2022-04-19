<template>
  <div class="app__one-card">
    <p>
      Please create a password to finish registration
    </p>
    <unrest-schema-form form_name="schema/first-password" :success="success" />
  </div>
</template>

<script>
export default {
  __route: {
    path: "/registration/password/",
  },
  methods: {
    success() {
      this.$ui.toast.success("Password set and registration complete!")
      this.$router.replace('/')
    }
  }
}
</script>

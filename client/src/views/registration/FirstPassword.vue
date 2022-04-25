<template>
  <div class="modal -relative app__content">
    <div class="modal-content">
      <p>
        Please create a password to finish registration
      </p>
      <unrest-schema-form form_name="schema/first-password" :success="success" />
    </div>
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

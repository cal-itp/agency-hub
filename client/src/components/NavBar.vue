<template>
  <header class="navbar">
    <section class="navbar__section -left">
      <router-link class="navbar__brand" to="/">
        Agency Hub
      </router-link>
    </section>
    <section class="navbar__section -right">
      <unrest-auth-menu />
    </section>
  </header>
</template>

<script>
export default {}
</script>
<template>
  <div class="app__wrapper">
    <nav-bar />
    <router-view class="app__content" />
    <unrest-ui />
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'

export default {
  components: { NavBar }
}
</script>

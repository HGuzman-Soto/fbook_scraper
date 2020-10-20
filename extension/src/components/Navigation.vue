<template>
  <header
    class="mdl-layout__header mdl-layout__header--scroll mdl-color--primary"
  >
    <div class="mdl-layout--large-screen-only mdl-layout__header-row"></div>
    <div class="mdl-layout--large-screen-only mdl-layout__header-row">
      <h3>Facebok Scraper Dashboard</h3>
    </div>
    <div class="mdl-layout--large-screen-only mdl-layout__header-row"></div>
    <div class="mdl-color--primary-dark" style="">
      <a
        href="#/"
        class="mdl-layout__tab"
        :class="{ 'is-active': $route.name === 'data' }"
        >Data</a
      >
    </div>
  </header>
</template>

<script>
export default {
  methods: {
    refresh() {
      window.location.reload();
    },
  },
};
</script>

<style lang="scss">
.mdl-layout__header {
  margin-bottom: 48px;
}

.mdl-layout__tab {
  padding-top: 10px;
  padding-bottom: 10px;
}
</style>

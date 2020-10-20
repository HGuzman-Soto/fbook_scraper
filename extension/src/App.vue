<template>
  <div class="mdl-layout mdl-js-layout mdl-layout--fixed-header">
    <Navigation></Navigation>
    <main class="mdl-layout__content">
      <router-view />
    </main>
  </div>
</template>

<script>
  import Navigation from './components/Navigation';

  export default {
    components: {
      Navigation
    }
  };
</script>
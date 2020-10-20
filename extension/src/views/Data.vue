<template>
  <div>
    <section class="section--center mdl-grid mdl-grid--no-spacing mdl-shadow--2dp">
      <div class="mdl-card mdl-cell mdl-cell--12-col-desktop">
        <div class="mdl-card__supporting-text">
          <h4>Data</h4>
        </div>
        <div class="mdl-card__actions">
          <a href="#" @click="reset" class="mdl-button">Reset Data</a>
        </div>

      <div>
        <div class="mdl-card__actions">
          <a href='#' @click="download" class="mdl-button">Download Data </a>
      </div>
    </section>
  </div>
</template>

<script>
  export default {
    methods: {
      async reset () {
        await drop ('threads');
        await drop ('vocab');
      },
      async download(){
        chrome.storage.local.get(["threads"], function(items) {

        var result = JSON.stringify(items);

        // Save as file
        var url =
          "data:application/json;base64," +
          btoa(unescape(encodeURIComponent(result)));
        chrome.downloads.download({
          url: url,
          filename: "threads.json",
        });
      });
      }
    }

  
  };
</script>
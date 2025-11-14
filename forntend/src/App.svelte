<script lang="ts">
  import Router from "svelte-spa-router";
  import Home from "./routes/Home.svelte";
  import History from "./routes/History.svelte";

  const routes = {
    "/": Home,
    "/history": History
  };
</script>

<Router {routes} />
<script lang="ts">
  import Router from "svelte-spa-router";
  import Home from "./routes/Home.svelte";
  import History from "./routes/History.svelte";
  import Create from "./routes/Create.svelte";
  
  const routes = {
    "/": Home,
    "/history": History,
    "/create": Create
  };
</script>

<Router {routes} />
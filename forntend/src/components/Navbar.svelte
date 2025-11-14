<script lang="ts">
  import { link } from "svelte-spa-router";
</script>

<nav class="bg-gradient-to-r from-blue-600 to-blue-800 shadow-lg">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-16">
      
      <div class="flex items-center">
        <svg class="w-8 h-8 text-white mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"></path>
        </svg>
        <span class="text-white text-xl font-bold">Weather Station</span>
      </div>
      
      <div class="flex items-center space-x-4">
        <a href="/" use:link class="text-blue-100 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Home</a>
        <a href="/history" use:link class="text-blue-100 hover:text-white px-3 py-2 rounded-md text-sm font-medium">History</a>
        <div class="flex items-center space-x-2">
          <span class="text-blue-100 text-sm">Live Data</span>
          <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
        </div>
      </div>
    </div>
  </div>
</nav>
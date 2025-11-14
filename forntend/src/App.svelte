<script lang="ts">
    import { onMount, onDestroy } from "svelte";

    interface WeatherData {
      temperature: number;
      humidity: number;
      pressure: number;
      timestamp: Date;
    }

    const apiUrl: string = "http://localhost:8000"
    let weatherData: WeatherData | null = null;
    let error: string | null = null;
    

    async function fetchWeatherData(): Promise<WeatherData> {
      const res = await fetch(`${apiUrl}/weather`);
      if (!res.ok) throw new Error("Network response was not ok");
      const data = await res.json();
      return {
        temperature: data.temperature,
        humidity: data.humidity,
        pressure: data.pressure,
        timestamp: new Date(data.timestamp),
      };
    }

    let intervalId: number;

    onMount(() => {
      fetchWeatherData()
        .then((data) => (weatherData = data))
        .catch((err) => (error = err.message));

      intervalId = setInterval(async () => {
        try {
          weatherData = await fetchWeatherData();

        } catch (err: any) {
          error = err.message;
        }
      }, 60000); // co 60 sekund
    });

    onDestroy(() => {
      clearInterval(intervalId);
    });
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
        <span class="text-blue-100 text-sm">Live Data</span>
        <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
      </div>
    </div>
  </div>
</nav>

<main class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    {#if error}
      <div class="bg-red-50 border-l-4 border-red-500 p-6 rounded-lg shadow-md">
        <div class="flex items-center">
          <svg class="w-6 h-6 text-red-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <p class="text-red-800 font-medium">Error: {error}</p>
        </div>
      </div>
    {:else if weatherData}
      <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
        <div class="bg-gradient-to-r from-blue-500 to-indigo-600 px-8 py-6">
          <h1 class="text-3xl font-bold text-white">Current Weather</h1>
          <p class="text-blue-100 mt-1">Real-time measurements from your weather station</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-8">
          <!-- Temperature Card -->
          <div class="bg-gradient-to-br from-orange-50 to-red-50 rounded-xl p-6 border border-orange-200">
            <div class="flex items-center justify-between mb-2">
              <span class="text-orange-600 font-medium">Temperature</span>
              <svg class="w-6 h-6 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
            <p class="text-4xl font-bold text-gray-800">{weatherData.temperature}<span class="text-2xl text-gray-600">°C</span></p>
          </div>

          <!-- Humidity Card -->
          <div class="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl p-6 border border-blue-200">
            <div class="flex items-center justify-between mb-2">
              <span class="text-blue-600 font-medium">Humidity</span>
              <svg class="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4"></path>
              </svg>
            </div>
            <p class="text-4xl font-bold text-gray-800">{weatherData.humidity}<span class="text-2xl text-gray-600">%</span></p>
          </div>

          <div class="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-6 border border-purple-200">
            <div class="flex items-center justify-between mb-2">
              <span class="text-purple-600 font-medium">Pressure</span>
              <svg class="w-6 h-6 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
            </div>
            <p class="text-4xl font-bold text-gray-800">{weatherData.pressure}<span class="text-2xl text-gray-600"> hPa</span></p>
          </div>
        </div>

        <div class="bg-gray-50 px-8 py-4 border-t border-gray-200">
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-600">Last Updated:</span>
            <span class="text-gray-800 font-medium">{weatherData.timestamp.toLocaleTimeString('pl-PL')}</span>
          </div>
        </div>
      </div>
    {:else}
      <div class="bg-white rounded-2xl shadow-xl p-12 text-center">
        <svg class="animate-spin h-12 w-12 text-blue-600 mx-auto mb-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="text-gray-600 text-lg">Loading weather data...</p>
      </div>
    {/if}
  </div>
</main>
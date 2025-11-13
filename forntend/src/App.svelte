<script lang="ts">
    import { onMount } from "svelte";

    interface WeatherData {
      temperature: number;
      humidity: number;
      pressure: number;
      timestamp: Date;
    }

    const apiUrl: string = "http://localhost:8000"
    let weatherData: WeatherData | null = null;
    let error: string | null = null;
    
    function fetchWeatherData(): Promise<weatherData> {
      return fetch(`${apiUrl}/weather`)
        .then((response) => {
          if (!response.ok) throw new Error("Network response was not ok");
          return response.json();
        })
        .then((data) => ({
          temperature: data.temperature,
          humidity: data.humidity,
          pressure: data.pressure,
          timestamp: new Date(data.timestamp),
        }));
    }

    onMount(async () => {
      try {
        weatherData = await fetchWeatherData();
      } catch (e: any) {
        error = e.message;
      }
    });
</script>

<main>
  {#if error}
    <p>Error: {error}</p>
  {:else if weatherData}
    <h1>Current Weather</h1>
    <p>Temperature: {weatherData.temperature} °C</p>
    <p>Humidity: {weatherData.humidity} %</p>
    <p>Pressure: {weatherData.pressure} hPa</p>
    <p>Last Updated: {weatherData.timestamp.toLocaleString()}</p>
  {:else}
    <p>Loading weather data...</p>
    
  {/if}
</main>

<style>
main {
    font-family: sans-serif;
    padding: 1em;
  }
</style>

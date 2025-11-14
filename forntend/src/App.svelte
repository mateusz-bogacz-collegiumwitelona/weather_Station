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

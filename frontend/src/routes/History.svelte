<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import Navbar from "../components/Navbar.svelte";
    import type { WeatherData } from "../types/weather";
    import { API_URL } from "../config";
    
    const apiUrl: string = `${API_URL}/history`;
    let weatherData: WeatherData[] = [];
    let error: string | null = null;
    let loading: boolean = true;
    let intervalId: number;

    async function fetchWeatherHistory(): Promise<WeatherData[]> {
        const res = await fetch(`${apiUrl}`);
        if (!res.ok) throw new Error("Network response was not ok");
        const data: WeatherData[] = await res.json();

        return data.map(item => ({
            temperature: item.temperature,
            humidity: item.humidity,
            pressure: item.pressure,
            timestamp: new Date(item.timestamp)
        }));
    }

    function formatDate(date: Date): string {
        return date.toLocaleDateString('pl-PL', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
        });
    }

    function formatTime(date: Date): string {
        return date.toLocaleTimeString('pl-PL', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    }

    onMount(() => {
        fetchWeatherHistory()
            .then((data) => {
                weatherData = data;
                loading = false;
            })
            .catch((err) => {
                error = err.message;
                loading = false;
            });

        intervalId = setInterval(async () => {
            try {
                weatherData = await fetchWeatherHistory();
            } catch (err: any) {
                error = err.message;
            }
        }, 60000);
    });

    onDestroy(() => {
        clearInterval(intervalId);
    });
</script>

<Navbar />

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
        {:else if loading}
            <div class="bg-white rounded-2xl shadow-xl p-12 text-center">
                <svg class="animate-spin h-12 w-12 text-blue-600 mx-auto mb-4" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <p class="text-gray-600 text-lg">Loading weather history...</p>
            </div>
        {:else if weatherData.length === 0}
            <div class="bg-yellow-50 border-l-4 border-yellow-500 p-6 rounded-lg shadow-md">
                <div class="flex items-center">
                    <svg class="w-6 h-6 text-yellow-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                    </svg>
                    <p class="text-yellow-800 font-medium">No historical data available</p>
                </div>
            </div>
        {:else}
            <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
                <div class="bg-gradient-to-r from-blue-500 to-indigo-600 px-8 py-6">
                    <h1 class="text-3xl font-bold text-white">Weather History</h1>
                    <p class="text-blue-100 mt-1">Historical measurements from your weather station</p>
                </div>
                
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                                    Date
                                </th>
                                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                                    Time
                                </th>
                                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                                    Temperature
                                </th>
                                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                                    Humidity
                                </th>
                                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                                    Pressure
                                </th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            {#each weatherData as item, i}
                                <tr class="hover:bg-blue-50 transition-colors duration-150 {i % 2 === 0 ? 'bg-white' : 'bg-gray-50'}">
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 font-medium">
                                        {formatDate(item.timestamp)}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                                        {formatTime(item.timestamp)}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="flex items-center">
                                            <div class="bg-gradient-to-br from-orange-50 to-red-50 rounded-lg px-3 py-1 border border-orange-200">
                                                <span class="text-sm font-semibold text-gray-800">
                                                    {item.temperature.toFixed(1)}<span class="text-xs text-gray-600">°C</span>
                                                </span>
                                            </div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="flex items-center">
                                            <div class="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-lg px-3 py-1 border border-blue-200">
                                                <span class="text-sm font-semibold text-gray-800">
                                                    {item.humidity.toFixed(1)}<span class="text-xs text-gray-600">%</span>
                                                </span>
                                            </div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="flex items-center">
                                            <div class="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg px-3 py-1 border border-purple-200">
                                                <span class="text-sm font-semibold text-gray-800">
                                                    {item.pressure.toFixed(0)}<span class="text-xs text-gray-600"> hPa</span>
                                                </span>
                                            </div>
                                        </div>
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
                
                <div class="bg-gray-50 px-8 py-4 border-t border-gray-200">
                    <div class="flex items-center justify-between text-sm">
                        <span class="text-gray-600">Total Records:</span>
                        <span class="text-gray-800 font-medium">{weatherData.length}</span>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</main>
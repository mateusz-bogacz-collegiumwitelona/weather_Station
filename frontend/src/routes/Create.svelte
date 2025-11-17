<script lang="ts">
  import Navbar from "../components/Navbar.svelte";
</script>

<Navbar />

<main class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-16">

    <div class="bg-white rounded-2xl shadow-xl p-10 space-y-6">

      <h1 class="text-3xl font-bold text-gray-800 text-center">
        About This Project
      </h1>

      <p class="text-gray-700 text-lg text-center">
        Weather Station Dashboard — Version 1.1
      </p>

      <div class="border-t border-gray-200 pt-6 space-y-6">

        <div>
          <h2 class="text-xl font-semibold text-gray-800">Author</h2>
          <p class="text-gray-700">Mateusz Bogacz-Drewniak</p>
        </div>

        <div>
          <h2 class="text-xl font-semibold text-gray-800">Project Purpose</h2>
          <p class="text-gray-700">
            Aplikacja wykonana na zaliczenie przedmiotu „Techniki mikroprocesorowe i systemy wbudowane”.
            Projekt prezentuje dane pogodowe pobierane w czasie rzeczywistym z własnej stacji meteo
            opartej na Raspberry Pi oraz czujniku BME280.
          </p>
        </div>

        <div>
          <h2 class="text-xl font-semibold text-gray-800">Technologies Used</h2>
          <ul class="list-disc pl-6 text-gray-700">
            <li>Svelte</li>
            <li>TailwindCSS</li>
            <li>FastAPI (Python backend)</li>
            <li>SQLite</li>
            <li>Raspberry Pi 4B 4GB</li>
            <li>Czujnik BME280 (I2C)</li>
          </ul>
        </div>

        <div>
          <h2 class="text-xl font-semibold text-gray-800">Hardware Requirements</h2>
          <ul class="list-disc pl-6 text-gray-700">
            <li>Raspberry Pi z Raspberry Pi OS</li>
            <li>Czujnik BME280</li>
            <li>Kable połączeniowe</li>
            <li>Płytka prototypowa</li>
          </ul>
        </div>

        <div>
          <h2 class="text-xl font-semibold text-gray-800">Software Requirements</h2>
          <ul class="list-disc pl-6 text-gray-700">
            <li>Python</li>
            <li>Node.js + npm</li>
          </ul>
        </div>

        <div>
          <h2 class="text-xl font-semibold text-gray-800">BME280 Wiring</h2>
          <p class="text-gray-700 mb-2">Schemat podłączeń (I2C):</p>

          <table class="w-full text-left border border-gray-300 text-gray-700">
            <thead>
              <tr class="bg-gray-100">
                <th class="p-2 border">Raspberry Pi GPIO</th>
                <th class="p-2 border">BME280</th>
              </tr>
            </thead>

            <tbody>
              <tr>
                <td class="p-2 border">17 (3.3V)</td>
                <td class="p-2 border">Vin</td>
              </tr>
              <tr>
                <td class="p-2 border">6 (GND)</td>
                <td class="p-2 border">GND</td>
              </tr>
              <tr>
                <td class="p-2 border">3 (SDA)</td>
                <td class="p-2 border">SDA (SDI)</td>
              </tr>
              <tr>
                <td class="p-2 border">5 (SCL)</td>
                <td class="p-2 border">SCL (SDK)</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div>
          <h2 class="text-xl font-semibold text-gray-800">Version</h2>
          <p class="text-gray-700">1.1 — last updated: 2025-11-17</p>
        </div>

        <div>
          <h2 class="text-xl font-semibold text-gray-800">Contact</h2>
          <p class="text-gray-700">
            Email: <span class="font-medium">mateusz.bogacz-drewniak@studenci.collegiumwitelona.pl</span><br />
            GitHub: <span class="font-medium">https://github.com/mateusz-bogacz-collegiumwitelona</span>          </p>
        </div>

      </div>

    </div>

  </div>
</main>

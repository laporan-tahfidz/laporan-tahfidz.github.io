<script>
    import { onMount, onDestroy } from 'svelte';
    import { browser } from '$app/environment';
    import { getPhpBackendBaseUrl } from '$lib/utils.js';
    import {
        Chart as ChartJS,
        LineController,
        LineElement,
        PointElement,
        LinearScale,
        TimeScale,
        Title,
        Tooltip,
        Legend
    } from 'chart.js';
    import 'chartjs-adapter-date-fns';

    // Register the components
    ChartJS.register(
        LineController,
        LineElement,
        PointElement,
        LinearScale,
        TimeScale,
        Title,
        Tooltip,
        Legend
    );

    let { className = '' } = $props();
    let isLoading = $state(true);
    let activeTab = $state('ziyadah'); // Default to ziyadah
    let chartData = $state({
        ziyadah: [],
        setengah_juz: [],
        juziyah: [],
        syahadah: []
    });
    let chartInstance = null;
    let chartCanvas;

    // Generate dates for the current year (Jan 1 to Dec 31)
    function generateDateRange() {
        const year = new Date().getFullYear();
        const startDate = new Date(year, 0, 1); // January 1
        const endDate = new Date(year, 11, 31); // December 31

        const dates = [];
        const currentDate = new Date(startDate);

        while (currentDate <= endDate) {
            dates.push({
                x: currentDate.toISOString().split('T')[0], // Format to YYYY-MM-DD
                y: 0 // Placeholder, will be filled with actual values
            });
            currentDate.setDate(currentDate.getDate() + 1);
        }

        return dates;
    }

    onMount(async () => {
        if (browser) {
            await loadAchievementData();
        } else {
            isLoading = false;
        }
    });

    async function loadAchievementData() {
        try {
            const token = localStorage.getItem('tokenSuper') || '';

            const response = await fetch(`${getPhpBackendBaseUrl()}/get-achievement-statistics.php`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ token })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();

            if (result.success) {
                // Debug: Log the received data
                console.log('Received achievement data:', result.data);

                // Process the data for each achievement type
                chartData.ziyadah = processAchievementData(result.data.ziyadah || []);
                chartData.setengah_juz = processAchievementData(result.data['setengah_juz'] || []);
                chartData.juziyah = processAchievementData(result.data.juziyah || []);
                chartData.syahadah = processAchievementData(result.data.syahadah || []);

                // Debug: Log the processed data
                console.log('Processed ziyadah data:', chartData.ziyadah.slice(0, 5)); // First 5 entries
                console.log('Processed setengah_juz data:', chartData.setengah_juz.slice(0, 5));
                console.log('Processed juziyah data:', chartData.juziyah.slice(0, 5));
                console.log('Processed syahadah data:', chartData.syahadah.slice(0, 5));
            } else {
                console.error('Failed to load achievement data:', result.message);
            }
        } catch (error) {
            console.error('Error loading achievement data:', error);
        } finally {
            isLoading = false;
            // Initialize or update the chart after loading data
            setTimeout(() => {
                safeInitializeChart();
            }, 0);
        }
    }

    function processAchievementData(rawData) {
        // Debug: Log the raw data
        console.log('Processing raw data:', rawData);

        // Generate date range for the full year (Jan 1 to Dec 31)
        const dateRange = generateDateRange();

        // If no raw data, return the date range with all zeros
        if (!rawData || rawData.length === 0) {
            // Return date range with zero values
            return dateRange.map(dateObj => ({
                x: dateObj.x,
                y: 0
            }));
        }

        // Convert raw data to a map for quick lookup
        const dataMap = new Map();
        rawData.forEach(item => {
            // Ensure the date is in the correct format
            const date = new Date(item.date).toISOString().split('T')[0]; // Format to YYYY-MM-DD
            dataMap.set(date, parseInt(item.total));
        });

        // Debug: Log the data map
        console.log('Data map:', Object.fromEntries(dataMap));

        // Create daily data for each date in the range
        const processedData = dateRange.map(dateObj => {
            const dateStr = dateObj.x; // The date string in YYYY-MM-DD format
            const dailyValue = dataMap.has(dateStr) ? dataMap.get(dateStr) : 0;

            return {
                x: dateStr, // Using string format for Chart.js compatibility
                y: dailyValue
            };
        });

        // Debug: Log the first few processed entries
        console.log('First 5 processed entries:', processedData.slice(0, 5));

        return processedData;
    }

    function setActiveTab(tab) {
        activeTab = tab;
        setTimeout(() => {
            updateChart();
        }, 0);
    }

    function getTabLabel(tab) {
        switch(tab) {
            case 'ziyadah': return 'Ziyadah';
            case 'setengah_juz': return 'Setengah Juz';
            case 'juziyah': return 'Juziyah';
            case 'syahadah': return 'Syahadah';
            default: return tab;
        }
    }

    function getTabColor(tab) {
        switch(tab) {
            case 'ziyadah': return '#3b82f6'; // blue-500
            case 'setengah_juz': return '#10b981'; // green-500
            case 'juziyah': return '#f59e0b'; // yellow-500
            case 'syahadah': return '#8b5cf6'; // violet-500
            default: return '#6b7280'; // gray-500
        }
    }

    function initializeChart() {
        if (chartInstance) {
            chartInstance.destroy();
        }

        if (chartCanvas) {
            const ctx = chartCanvas.getContext('2d');

            // Check if chartData for the active tab has data
            const hasData = chartData[activeTab] && chartData[activeTab].length > 0;

            chartInstance = new ChartJS(ctx, {
                type: 'line',
                data: {
                    datasets: [{
                        label: getTabLabel(activeTab),
                        data: hasData ? [...chartData[activeTab]] : [], // Create a copy to avoid Svelte state issues
                        borderColor: getTabColor(activeTab),
                        backgroundColor: `${getTabColor(activeTab)}20`, // 20% opacity
                        borderWidth: 2,
                        tension: 0.4,
                        fill: false,
                        pointRadius: 0, // Hide points by default
                        pointHoverRadius: 6, // Show points on hover
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false
                        }
                    },
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'month',
                                tooltipFormat: 'dd MMM yyyy'
                            },
                            grid: {
                                display: false
                            }
                        },
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: 'rgba(0, 0, 0, 0.1)'
                            }
                        }
                    },
                    interaction: {
                        mode: 'nearest',
                        axis: 'x',
                        intersect: false
                    }
                }
            });
        }
    }

    function updateChart() {
        if (chartInstance) {
            chartInstance.data.datasets[0].label = getTabLabel(activeTab);
            chartInstance.data.datasets[0].data = [...(chartData[activeTab] || [])]; // Create a copy to avoid Svelte state issues
            chartInstance.data.datasets[0].borderColor = getTabColor(activeTab);
            chartInstance.data.datasets[0].backgroundColor = `${getTabColor(activeTab)}20`;
            chartInstance.update();
        } else {
            initializeChart();
        }
    }

    // Clean up the chart instance when component is destroyed
    onDestroy(() => {
        if (chartInstance) {
            chartInstance.destroy();
            chartInstance = null;
        }
    });

    // Function to safely initialize chart when canvas is available
    function safeInitializeChart() {
        if (chartCanvas && !isLoading) {
            initializeChart();
        }
    }
</script>

<div class={className}>
    <div class="bg-white rounded-xl shadow p-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-6">Statistik Pencapaian Santri</h2>

        {#if isLoading}
            <div class="flex justify-center items-center py-12">
                <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
            </div>
        {:else}
            <!-- Tabs for Achievement Types -->
            <div class="border-b border-gray-200 mb-6">
                <nav class="-mb-px flex space-x-8 overflow-x-auto py-2">
                    {#each [
                        { id: 'ziyadah', label: 'Ziyadah' },
                        { id: 'setengah_juz', label: 'Setengah Juz' },
                        { id: 'juziyah', label: 'Juziyah' },
                        { id: 'syahadah', label: 'Syahadah' }
                    ] as tab}
                        <button
                            type="button"
                            class={`whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm ${
                                activeTab === tab.id
                                    ? 'border-blue-500 text-blue-600'
                                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                            }`}
                            onclick={() => setActiveTab(tab.id)}
                        >
                            {tab.label}
                        </button>
                    {/each}
                </nav>
            </div>

            <!-- Chart Container -->
            <div class="h-80 w-full">
                <canvas bind:this={chartCanvas}></canvas>
            </div>
        {/if}
    </div>
</div>
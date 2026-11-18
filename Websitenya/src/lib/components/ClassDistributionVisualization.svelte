<script>
    import { cn } from '$lib/utils.js';

    // Props using $props() for Svelte 5 runes mode
    let {
        distribution = {
            'Kelas 1': 0,
            'Kelas 2': 0,
            'Kelas 3': 0,
            'Lainnya': 0
        },
        className = ''
    } = $props();

    // Calculate total students
    let totalStudents = $derived(Object.values(distribution).reduce((sum, count) => sum + count, 0));

    // Calculate percentages
    let percentages = $derived(() => {
        const result = {};
        for (const [className, count] of Object.entries(distribution)) {
            result[className] = totalStudents > 0 ? Math.round((count / totalStudents) * 100) : 0;
        }
        return result;
    });
</script>

<div class={cn('w-full', className)}>
    <h3 class="text-lg font-semibold text-gray-800 mb-4">Distribusi Kelas Santri</h3>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {#each Object.entries(distribution) as [className, count]}
            <div class="bg-white rounded-xl shadow p-4 border-l-4 
                {className === 'Kelas 1' ? 'border-blue-500' : 
                 className === 'Kelas 2' ? 'border-green-500' : 
                 className === 'Kelas 3' ? 'border-purple-500' : 
                 'border-gray-500'}">
                <div class="text-sm font-medium text-gray-500">{className}</div>
                <div class="flex items-baseline mt-1">
                    <div class="text-2xl font-bold text-gray-900">{count}</div>
                    <div class="ml-2 text-sm text-gray-500">santri ({percentages[className]}%)</div>
                </div>
                <div class="mt-2 w-full bg-gray-200 rounded-full h-2">
                    <div 
                        class="h-2 rounded-full 
                        {className === 'Kelas 1' ? 'bg-blue-500' : 
                         className === 'Kelas 2' ? 'bg-green-500' : 
                         className === 'Kelas 3' ? 'bg-purple-500' : 
                         'bg-gray-500'}" 
                        style="width: {percentages[className]}%"
                    ></div>
                </div>
            </div>
        {/each}
    </div>

    <!-- Detailed Chart Visualization -->
    <div class="bg-white rounded-xl shadow p-6">
        <h4 class="font-medium text-gray-800 mb-4">Visualisasi Distribusi</h4>
        
        <div class="space-y-4">
            {#each Object.entries(distribution) as [className, count]}
                <div>
                    <div class="flex justify-between mb-1">
                        <span class="text-sm font-medium text-gray-700">{className}</span>
                        <span class="text-sm font-medium text-gray-700">{count} santri ({percentages[className]}%)</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-6">
                        <div 
                            class="h-6 rounded-full leading-6 text-center text-xs font-medium text-white
                            {className === 'Kelas 1' ? 'bg-blue-500' : 
                             className === 'Kelas 2' ? 'bg-green-500' : 
                             className === 'Kelas 3' ? 'bg-purple-500' : 
                             'bg-gray-500'}" 
                            style="width: {percentages[className]}%"
                        >
                            {percentages[className]}%
                        </div>
                    </div>
                </div>
            {/each}
        </div>
        
        <div class="mt-6 pt-4 border-t border-gray-200">
            <div class="flex justify-between items-center">
                <div class="text-lg font-semibold text-gray-800">Total Santri</div>
                <div class="text-2xl font-bold text-blue-600">{totalStudents}</div>
            </div>
        </div>
    </div>
</div>
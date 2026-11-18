<script>
    import { onMount } from 'svelte';

    let { selectedDate, onDateSelect } = $props();
    let currentDate = $state(new Date());
    let selected = $state(selectedDate ? new Date(selectedDate) : null);

    // Update selected date when prop changes
    $effect(() => {
        if (selectedDate) {
            selected = new Date(selectedDate);
        }
    });

    // Get days in month
    const getDaysInMonth = (year, month) => {
        return new Date(year, month + 1, 0).getDate();
    };

    // Get first day of month (0 = Sunday, 1 = Monday, etc.)
    const getFirstDayOfMonth = (year, month) => {
        return new Date(year, month, 1).getDay();
    };

    // Navigate to previous month
    const prevMonth = () => {
        currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1);
    };

    // Navigate to next month
    const nextMonth = () => {
        currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1);
    };

    // Format month and year for display
    const formatMonthYear = (date) => {
        const options = { month: 'long', year: 'numeric' };
        return date.toLocaleDateString('id-ID', options);
    };

    // Check if a date is the selected date
    const isSelected = (day) => {
        if (!selected) return false;
        return (
            day === selected.getDate() &&
            currentDate.getMonth() === selected.getMonth() &&
            currentDate.getFullYear() === selected.getFullYear()
        );
    };

    // Handle date selection
    const selectDate = (day) => {
        // Create date in local timezone to avoid timezone offset issues
        const newDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), day, 12, 0, 0, 0); // Set to noon to avoid DST issues
        selected = newDate;
        if (onDateSelect) {
            onDateSelect(newDate);
        }
    };

    // Days of the week in Indonesian
    const daysOfWeek = ['Min', 'Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab'];
</script>

<div class="custom-calendar">
    <div class="calendar-header flex items-center justify-between mb-2">
        <button 
            class="p-1 rounded hover:bg-gray-100"
            on:click={prevMonth}
            aria-label="Previous month"
        >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
        </button>
        
        <h3 class="font-medium text-gray-800">{formatMonthYear(currentDate)}</h3>
        
        <button 
            class="p-1 rounded hover:bg-gray-100"
            on:click={nextMonth}
            aria-label="Next month"
        >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
            </svg>
        </button>
    </div>

    <div class="grid grid-cols-7 gap-1 mb-1">
        {#each daysOfWeek as day}
            <div class="text-center text-xs font-medium text-gray-500 py-1">{day}</div>
        {/each}
    </div>

    <div class="grid grid-cols-7 gap-1">
        {#each Array.from({ length: getFirstDayOfMonth(currentDate.getFullYear(), currentDate.getMonth()) }, (_, i) => null) as _, i}
            <div class="h-8"></div>
        {/each}

        {#each Array.from({ length: getDaysInMonth(currentDate.getFullYear(), currentDate.getMonth()) }, (_, i) => i + 1) as day}
            <button
                class="h-8 w-8 text-sm rounded-full flex items-center justify-center hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                class:selected={isSelected(day)}
                on:click={() => selectDate(day)}
                aria-label={"Select " + day + " " + formatMonthYear(currentDate)}
            >
                {day}
            </button>
        {/each}
    </div>
</div>

<style>
    .selected {
        background-color: #3b82f6;
        color: white;
    }
</style>
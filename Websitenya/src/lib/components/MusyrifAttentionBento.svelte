<script>
    import AttentionBento from './AttentionBento.svelte';
    let { className = '' } = $props();
</script>

<AttentionBento
    {className}
    title="Perlu Perhatian Musyrif"
    description="Daftar santri yang membutuhkan perhatian khusus dari musyrif"
    attentionType="musyrif"
/>
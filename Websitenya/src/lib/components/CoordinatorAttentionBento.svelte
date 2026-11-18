<script>
    import AttentionBento from './AttentionBento.svelte';
    let { className = '' } = $props();
</script>

<AttentionBento
    {className}
    title="Perlu Perhatian Koordinator Tahfidz"
    description="Daftar santri yang membutuhkan perhatian khusus dari koordinator tahfidz"
    attentionType="coordinator"
/>
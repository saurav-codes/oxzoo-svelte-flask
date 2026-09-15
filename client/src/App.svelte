<script>
  import { onMount } from "svelte";

  // Baked at BUILD time: vite replaces import.meta.env.GREETING_TAG with a
  // string literal and esbuild folds this single expression into one bundle
  // literal. Keep the whole line in this one expression.
  const frontendLine =
    "frontend: hello world oxzoo-svelte-flask_" + import.meta.env.GREETING_TAG;

  let backendLine = $state("");
  let status = $state("loading");

  onMount(async () => {
    try {
      const res = await fetch("/api/greeting");
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      backendLine = await res.text();
      status = "ready";
    } catch {
      status = "error";
    }
  });
</script>

<main>
  <h1>oxzoo-svelte-flask</h1>
  <p class="line" id="frontend-line">{frontendLine}</p>
  <p class="line" id="backend-line">
    {#if status === "loading"}
      backend: loading...
    {:else if status === "error"}
      backend: error: could not reach /api/greeting
    {:else}
      backend: {backendLine}
    {/if}
  </p>
</main>

<style>
  main {
    font-family: system-ui, sans-serif;
    max-width: 40rem;
    margin: 3rem auto;
    padding: 0 1rem;
  }
  h1 {
    font-size: 1.25rem;
  }
  .line {
    font-family: ui-monospace, monospace;
  }
</style>

// Capacidades operativas del HUD web.
(() => {
    'use strict';

    const API = window.location.origin;
    let orchestrationPollTimer = null;

    const byId = (id) => document.getElementById(id);
    const pretty = (value) => JSON.stringify(value ?? null, null, 2);
    const escapeHtml = (value) => String(value ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');

    async function fetchJson(path, options = {}) {
        const response = await fetch(`${API}${path}`, options);
        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
            throw new Error(data.detail || data.error || `HTTP ${response.status}`);
        }
        return data;
    }

    function renderCards(containerId, entries) {
        const container = byId(containerId);
        if (!container) return;
        container.innerHTML = entries.map(([label, value]) => `
            <div class="admin-card">
                <div class="admin-label">${escapeHtml(label)}</div>
                <div class="admin-value">${escapeHtml(value)}</div>
            </div>
        `).join('');
    }

    function setLoading(elementId, message = 'Cargando...') {
        const element = byId(elementId);
        if (element) element.textContent = message;
    }

    // MEMORY — GET /api/memory
    async function loadMemory(selectedKey = '') {
        setLoading('memory-value');
        try {
            const query = new URLSearchParams({ history_limit: '15' });
            if (selectedKey) query.set('key', selectedKey);
            const data = await fetchJson(`/api/memory?${query}`);
            const status = data.status || {};
            renderCards('memory-status', [
                ['Estado', status.running ? 'RUNNING' : 'STOPPED'],
                ['Ruta', status.path || '-'],
                ['Claves', status.key_count ?? 0],
                ['Ejecuciones', status.history_count ?? 0],
            ]);

            const select = byId('memory-key-select');
            const previous = selectedKey || select.value;
            select.innerHTML = '<option value="">-- Seleccionar clave --</option>';
            (data.keys || []).forEach((key) => {
                const option = document.createElement('option');
                option.value = key;
                option.textContent = key;
                select.appendChild(option);
            });
            if ((data.keys || []).includes(previous)) select.value = previous;

            byId('memory-value').textContent = selectedKey ? pretty(data.value) : 'Seleccioná una clave.';
            byId('memory-latest').textContent = data.latest ? pretty(data.latest) : 'Sin ejecuciones registradas.';

            const history = data.history || [];
            byId('memory-history').innerHTML = history.length ? `
                <table class="admin-table">
                    <thead><tr><th>ID</th><th>Modo</th><th>Estado</th><th>Agentes</th><th>Duración</th></tr></thead>
                    <tbody>${history.map((row) => `
                        <tr>
                            <td>${escapeHtml((row.execution_id || '-').slice(0, 8))}</td>
                            <td>${escapeHtml(row.mode || '-')}</td>
                            <td>${row.success ? 'OK' : 'ERROR'}</td>
                            <td>${escapeHtml((row.agents || []).join(', '))}</td>
                            <td>${escapeHtml(Number(row.duration_ms || 0).toFixed(1))} ms</td>
                        </tr>`).join('')}</tbody>
                </table>` : '<div class="admin-status">Sin historial.</div>';
        } catch (error) {
            byId('memory-value').textContent = `Error: ${error.message}`;
        }
    }

    // LOGS — GET /api/logs
    async function loadLogs() {
        const lines = Math.max(20, Math.min(500, Number(byId('logs-lines').value) || 80));
        ['logs-runtime', 'logs-warnings', 'logs-errors'].forEach((id) => setLoading(id));
        try {
            const data = await fetchJson(`/api/logs?lines=${lines}`);
            byId('logs-path').textContent = data.path || '';
            byId('logs-runtime').textContent = (data.lines || []).join('\n') || 'Sin logs.';
            byId('logs-warnings').textContent = (data.warnings || []).join('\n') || 'Sin warnings.';
            byId('logs-errors').textContent = (data.errors || []).join('\n') || 'Sin errores.';
            const events = data.events || [];
            byId('logs-events').innerHTML = events.length ? `
                <table class="admin-table"><thead><tr><th>Hora</th><th>Tipo</th><th>Evento</th></tr></thead>
                <tbody>${events.slice().reverse().map((event) => `
                    <tr><td>${escapeHtml(event.timestamp || '-')}</td><td>${escapeHtml(event.kind || '-')}</td><td>${escapeHtml(event.message || '')}</td></tr>
                `).join('')}</tbody></table>` : '<div class="admin-status">Sin eventos.</div>';
        } catch (error) {
            byId('logs-runtime').textContent = `Error: ${error.message}`;
        }
    }

    // HYBRID — GET /api/status?full=true
    async function loadHybrid() {
        setLoading('hybrid-reason', 'Ejecutando diagnóstico...');
        try {
            const data = await fetchJson('/api/status?full=true');
            const hybrid = data.hybrid || {};
            renderCards('hybrid-status', [
                ['Modo', hybrid.execution_mode || '-'],
                ['Origen', hybrid.provider_origin || hybrid.source || '-'],
                ['Provider', hybrid.active_provider || '-'],
                ['Modelo', hybrid.active_model || '-'],
                ['Política', hybrid.policy || '-'],
                ['SAFE', hybrid.safe_mode ? 'SÍ' : 'NO'],
                ['Online', hybrid.online === null || hybrid.online === undefined ? '-' : (hybrid.online ? 'SÍ' : 'NO')],
                ['Estado', hybrid.connectivity_state || '-'],
            ]);
            byId('hybrid-reason').textContent = hybrid.routing_reason || hybrid.last_route?.reason || 'Sin decisión registrada.';
            byId('hybrid-connectivity').textContent = pretty(hybrid.connectivity || { state: hybrid.connectivity_state, online: hybrid.online });
            byId('hybrid-metrics').textContent = pretty(hybrid.metrics_summary || {});
        } catch (error) {
            byId('hybrid-reason').textContent = `Error: ${error.message}`;
        }
    }

    // ORCHESTRATION — POST /api/debate/start + GET /api/debate/{id}
    async function loadOrchestrationAgents() {
        const container = byId('orchestration-agents');
        container.textContent = 'Cargando agentes...';
        try {
            const data = await fetchJson('/api/agents/list');
            const agents = data.agents || [];
            container.innerHTML = agents.map((agent) => `
                <label class="admin-agent-option">
                    <input type="checkbox" value="${escapeHtml(agent.id)}" checked>
                    ${escapeHtml(agent.id)} <span class="admin-label">[${escapeHtml(agent.role || '-')}]</span>
                </label>
            `).join('') || '<div class="admin-status">No hay agentes.</div>';
        } catch (error) {
            container.textContent = `Error: ${error.message}`;
        }
    }

    function renderOrchestrationResult(result) {
        byId('orchestration-status').textContent = `${result.success ? 'COMPLETADO' : 'FINALIZADO CON ERRORES'} · ${Number(result.duration_ms || 0).toFixed(1)} ms · ${result.execution_id || '-'}`;
        byId('orchestration-scores').textContent = pretty(result.scores_summary || {});
        const steps = result.steps || [];
        byId('orchestration-steps').innerHTML = steps.map((step) => `
            <details class="admin-step ${step.success ? '' : 'error'}">
                <summary>${escapeHtml(step.agent_name || 'unknown')} · ${step.success ? 'OK' : 'ERROR'} · ${Number(step.duration_ms || 0).toFixed(1)} ms · score=${escapeHtml(step.score ?? '-')}</summary>
                ${step.error ? `<pre class="admin-pre">${escapeHtml(step.error)}</pre>` : ''}
                ${step.output ? `<pre class="admin-pre">${escapeHtml(step.output)}</pre>` : ''}
            </details>
        `).join('') || '<div class="admin-status">Sin pasos.</div>';
    }

    async function pollOrchestration(id) {
        try {
            const data = await fetchJson(`/api/debate/${encodeURIComponent(id)}`);
            byId('orchestration-status').textContent = `${String(data.status || '').toUpperCase()} · ${id}`;
            if (data.status === 'complete') {
                clearTimeout(orchestrationPollTimer);
                orchestrationPollTimer = null;
                renderOrchestrationResult(data.result || {});
                byId('orchestration-run-btn').disabled = false;
                return;
            }
            if (data.status === 'error') {
                throw new Error(data.error || 'La ejecución falló');
            }
            orchestrationPollTimer = setTimeout(() => pollOrchestration(id), 1500);
        } catch (error) {
            byId('orchestration-status').textContent = `ERROR · ${error.message}`;
            byId('orchestration-run-btn').disabled = false;
            orchestrationPollTimer = null;
        }
    }

    async function runOrchestration() {
        const task = byId('orchestration-task').value.trim();
        const mode = byId('orchestration-mode').value;
        const agents = [...document.querySelectorAll('#orchestration-agents input:checked')].map((input) => input.value);
        if (!task) {
            byId('orchestration-status').textContent = 'Ingresá una tarea.';
            return;
        }
        if (!agents.length) {
            byId('orchestration-status').textContent = 'Seleccioná al menos un agente.';
            return;
        }

        byId('orchestration-run-btn').disabled = true;
        byId('orchestration-status').textContent = 'ENCOLANDO...';
        byId('orchestration-scores').textContent = 'Esperando resultados...';
        byId('orchestration-steps').innerHTML = '';
        try {
            const data = await fetchJson('/api/debate/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task, mode, agents }),
            });
            pollOrchestration(data.debate_id);
        } catch (error) {
            byId('orchestration-status').textContent = `ERROR · ${error.message}`;
            byId('orchestration-run-btn').disabled = false;
        }
    }

    // OVERVIEW — GET /api/status
    async function loadOverview() {
        try {
            const data = await fetchJson('/api/status');
            const overview = data.overview || {};
            renderCards('overview-status', [
                ['Supervisor', data.running ? 'ONLINE' : 'OFFLINE'],
                ['Uptime', `${Number(overview.uptime_s || 0).toFixed(1)} s`],
                ['Agentes', overview.agent_count ?? 0],
                ['Providers', overview.provider_count ?? 0],
                ['Herramientas', overview.tool_count ?? 0],
                ['Ejecuciones', overview.orchestrations ?? 0],
                ['Despachos', overview.agent_dispatches ?? 0],
                ['Última latencia', `${Number(overview.last_orchestration_ms || 0).toFixed(1)} ms`],
            ]);
            byId('overview-tools').textContent = (overview.tools || []).join('\n') || 'Sin herramientas cargadas.';
            byId('overview-memory').textContent = pretty(overview.memory || {});
        } catch (error) {
            byId('overview-memory').textContent = `Error: ${error.message}`;
        }
    }

    const loaders = {
        memory: () => loadMemory(byId('memory-key-select').value),
        logs: loadLogs,
        hybrid: loadHybrid,
        orchestration: loadOrchestrationAgents,
        overview: loadOverview,
    };

    function initialize() {
        byId('memory-refresh-btn')?.addEventListener('click', () => loadMemory(byId('memory-key-select').value));
        byId('memory-key-select')?.addEventListener('change', (event) => loadMemory(event.target.value));
        byId('logs-refresh-btn')?.addEventListener('click', loadLogs);
        byId('hybrid-refresh-btn')?.addEventListener('click', loadHybrid);
        byId('orchestration-run-btn')?.addEventListener('click', runOrchestration);
        byId('overview-refresh-btn')?.addEventListener('click', loadOverview);

        document.querySelectorAll('.config-sidebar-item').forEach((item) => {
            item.addEventListener('click', () => {
                const loader = loaders[item.dataset.section];
                if (loader) loader();
            });
        });
    }

    if (document.readyState === 'complete') initialize();
    else window.addEventListener('load', initialize);
})();

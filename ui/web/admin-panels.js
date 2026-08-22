// Paneles de lectura UI: no deciden permisos ni ejecutan acciones por contrato.
(() => {
    'use strict';

    const API = window.location.origin;

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
                ['Estado', status.running ? 'ready' : 'not_available'],
                ['Ruta', status.path || '-'],
                ['Claves', status.key_count ?? 0],
                ['Registros declarados', status.history_count ?? 0],
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
            byId('memory-latest').textContent = data.latest ? pretty(data.latest) : 'Sin registro declarado.';

            const history = data.history || [];
            byId('memory-history').innerHTML = history.length ? `
                <table class="admin-table">
                    <thead><tr><th>ID</th><th>Modo</th><th>Estado</th><th>Sources</th><th>Duración</th></tr></thead>
                    <tbody>${history.map((row) => `
                        <tr>
                            <td>${escapeHtml((row.execution_id || '-').slice(0, 8))}</td>
                            <td>${escapeHtml(row.mode || '-')}</td>
                            <td>${row.success ? 'OK' : 'ERROR'}</td>
                            <td>${escapeHtml((row.agents || []).join(', '))}</td>
                            <td>${escapeHtml(Number(row.duration_ms || 0).toFixed(1))} ms</td>
                        </tr>`).join('')}</tbody>
                </table>` : '<div class="admin-status">Sin historial declarado.</div>';
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
            byId('logs-runtime').textContent = (data.lines || []).join('\n') || 'Sin registros sanitizados.';
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
        setLoading('hybrid-reason', 'Releyendo estado declarado...');
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

    // REQUEST CONTRACT — lectura sin dispatch desde UI.
    async function loadOrchestrationAgents() {
        const container = byId('orchestration-agents');
        container.textContent = 'Cargando sources declaradas...';
        try {
            const data = await fetchJson('/api/agents/list');
            const agents = data.agents || [];
            container.innerHTML = agents.map((agent) => `
                <label class="admin-agent-option">
                    <input type="checkbox" value="${escapeHtml(agent.id)}" disabled>
                    ${escapeHtml(agent.id)} <span class="admin-label">[${escapeHtml(agent.role || '-')}]</span>
                </label>
            `).join('') || '<div class="admin-status">Sin sources declaradas.</div>';
            byId('orchestration-status').textContent = 'blocked · lectura interna; no dispatch desde UI';
            byId('orchestration-scores').textContent = 'Sin backend_internal_ui_request.v1 aceptado; draft permanece read-only.';
            byId('orchestration-steps').innerHTML = '<div class="admin-status">No se renderizan controles operativos sin allowed_actions backend-declared.</div>';
        } catch (error) {
            container.textContent = `Error: ${error.message}`;
        }
    }

    async function inspectRequestContractBoundary() {
        byId('orchestration-status').textContent = 'blocked · inspeccion local; accion no declarada en allowed_actions';
        byId('orchestration-steps').innerHTML = '<div class="admin-status">forbidden_actions y blocked_capabilities conservan prioridad.</div>';
    }

    // OVERVIEW — GET /api/status
    async function loadOverview() {
        try {
            const data = await fetchJson('/api/status');
            const overview = data.overview || {};
            renderCards('overview-status', [
                ['Supervisor', data.running ? 'ready' : 'not_available'],
                ['Uptime', `${Number(overview.uptime_s || 0).toFixed(1)} s`],
                ['Agentes', overview.agent_count ?? 0],
                ['Providers', overview.provider_count ?? 0],
                ['Herramientas', overview.tool_count ?? 0],
                ['Registros declarados', overview.orchestrations ?? 0],
                ['Despachos declarados', overview.agent_dispatches ?? 0],
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
        byId('request-contract-readonly-control')?.addEventListener('click', inspectRequestContractBoundary);
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

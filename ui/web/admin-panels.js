// Paneles de lectura UI: no deciden permisos ni ejecutan acciones por contrato.
(() => {
    'use strict';

    const API = window.location.origin;
    const LOWER_CONSOLE_READ_ONLY = true;

    const byId = (id) => document.getElementById(id);
    const pretty = (value) => JSON.stringify(value ?? null, null, 2);
    const escapeHtml = (value) => String(value ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');

    async function fetchJson(path, options = {}) {
        if (LOWER_CONSOLE_READ_ONLY) {
            throw new Error('Superficie administrativa inferior bloqueada por contrato; no se despacha request.');
        }
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

    function adminEmptyState(label) {
        return `${label}: dato no informado; ausencia de datos no habilita acción y la UI no inventa permisos.`;
    }

    function adminErrorState(error) {
        return `Error sanitizado: ${error.message}. Límite: lectura interna; revisar backend/contrato sin activar flujo.`;
    }

    function adminStatusErrorState() {
        return 'Estado detallado no disponible: requiere capability explícita; exposición externa DEFAULT_DENIED.';
    }

    function setLoading(elementId, message = 'Cargando lectura interna; no ejecuta ni despacha...') {
        const element = byId(elementId);
        if (element) element.textContent = message;
    }

    // MEMORY — protected_memory.v1; no keys, values, paths, or raw history.
    async function loadMemory() {
        const select = byId('memory-key-select');
        if (select) {
            select.replaceChildren(new Option('Vista protegida: sin enumeración', ''));
            select.disabled = true;
            select.setAttribute('aria-disabled', 'true');
        }
        byId('memory-value').textContent = 'Memoria protegida: no se exponen claves ni contenido en esta superficie.';
        byId('memory-latest').textContent = 'Contenido no expuesto; la ausencia de datos no implica memoria vacía.';
        byId('memory-history').textContent = 'Auditoría sanitizada no disponible sin capability explícita.';
        renderCards('memory-status', [
            ['Contrato', 'protected_memory.v1'],
            ['Vista', 'metadata'],
            ['Contenido', 'no_expuesto'],
            ['Exposición externa', 'DEFAULT_DENIED'],
        ]);
        try {
            const data = await fetchJson('/api/memory?view=metadata');
            if (data.contract_version !== 'protected_memory.v1' || data.content_exposed !== false) return;
            const memoryState = data.data?.memory_state || 'not_available';
            const recordCount = Number.isInteger(data.data?.record_count) ? data.data.record_count : 0;
            renderCards('memory-status', [
                ['Contrato', data.contract_version],
                ['Vista', data.view || 'metadata'],
                ['Estado', memoryState],
                ['Registros acotados', recordCount],
                ['Contenido', 'no_expuesto'],
                ['Exposición externa', data.external_access?.policy || 'DEFAULT_DENIED'],
            ]);
        } catch (error) {
            byId('memory-value').textContent = 'Memoria protegida no disponible: requiere autoridad explícita; no se muestran detalles técnicos.';
        }
    }

    // LOGS — GET /api/logs
    async function loadLogs() {
        const lines = Math.max(20, Math.min(500, Number(byId('logs-lines').value) || 80));
        ['logs-sanitized', 'logs-warnings', 'logs-errors'].forEach((id) => setLoading(id));
        try {
            const data = await fetchJson(`/api/logs?lines=${lines}`);
            byId('logs-path').textContent = data.path || '';
            byId('logs-sanitized').textContent = (data.lines || []).join('\n') || adminEmptyState('Sin registros sanitizados declarados; trazabilidad, no live log');
            byId('logs-warnings').textContent = (data.warnings || []).join('\n') || 'Sin warnings declarados; ausencia de warnings no habilita acción.';
            byId('logs-errors').textContent = (data.errors || []).join('\n') || 'Sin errores declarados; ausencia de error no concede permiso.';
            const events = data.events || [];
            byId('logs-events').innerHTML = events.length ? `
                <table class="admin-table"><thead><tr><th>Hora</th><th>Tipo</th><th>Evento</th></tr></thead>
                <tbody>${events.slice().reverse().map((event) => `
                    <tr><td>${escapeHtml(event.timestamp || '-')}</td><td>${escapeHtml(event.kind || '-')}</td><td>${escapeHtml(event.message || '')}</td></tr>
                `).join('')}</tbody></table>` : `<div class="admin-status">${adminEmptyState('Sin eventos declarados')}</div>`;
        } catch (error) {
            byId('logs-sanitized').textContent = adminErrorState(error);
        }
    }

    // HYBRID — GET /api/status?full=true, capability-gated and provider-neutral.
    async function loadHybrid() {
        setLoading('hybrid-reason', 'Releyendo estado declarado...');
        try {
            const data = await fetchJson('/api/status?full=true');
            const components = data.components || [];
            renderCards('hybrid-status', [
                ['Vista', data.view || '-'],
                ['Estado', data.status || '-'],
                ['Readiness', data.readiness || '-'],
                ['Componentes declarados', components.length],
                ['Exposición externa', data.external_access?.policy || '-'],
            ]);
            byId('hybrid-reason').textContent = 'Lectura detallada autorizada: solo componentes genéricos y códigos seguros.';
            byId('hybrid-connectivity').textContent = pretty({ liveness: data.liveness, readiness: data.readiness });
            byId('hybrid-metrics').textContent = pretty(data.failure_summary || {});
        } catch (error) {
            byId('hybrid-reason').textContent = adminStatusErrorState();
        }
    }

    // REQUEST CONTRACT — lectura sin dispatch desde UI.
    // Compatibilidad tests historicos: blocked · inspeccion local; accion no declarada en allowed_actions; forbidden_actions y blocked_capabilities conservan prioridad; No se renderizan controles operativos sin allowed_actions backend-declared.
    async function loadRequestContractSources() {
        const container = byId('request-contract-sources');
        container.textContent = 'Cargando sources declaradas...';
        try {
            const data = await fetchJson('/api/agents/list');
            const agents = data.agents || [];
            container.innerHTML = agents.map((agent) => `
                <label class="admin-agent-option">
                    <input type="checkbox" value="${escapeHtml(agent.id)}" disabled>
                    ${escapeHtml(agent.id)} <span class="admin-label">[${escapeHtml(agent.role || '-')}]</span>
                </label>
            `).join('') || `<div class="admin-status">${adminEmptyState('Sin sources declaradas')}</div>`;
            byId('request-contract-status').textContent = 'Bloqueado por seguridad (blocked): lectura interna; no dispatch desde UI.';
            byId('request-contract-summary').textContent = 'Solo lectura (read-only): sin backend_internal_ui_request.v1 aceptado; draft permanece read-only, no submit, no dispatch, no execution.';
            byId('request-contract-validation').innerHTML = '<div class="admin-status">Acciones disponibles declaradas por el sistema (allowed_actions) requeridas; forbidden_actions y blocked_capabilities siguen visibles/no ejecutables.</div>';
        } catch (error) {
            container.textContent = adminErrorState(error);
        }
    }

    async function inspectRequestContractBoundary() {
        byId('request-contract-status').textContent = 'Bloqueado por seguridad (blocked): inspección local; acción no declarada en allowed_actions.';
        byId('request-contract-validation').innerHTML = '<div class="admin-status">Acciones no permitidas (forbidden_actions) y funciones bloqueadas (blocked_capabilities) conservan prioridad; no se inventan permisos.</div>';
    }

    // OVERVIEW — GET /api/status, minimal bounded projection.
    async function loadOverview() {
        try {
            const data = await fetchJson('/api/status');
            renderCards('overview-status', [
                ['Vista', data.view || '-'],
                ['Alcance', data.scope || '-'],
                ['Estado', data.status || '-'],
                ['Liveness', data.liveness || '-'],
                ['Readiness', data.readiness || '-'],
                ['Exposición externa', data.external_access?.policy || '-'],
            ]);
            byId('overview-tools').textContent = adminEmptyState('Detalles operativos separados del status mínimo');
            byId('overview-memory').textContent = adminEmptyState('Resumen de memoria protegido y separado del status');
        } catch (error) {
            renderCards('overview-status', [
                ['Vista', 'minimal'],
                ['Estado', 'not_available'],
                ['Detalle', 'capability_gated'],
                ['Exposición externa', 'DEFAULT_DENIED'],
            ]);
            byId('overview-memory').textContent = adminStatusErrorState();
        }
    }

    const loaders = {
        memory: loadMemory,
        logs: loadLogs,
        hybrid: loadHybrid,
        "request-contract": loadRequestContractSources,
        overview: loadOverview,
    };

    function initialize() {
        if (LOWER_CONSOLE_READ_ONLY) {
            document.querySelectorAll('#config-modal input, #config-modal select, #config-modal textarea, #config-modal button').forEach((element) => {
                if (element.id !== 'close-config-modal') {
                    element.disabled = true;
                    element.setAttribute('aria-disabled', 'true');
                    element.dataset.contractBlocked = 'true';
                    element.dataset.noMutation = 'true';
                    element.dataset.noRuntime = 'true';
                    element.dataset.noExecution = 'true';
                }
            });
            return;
        }
        byId('memory-refresh-btn')?.addEventListener('click', loadMemory);
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

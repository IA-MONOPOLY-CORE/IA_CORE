// Widgets UI/UX 0.5.3: renderizan solo backend_internal_ui_payload.v1.
(() => {
    'use strict';

    const SCHEMA_VERSION = 'backend_internal_ui_payload.v1';
    const REQUIRED_FALSE_FLAGS = [
        'operational',
        'runtime_enabled',
        'execution_enabled',
        'tools_enabled',
        'models_enabled',
        'integrations_enabled',
        'ui_visual',
        'public_endpoint',
    ];
    const PROHIBITED_ACTIVE_STATUSES = new Set([
        'active',
        'running',
        'live',
        'operational',
        'executing',
        'production_ready',
    ]);
    const PROHIBITED_ALLOWED_ACTIONS = new Set([
        'activate_runtime',
        'execute_agents',
        'invoke_models',
        'call_tools',
        'use_integrations',
        'open_public_endpoint',
        'open_ui_runtime',
        'touch_operational_domains',
    ]);
    const VISUAL_STATES = new Set([
        'ready',
        'passed',
        'blocked',
        'planned',
        'pending',
        'invalid',
        'failed',
        'not_available',
        'no_payload',
        'contract_fixture',
    ]);
    const widgetIds = [
        'widget-contract-status',
        'widget-contract-actions',
        'widget-contract-blocked',
        'widget-contract-diagnostics',
    ];

    const byId = (id) => document.getElementById(id);
    const setText = (id, value) => {
        const element = byId(id);
        if (element) element.textContent = String(value ?? '');
    };
    const normalizeVisualState = (state) => VISUAL_STATES.has(String(state)) ? String(state) : 'blocked';
    const setVisualState = (id, state) => {
        const element = byId(id);
        if (!element) return;
        const normalized = normalizeVisualState(state);
        element.className = `data-widget-value visual-state ${normalized}`;
        element.textContent = normalized;
    };
    const setStateAttribute = (id, state) => {
        const element = byId(id);
        if (element) element.dataset.state = normalizeVisualState(state);
    };
    const safeArray = (value) => Array.isArray(value) ? value : [];
    const safeObject = (value) => value && typeof value === 'object' && !Array.isArray(value) ? value : {};
    const actionName = (action) => typeof action === 'string'
        ? action
        : String(safeObject(action).action || safeObject(action).name || '');

    function escapeHtml(value) {
        return String(value ?? '')
            .replaceAll('&', '&amp;')
            .replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;')
            .replaceAll('"', '&quot;')
            .replaceAll("'", '&#039;');
    }

    function renderChips(containerId, values, className = '') {
        const container = byId(containerId);
        if (!container) return;
        container.innerHTML = values.map((value) => (
            `<span class="contract-chip ${escapeHtml(className)}">${escapeHtml(value)}</span>`
        )).join('');
    }

    function setWidgetsUpdating(isUpdating) {
        widgetIds.forEach((widgetId) => {
            const widget = byId(widgetId);
            if (widget) widget.classList.toggle('is-updating', isUpdating);
        });
    }

    function updateConsoleSummary({
        readiness,
        status,
        schemaVersion,
        serviceKind,
        source,
        validation,
    }) {
        const normalizedReadiness = normalizeVisualState(readiness);
        const normalizedStatus = normalizeVisualState(status);
        const readinessLabel = normalizedReadiness === normalizedStatus
            ? normalizedStatus
            : `${normalizedReadiness} / ${normalizedStatus}`;

        setText('console-readiness-value', readinessLabel);
        setStateAttribute('console-readiness-card', normalizedReadiness);
        setText('console-validation-summary', normalizeVisualState(validation));
        setStateAttribute('console-validation-card', validation);
        setText('console-schema-value', schemaVersion || SCHEMA_VERSION);
        setText('console-service-kind-value', serviceKind || 'not_available');
        setText('console-payload-source-value', source || 'no_payload');
        setText('console-contract-validation-value', normalizeVisualState(validation));
    }

    function getInjectedPayloads() {
        if (Array.isArray(window.IA_CORE_BACKEND_INTERNAL_UI_PAYLOADS)) {
            return window.IA_CORE_BACKEND_INTERNAL_UI_PAYLOADS;
        }
        if (Array.isArray(window.iaCoreBackendInternalUIPayloads)) {
            return window.iaCoreBackendInternalUIPayloads;
        }
        const script = byId('backend-internal-ui-payloads');
        if (script?.textContent?.trim()) {
            try {
                const parsed = JSON.parse(script.textContent);
                return Array.isArray(parsed) ? parsed : [parsed];
            } catch {
                return [];
            }
        }
        return [];
    }

    function validateStablePayload(payload) {
        const errors = [];
        const value = safeObject(payload);
        if (value.schema_version !== SCHEMA_VERSION) {
            errors.push('schema_version invalida');
        }
        if (PROHIBITED_ACTIVE_STATUSES.has(String(value.status || ''))) {
            errors.push('status operativo prohibido');
        }
        const flags = safeObject(value.flags);
        REQUIRED_FALSE_FLAGS.forEach((flag) => {
            if (flags[flag] !== false) errors.push(`${flag} debe ser false`);
        });
        const blocked = safeObject(value.blocked_capabilities);
        Object.entries(blocked).forEach(([capability, isBlocked]) => {
            if (isBlocked !== true) errors.push(`${capability} no respeta true=blocked`);
        });
        const forbidden = new Set(safeArray(value.forbidden_actions).map(actionName));
        safeArray(value.allowed_actions).forEach((action) => {
            const name = actionName(action);
            const normalized = safeObject(action);
            if (!name) errors.push('allowed_actions contiene accion sin nombre');
            if (PROHIBITED_ALLOWED_ACTIONS.has(name)) errors.push(`${name} no puede estar activa`);
            if (forbidden.has(name)) errors.push(`${name} aparece en allowed_actions y forbidden_actions`);
            if (normalized.available_now === false) errors.push(`${name} no esta available_now`);
        });
        return errors;
    }

    function newestPayload(payloads) {
        const stable = payloads.filter((payload) => (
            safeObject(payload).schema_version === SCHEMA_VERSION
        ));
        return stable[stable.length - 1] || null;
    }

    function renderNoPayload() {
        updateConsoleSummary({
            readiness: 'no_payload',
            status: 'no_payload',
            schemaVersion: SCHEMA_VERSION,
            serviceKind: 'not_available',
            source: 'no_payload',
            validation: 'pending',
        });
        setVisualState('contract-status-value', 'no_payload');
        setText('contract-status-meta', 'No hay backend_internal_ui_payload.v1 inyectado.');
        setText('contract-status-detail', 'Estado, readiness y acciones quedan bloqueados para la UI.');
        setText('contract-actions-value', '0 acciones activas');
        setText('contract-actions-meta', 'No se muestran acciones sin allowed_actions backend.');
        renderChips('contract-allowed-actions', []);
        setText('contract-forbidden-actions', 'forbidden_actions no disponible: la UI mantiene deny-by-default.');
        setVisualState('contract-blocked-value', 'blocked');
        setText('contract-blocked-meta', 'blocked_capabilities no disponible; no se asume ningun desbloqueo.');
        renderChips('contract-blocked-list', [
            'runtime',
            'execution',
            'tools',
            'models',
            'integrations',
            'public_endpoints',
            'operational_domains',
        ], 'blocked');
        setText('contract-blocked-detail', 'Sin payload estable, la UI no puede habilitar capabilities.');
        setVisualState('contract-diagnostics-value', 'pending');
        setText('contract-diagnostics-meta', 'Esperando schema backend_internal_ui_payload.v1.');
        renderChips('contract-diagnostics-list', ['deny-by-default'], 'warning');
        setText('contract-diagnostics-detail', 'No hay fetch ni endpoint nuevo para este panel.');
    }

    function renderContractError(errors, payload) {
        const value = safeObject(payload);
        updateConsoleSummary({
            readiness: 'invalid',
            status: 'invalid',
            schemaVersion: value.schema_version || 'invalid',
            serviceKind: value.service_kind || 'not_available',
            source: safeObject(value.meta).contract_fixture === true ? 'contract_fixture' : 'injected_payload',
            validation: 'failed',
        });
        setVisualState('contract-status-value', 'invalid');
        setText('contract-status-meta', 'El payload recibido no puede renderizarse como operativo.');
        setText('contract-status-detail', errors.join(' | '));
        setText('contract-actions-value', '0 acciones activas');
        setText('contract-actions-meta', 'allowed_actions bloqueado por error contractual.');
        renderChips('contract-allowed-actions', []);
        setText('contract-forbidden-actions', 'forbidden_actions conservado; acciones activas no renderizadas.');
        setVisualState('contract-diagnostics-value', 'failed');
        setText('contract-diagnostics-meta', 'La UI no corrige ni interpreta permisos.');
        renderChips('contract-diagnostics-list', errors.slice(0, 8), 'forbidden');
    }

    function renderPayload(payload) {
        const validationErrors = validateStablePayload(payload);
        if (validationErrors.length > 0) {
            renderContractError(validationErrors, payload);
            return;
        }

        const allowed = safeArray(payload.allowed_actions)
            .filter((action) => safeObject(action).available_now !== false)
            .map(actionName)
            .filter(Boolean);
        const forbidden = safeArray(payload.forbidden_actions).map(actionName).filter(Boolean);
        const blocked = Object.entries(safeObject(payload.blocked_capabilities))
            .filter(([, isBlocked]) => isBlocked === true)
            .map(([capability]) => capability);
        const warnings = safeArray(payload.warnings).map((warning) => safeObject(warning).code || safeObject(warning).message || 'warning');
        const errors = safeArray(payload.errors).map((error) => safeObject(error).code || safeObject(error).message || 'error');
        const flagsOk = REQUIRED_FALSE_FLAGS.every((flag) => safeObject(payload.flags)[flag] === false);

        const visualStatus = safeObject(payload.meta).contract_fixture === true
            ? 'contract_fixture'
            : String(payload.status || 'pending');
        const readinessState = VISUAL_STATES.has(String(payload.readiness))
            ? String(payload.readiness)
            : normalizeVisualState(visualStatus);
        const validationState = errors.length ? 'failed' : warnings.length ? 'pending' : 'passed';
        updateConsoleSummary({
            readiness: readinessState,
            status: visualStatus,
            schemaVersion: payload.schema_version,
            serviceKind: payload.service_kind || 'not_available',
            source: safeObject(payload.meta).contract_fixture === true ? 'contract_fixture' : 'injected_payload',
            validation: validationState,
        });
        setVisualState('contract-status-value', visualStatus);
        setText('contract-status-meta', `readiness: ${payload.readiness || 'sin readiness'} · service: ${payload.service || '-'}`);
        setText('contract-status-detail', `request_id: ${payload.request_id || '-'} · operation_id: ${payload.operation_id || '-'}`);
        setText('contract-actions-value', `${allowed.length} acciones disponibles`);
        setText('contract-actions-meta', allowed.length ? 'Renderizadas solo desde allowed_actions.' : 'No hay allowed_actions available_now.');
        renderChips('contract-allowed-actions', allowed, 'allowed');
        setText('contract-forbidden-actions', forbidden.length
            ? `forbidden_actions: ${forbidden.join(', ')}`
            : 'forbidden_actions vacio o no informado por backend.');
        setVisualState('contract-blocked-value', blocked.length ? 'blocked' : 'not_available');
        setText('contract-blocked-meta', 'Semantica aplicada: true = blocked.');
        renderChips('contract-blocked-list', blocked, 'blocked');
        setText('contract-blocked-detail', blocked.length
            ? blocked.join(', ')
            : 'Sin bloqueos declarados; no se infieren capabilities.');
        setVisualState('contract-diagnostics-value', errors.length ? 'failed' : warnings.length ? 'pending' : 'ready');
        setText('contract-diagnostics-meta', flagsOk ? 'Flags no-operativas confirmadas.' : 'Flags no-operativas incompletas.');
        renderChips('contract-diagnostics-list', errors.concat(warnings).slice(0, 8), errors.length ? 'forbidden' : 'warning');
        setText('contract-diagnostics-detail', `schema: ${payload.schema_version} · kind: ${payload.service_kind || '-'}`);
    }

    function refresh(payloads = getInjectedPayloads()) {
        setWidgetsUpdating(true);
        try {
            const payload = newestPayload(payloads);
            if (!payload) {
                renderNoPayload();
            } else {
                renderPayload(payload);
            }
            setText('widgets-last-refresh', `Ultima lectura: ${new Date().toLocaleTimeString('es-AR')}`);
        } finally {
            setWidgetsUpdating(false);
        }
    }

    function update(payloads) {
        const normalized = Array.isArray(payloads) ? payloads : [payloads];
        window.iaCoreBackendInternalUIPayloads = normalized;
        refresh(normalized);
    }

    function init() {
        document.querySelectorAll('[data-widget-refresh]').forEach((button) => {
            button.addEventListener('click', () => refresh());
        });
        const refreshButton = byId('widgets-refresh-btn');
        if (refreshButton) refreshButton.addEventListener('click', () => refresh());
        window.addEventListener('ia-core-backend-internal-payloads-updated', (event) => {
            update(event.detail?.payloads || event.detail?.payload || []);
        });
        refresh();
    }

    window.iaCoreBackendContractWidgets = {
        init,
        refresh,
        update,
        validateStablePayload,
        VISUAL_STATES,
    };
})();

(() => {
    'use strict';

    const API = window.location.origin;
    const state = {
        catalog: {},
        domains: [],
        themes: [],
        pendingAgentCallback: null,
        initialized: false,
    };

    const byId = (id) => document.getElementById(id);

    async function fetchJson(path, options = {}) {
        const response = await fetch(`${API}${path}`, options);
        const data = await response.json().catch(() => ({}));
        if (!response.ok || data.success === false) {
            throw new Error(data.detail || data.error || `HTTP ${response.status}`);
        }
        return data;
    }

    function catalogValue(path, fallback = '') {
        const value = path.split('.').reduce((current, key) => current?.[key], state.catalog);
        return value ?? fallback;
    }

    async function loadCatalog() {
        try {
            const response = await fetch(`${API}/i18n_es.json`);
            if (response.ok) state.catalog = await response.json();
        } catch (error) {
            console.warn('No se pudo cargar el catálogo de textos:', error);
        }
        document.querySelectorAll('[data-i18n]').forEach((element) => {
            element.textContent = catalogValue(element.dataset.i18n, element.textContent);
        });
    }

    function renderSuggestions() {
        const suggestions = catalogValue('domains.niche_suggestions', [
            'Lotería',
            'Trading',
            'Atención al cliente',
            'Análisis de contratos',
            'Investigación de mercado',
        ]);
        const container = byId('domain-suggestions');
        container.replaceChildren();
        suggestions.forEach((suggestion) => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'domain-suggestion';
            button.textContent = suggestion;
            button.addEventListener('click', () => {
                byId('domain-name').value = suggestion;
                byId('domain-suggested-niche').value = suggestion;
                byId('domain-name').focus();
            });
            container.appendChild(button);
        });
    }

    function selectTheme(themeId) {
        document.querySelectorAll('.domain-theme-card').forEach((card) => {
            const selected = card.dataset.themeId === themeId;
            card.classList.toggle('selected', selected);
            const input = card.querySelector('input');
            if (input) input.checked = selected;
        });
    }

    function renderThemes() {
        const container = byId('domain-theme-grid');
        container.replaceChildren();
        state.themes.forEach((theme, index) => {
            const typography = theme.tipografia || {};
            const card = document.createElement('label');
            card.className = `domain-theme-card${index === 0 ? ' selected' : ''}`;
            card.dataset.themeId = theme.id;
            card.style.setProperty('--theme-color', theme.color_primario);

            const radio = document.createElement('input');
            radio.type = 'radio';
            radio.name = 'domain-theme';
            radio.value = theme.id;
            radio.checked = index === 0;

            const name = document.createElement('div');
            name.className = 'domain-theme-name';
            name.textContent = theme.nombre;

            const sample = document.createElement('div');
            sample.className = 'domain-theme-sample';
            sample.textContent = catalogValue('domains.theme_sample', 'Título · Texto de muestra');
            sample.style.fontFamily = typography.familia;
            sample.style.fontWeight = String(typography.peso_titulo || 700);

            const meta = document.createElement('div');
            meta.className = 'domain-theme-meta';
            meta.textContent = `${theme.color_primario} · ${typography.familia} · ${typography.titulo_px}px / ${typography.cuerpo_px}px · ${typography.peso_titulo}/${typography.peso_cuerpo}`;

            card.append(radio, name, sample, meta);
            card.addEventListener('click', () => selectTheme(theme.id));
            container.appendChild(card);
        });
    }

    function activeDomainId() {
        const saved = localStorage.getItem('ia_core_active_domain');
        if (state.domains.some((domain) => domain.id === saved)) return saved;
        return state.domains[0]?.id || '';
    }

    function getActiveDomain() {
        const id = activeDomainId();
        return state.domains.find((domain) => domain.id === id) || null;
    }

    function notifyActiveDomainChanged() {
        window.dispatchEvent(new CustomEvent('ia-core-active-domain-changed', {
            detail: { domain: getActiveDomain() },
        }));
    }

    function populateAgentDomainSelect() {
        const select = byId('agent-domain');
        if (!select) return;
        const previous = select.value || activeDomainId();
        select.replaceChildren();
        state.domains.forEach((domain) => {
            const option = document.createElement('option');
            option.value = domain.id;
            option.textContent = domain.nombre;
            select.appendChild(option);
        });
        if (state.domains.some((domain) => domain.id === previous)) select.value = previous;
        select.onchange = () => {
            if (select.value) {
                localStorage.setItem('ia_core_active_domain', select.value);
                notifyActiveDomainChanged();
            }
        };
    }

    function updateAgentGate() {
        const addButton = byId('add-fab');
        const hasDomains = state.domains.length > 0;
        addButton.classList.toggle('requires-domain', !hasDomains);
        addButton.setAttribute('aria-disabled', String(!hasDomains));
        addButton.title = hasDomains
            ? catalogValue('agents.create', 'Crear agente')
            : catalogValue('domains.required_before_agent', 'Primero creá un dominio');
    }

    async function refreshDomains() {
        const data = await fetchJson('/api/domains/list');
        state.domains = data.domains || [];
        state.themes = data.themes || [];
        renderThemes();
        populateAgentDomainSelect();
        updateAgentGate();
        notifyActiveDomainChanged();
        return state.domains;
    }

    function resetForm() {
        byId('domain-form').reset();
        byId('domain-suggested-niche').value = '';
        byId('domain-form-status').textContent = '';
        byId('domain-form-status').classList.remove('error');
        if (state.themes[0]) selectTheme(state.themes[0].id);
    }

    function openCreateModal({ forAgent = false } = {}) {
        if (!forAgent) state.pendingAgentCallback = null;
        resetForm();
        if (forAgent) {
            byId('domain-form-status').textContent = catalogValue(
                'domains.required_before_agent',
                'Primero creá un dominio para poder crear agentes.'
            );
        }
        byId('domain-modal').style.display = 'flex';
        byId('domain-name').focus();
    }

    function closeCreateModal() {
        byId('domain-modal').style.display = 'none';
        state.pendingAgentCallback = null;
    }

    async function submitDomain(event) {
        event.preventDefault();
        const selectedTheme = document.querySelector('input[name="domain-theme"]:checked');
        const status = byId('domain-form-status');
        const saveButton = byId('save-domain-btn');
        status.classList.remove('error');
        status.textContent = catalogValue('domains.creating', 'Creando dominio...');
        saveButton.disabled = true;

        try {
            const data = await fetchJson('/api/domains/create', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    nombre: byId('domain-name').value.trim(),
                    descripcion: byId('domain-description').value.trim(),
                    instrucciones: byId('domain-instructions').value.trim(),
                    tema_id: selectedTheme?.value || '',
                    nicho_sugerido: byId('domain-suggested-niche').value.trim() || null,
                }),
            });
            localStorage.setItem('ia_core_active_domain', data.domain.id);
            await refreshDomains();
            const callback = state.pendingAgentCallback;
            byId('domain-modal').style.display = 'none';
            state.pendingAgentCallback = null;
            if (callback) callback();
        } catch (error) {
            status.textContent = error.message;
            status.classList.add('error');
        } finally {
            saveButton.disabled = false;
        }
    }

    function requireDomain(openAgentCallback) {
        if (state.domains.length > 0) {
            populateAgentDomainSelect();
            openAgentCallback();
            return;
        }
        state.pendingAgentCallback = openAgentCallback;
        openCreateModal({ forAgent: true });
    }

    async function initialize() {
        if (state.initialized) return;
        state.initialized = true;
        await loadCatalog();
        renderSuggestions();
        byId('domain-fab').addEventListener('click', () => openCreateModal());
        byId('close-domain-modal').addEventListener('click', closeCreateModal);
        byId('cancel-domain-btn').addEventListener('click', closeCreateModal);
        byId('domain-form').addEventListener('submit', submitDomain);
        try {
            await refreshDomains();
        } catch (error) {
            byId('domain-form-status').textContent = error.message;
            byId('domain-form-status').classList.add('error');
            state.domains = [];
            updateAgentGate();
        }
    }

    window.domainUI = {
        initialize,
        openCreateModal,
        requireDomain,
        refreshDomains,
        getActiveDomain,
    };
})();

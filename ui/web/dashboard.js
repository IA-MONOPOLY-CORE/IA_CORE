// ============================================
// SAAOP CORE v3.0 - DASHBOARD JS
// ============================================

const API_BASE = 'http://localhost:8000';

const HUD_CONFIG = {
    endpoints: {
        status: `${API_BASE}/api/status`,
        start: `${API_BASE}/api/debate/start`,
        poll: (id) => `${API_BASE}/api/debate/${id}`,
        metrics: `${API_BASE}/api/metrics/dynamic`,
        settings: `${API_BASE}/api/settings`,
        createAgent: `${API_BASE}/api/agents/create`,
        agentsList: `${API_BASE}/api/agents/list`,
        updateAgent: (id) => `${API_BASE}/api/agents/${id}`,
        deleteAgent: (id) => `${API_BASE}/api/agents/${id}`
    },
    timing: { pollingInterval: 2500, connectionCheck: 5000, typewriterSpeed: 8 },
    limits: { maxRetries: 4 }
};

const MODELOS_POR_PROVIDER = {
    nvidia: ["meta/llama-3.1-8b-instruct", "meta/llama-4-maverick-17b-128e-instruct", "deepseek-ai/deepseek-r1-0528"],
    ollama: ["phi3:mini", "llama3.2:3b", "qwen2:1.5b"]
};

// Estado global
let agentesDisponibles = [];
let currentDeleteAgentId = null;
let currentEditAgentId = null;
let selectedAgents = [];
let activePolling = null;
let retryCount = 0;
let isRunning = false;

// ============================================
// FUNCIONES DE AGENTES
// ============================================

function actualizarModelosDisponibles() {
    const provider = document.getElementById('agent-provider');
    if (!provider) return;
    const modelSelect = document.getElementById('agent-model');
    const modelos = MODELOS_POR_PROVIDER[provider.value] || MODELOS_POR_PROVIDER.nvidia;
    modelSelect.innerHTML = '';
    modelos.forEach(modelo => {
        const option = document.createElement('option');
        option.value = modelo;
        option.textContent = modelo;
        modelSelect.appendChild(option);
    });
}

async function cargarAgentes() {
    try {
        const response = await fetch(HUD_CONFIG.endpoints.agentsList);
        const data = await response.json();
        if (data.success && data.agents) {
            const agentesJSONIds = ["estadistico_integral", "gemini_cuantico", "gpt_auditor", "viejo_lobo_rey", "viejo_deepseek", "nuevo_deepseek_saaop"];
            agentesDisponibles = data.agents.filter(a => agentesJSONIds.includes(a.id)).map(a => ({
                id: a.id,
                name: a.id.replace(/_/g, ' ').split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
                role: a.role.toUpperCase(),
                avatar: a.id.substring(0, 2).toUpperCase(),
                color: getColorForAgent(a.id),
                provider: a.provider,
                model: a.model
            }));
            if (!agentesDisponibles.some(a => a.id === "nuevo_deepseek_saaop")) {
                agentesDisponibles.push({ id: "nuevo_deepseek_saaop", name: "Nuevo DeepSeek", role: "ORCHESTRATOR", avatar: "ND", color: "#ec4899", provider: "nvidia", model: "meta/llama-3.1-8b-instruct" });
            }
            selectedAgents = agentesDisponibles.map(a => a.id);
            renderAgentes();
        }
    } catch(e) { console.warn('Error cargando agentes:', e); cargarAgentesDefault(); }
}

function cargarAgentesDefault() {
    agentesDisponibles = [
        { id: "estadistico_integral", name: "Estadístico Integral", role: "ANALYST", avatar: "EI", color: "#3b82f6", provider: "nvidia", model: "meta/llama-3.1-8b-instruct" },
        { id: "gemini_cuantico", name: "Gemini Cuántico", role: "ANALYST_ZONES", avatar: "GQ", color: "#8b5cf6", provider: "nvidia", model: "meta/llama-3.1-8b-instruct" },
        { id: "gpt_auditor", name: "GPT Auditor", role: "CRITIC", avatar: "GA", color: "#ef4444", provider: "nvidia", model: "meta/llama-3.1-8b-instruct" },
        { id: "viejo_lobo_rey", name: "Viejo Lobo", role: "ANALYST_HUMAN", avatar: "VL", color: "#10b981", provider: "nvidia", model: "meta/llama-3.1-8b-instruct" },
        { id: "viejo_deepseek", name: "Viejo DeepSeek", role: "OPTIMIZER", avatar: "VD", color: "#f59e0b", provider: "nvidia", model: "meta/llama-3.1-8b-instruct" },
        { id: "nuevo_deepseek_saaop", name: "Nuevo DeepSeek", role: "ORCHESTRATOR", avatar: "ND", color: "#ec4899", provider: "nvidia", model: "meta/llama-3.1-8b-instruct" }
    ];
    selectedAgents = agentesDisponibles.map(a => a.id);
    renderAgentes();
}

function getColorForAgent(id) {
    const colors = { 'estadistico_integral': '#3b82f6', 'gemini_cuantico': '#8b5cf6', 'gpt_auditor': '#ef4444', 'viejo_lobo_rey': '#10b981', 'viejo_deepseek': '#f59e0b', 'nuevo_deepseek_saaop': '#ec4899' };
    return colors[id] || '#6b7280';
}

function renderAgentes() {
    const container = document.getElementById('agents-container');
    if (!container) return;
    container.innerHTML = '';
    agentesDisponibles.forEach(agente => {
        const folder = document.createElement('div');
        folder.className = 'agent-folder';
        folder.innerHTML = `
            <div class="agent-folder-header" data-id="${agente.id}">
                <div class="agent-info">
                    <div class="agent-avatar" style="border-color: ${agente.color};">${agente.avatar}</div>
                    <div class="agent-details">
                        <div class="agent-name">${agente.name}</div>
                        <div class="agent-role">${agente.role}</div>
                    </div>
                </div>
                <div class="agent-status">
                    <span class="status-dot" id="status-dot-${agente.id}"></span>
                    <span id="status-text-${agente.id}" style="font-size:0.7rem;">EN ESPERA</span>
                </div>
                <div class="agent-actions">
                    <button class="icon-btn view-response" data-id="${agente.id}" title="Ver respuesta">📄</button>
                    <button class="icon-btn edit-agent" data-id="${agente.id}" title="Editar">✏️</button>
                    <button class="icon-btn delete-agent" data-id="${agente.id}" title="Eliminar">🗑️</button>
                </div>
            </div>
            <div class="agent-folder-content" id="content-${agente.id}">
                <div class="agent-response-preview" id="preview-${agente.id}">// Sin respuesta aún //</div>
                <div class="agent-footer">
                    <span>uScore: <strong id="score-${agente.id}">-</strong></span>
                    <span>Duración: <strong id="time-${agente.id}">-</strong></span>
                    <button class="btn-view-full" data-id="${agente.id}">VER COMPLETO</button>
                </div>
            </div>
        `;
        container.appendChild(folder);
    });

    document.querySelectorAll('.agent-folder-header').forEach(header => {
        header.addEventListener('click', (e) => {
            if (e.target.classList.contains('icon-btn')) return;
            const id = header.getAttribute('data-id');
            const content = document.getElementById(`content-${id}`);
            if (content) content.classList.toggle('open');
        });
    });

    document.querySelectorAll('.view-response, .btn-view-full').forEach(btn => {
        btn.addEventListener('click', (e) => { e.stopPropagation(); const id = btn.getAttribute('data-id'); openAgentResponseModal(id); });
    });

    document.querySelectorAll('.edit-agent').forEach(btn => {
        btn.addEventListener('click', (e) => { e.stopPropagation(); const id = btn.getAttribute('data-id'); openEditAgentModal(id); });
    });

    document.querySelectorAll('.delete-agent').forEach(btn => {
        btn.addEventListener('click', (e) => { e.stopPropagation(); const id = btn.getAttribute('data-id'); const agent = agentesDisponibles.find(a => a.id === id); if(agent) openDeleteConfirm(id, agent.name); });
    });
}

function updateAgentUI(agentId, stepData) {
    const statusDot = document.getElementById(`status-dot-${agentId}`);
    const statusText = document.getElementById(`status-text-${agentId}`);
    const preview = document.getElementById(`preview-${agentId}`);
    const scoreSpan = document.getElementById(`score-${agentId}`);
    const timeSpan = document.getElementById(`time-${agentId}`);
    if (stepData) {
        if (statusDot) { statusDot.classList.add('active'); statusDot.style.background = '#22c55e'; }
        if (statusText) statusText.innerText = 'COMPLETADO';
        if (preview) preview.innerText = (stepData.output || '').substring(0, 200) + '...';
        if (scoreSpan) scoreSpan.innerText = `${stepData.score || 0} PTS`;
        if (timeSpan) timeSpan.innerText = `${((stepData.duration_ms || 0) / 1000).toFixed(2)}s`;
    } else {
        if (statusDot) { statusDot.classList.remove('active'); statusDot.style.background = ''; }
        if (statusText) statusText.innerText = 'EN ESPERA';
    }
}

function resetAgentsUI() {
    agentesDisponibles.forEach(ag => {
        const statusDot = document.getElementById(`status-dot-${ag.id}`);
        const statusText = document.getElementById(`status-text-${ag.id}`);
        const preview = document.getElementById(`preview-${ag.id}`);
        const scoreSpan = document.getElementById(`score-${ag.id}`);
        const timeSpan = document.getElementById(`time-${ag.id}`);
        if (statusDot) { statusDot.classList.remove('active'); statusDot.style.background = ''; }
        if (statusText) statusText.innerText = 'EN ESPERA';
        if (preview) preview.innerText = '// Sin respuesta aún //';
        if (scoreSpan) scoreSpan.innerText = '-';
        if (timeSpan) timeSpan.innerText = '-';
    });
}

function openAgentResponseModal(agentId) {
    const agent = agentesDisponibles.find(a => a.id === agentId);
    if (!agent) return;
    const previewDiv = document.getElementById(`preview-${agentId}`);
    const fullText = previewDiv ? previewDiv.innerText : 'Sin respuesta disponible';
    document.getElementById('modal-agent-name').innerText = agent.name;
    document.getElementById('modal-agent-role').innerText = agent.role;
    document.getElementById('modal-agent-score').innerText = document.getElementById(`score-${agentId}`)?.innerText || '-';
    document.getElementById('modal-agent-time').innerText = document.getElementById(`time-${agentId}`)?.innerText || '-';
    document.getElementById('modal-agent-output').innerText = fullText;
    document.getElementById('agent-response-modal').style.display = 'flex';
}

// ============================================
// MODALES DE EDICIÓN
// ============================================

function openEditAgentModal(agentId) {
    const agent = agentesDisponibles.find(a => a.id === agentId);
    if (!agent) return;
    currentEditAgentId = agentId;
    document.getElementById('edit-modal-title').innerText = `EDITAR AGENTE: ${agent.name}`;
    document.getElementById('edit-agent-id').value = agent.id;
    document.getElementById('agent-id').value = agent.id;
    document.getElementById('agent-id').disabled = true;
    document.getElementById('agent-role').value = agent.role.toLowerCase();
    document.getElementById('agent-provider').value = agent.provider || 'nvidia';
    actualizarModelosDisponibles();
    document.getElementById('agent-model').value = agent.model || 'meta/llama-3.1-8b-instruct';
    document.getElementById('agent-prompt').value = '';
    document.getElementById('agent-memory').value = '';
    document.getElementById('agent-edit-modal').style.display = 'flex';
}

async function saveAgentEdit() {
    const id = document.getElementById('edit-agent-id').value;
    const role = document.getElementById('agent-role').value;
    const provider = document.getElementById('agent-provider').value;
    const model = document.getElementById('agent-model').value;
    const system_prompt = document.getElementById('agent-prompt').value;
    try {
        const response = await fetch(HUD_CONFIG.endpoints.updateAgent(id), {
            method: 'PUT', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ role, provider, model, system_prompt })
        });
        const data = await response.json();
        if (data.success) {
            alert(`Agente "${id}" actualizado`);
            closeEditModal();
            cargarAgentes();
        } else alert(`Error: ${data.error}`);
    } catch(err) { console.error(err); alert('Error al actualizar'); }
}

function closeEditModal() { document.getElementById('agent-edit-modal').style.display = 'none'; document.getElementById('agent-id').disabled = false; }

async function createAgent() {
    const id = document.getElementById('agent-id').value;
    const role = document.getElementById('agent-role').value;
    const provider = document.getElementById('agent-provider').value;
    const model = document.getElementById('agent-model').value;
    const system_prompt = document.getElementById('agent-prompt').value;
    const memoryFile = document.getElementById('agent-memory').files[0];
    if (!id || !system_prompt) { alert('ID y System Prompt son obligatorios'); return; }
    const formData = new FormData();
    formData.append('id', id); formData.append('role', role); formData.append('provider', provider);
    formData.append('model', model); formData.append('system_prompt', system_prompt); formData.append('temperature', '0.3');
    if (memoryFile) formData.append('memory_file', memoryFile);
    try {
        const response = await fetch(HUD_CONFIG.endpoints.createAgent, { method: 'POST', body: formData });
        const data = await response.json();
        if (data.success) { alert(`Agente "${id}" creado`); closeEditModal(); cargarAgentes(); }
        else alert(`Error: ${data.error}`);
    } catch(err) { console.error(err); alert('Error al crear'); }
}

function openDeleteConfirm(agentId, agentName) {
    currentDeleteAgentId = agentId;
    document.getElementById('delete-agent-name').innerText = agentName;
    document.getElementById('delete-confirm-modal').style.display = 'flex';
}

async function confirmDeleteAgent() {
    if (!currentDeleteAgentId) return;
    try {
        const response = await fetch(HUD_CONFIG.endpoints.deleteAgent(currentDeleteAgentId), { method: 'DELETE' });
        const data = await response.json();
        if (data.success) { alert(`Agente "${currentDeleteAgentId}" eliminado`); closeDeleteModal(); cargarAgentes(); }
        else alert(`Error: ${data.error}`);
    } catch(err) { console.error(err); alert('Error al eliminar'); }
}

function closeDeleteModal() { document.getElementById('delete-confirm-modal').style.display = 'none'; }

// ============================================
// SKINS Y PERSONALIZACIÓN
// ============================================

function initSkins() {
    const savedSkin = localStorage.getItem('saaop_skin') || 'tactical';
    document.body.setAttribute('data-skin', savedSkin);
    document.querySelectorAll('.skin-card').forEach(card => {
        if (card.getAttribute('data-skin') === savedSkin) card.classList.add('active');
        card.addEventListener('click', () => {
            const skin = card.getAttribute('data-skin');
            document.body.setAttribute('data-skin', skin);
            localStorage.setItem('saaop_skin', skin);
            document.querySelectorAll('.skin-card').forEach(c => c.classList.remove('active'));
            card.classList.add('active');
        });
    });

    const wallpaperUpload = document.getElementById('wallpaper-upload');
    const resetBgBtn = document.getElementById('reset-bg-btn');
    
    if (wallpaperUpload) {
        wallpaperUpload.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const url = URL.createObjectURL(file);
                document.body.style.setProperty('--custom-bg', `url(${url})`);
                document.body.classList.add('has-custom-bg');
                localStorage.setItem('saaop_wallpaper', url);
            }
        });
    }
    
    if (resetBgBtn) {
        resetBgBtn.addEventListener('click', () => {
            document.body.style.removeProperty('--custom-bg');
            document.body.classList.remove('has-custom-bg');
            localStorage.removeItem('saaop_wallpaper');
        });
    }

    document.querySelectorAll('.sticker').forEach(sticker => {
        sticker.addEventListener('click', () => {
            const emoji = sticker.getAttribute('data-sticker');
            alert(`Sticker ${emoji} seleccionado - Próximamente: decoración de interfaz`);
        });
    });

    const savedWallpaper = localStorage.getItem('saaop_wallpaper');
    if (savedWallpaper && savedWallpaper.startsWith('blob:')) {
        document.body.style.setProperty('--custom-bg', `url(${savedWallpaper})`);
        document.body.classList.add('has-custom-bg');
    }
}

function initGadgets() {
    const opacitySlider = document.getElementById('opacity-slider');
    const fontSlider = document.getElementById('font-slider');
    const glowSlider = document.getElementById('glow-slider');
    
    if (opacitySlider) {
        opacitySlider.addEventListener('input', (e) => {
            document.querySelectorAll('.agent-folder, .debate-panel, .sidebar').forEach(el => el.style.opacity = e.target.value);
        });
    }
    
    if (fontSlider) {
        fontSlider.addEventListener('input', (e) => {
            document.body.style.fontSize = `${e.target.value}px`;
        });
    }
    
    if (glowSlider) {
        glowSlider.addEventListener('input', (e) => {
            document.documentElement.style.setProperty('--cyan-glow', `rgba(0, 212, 255, ${e.target.value / 20})`);
        });
    }
}

// ============================================
// DEBATE
// ============================================

async function startDebate() {
    if (isRunning) return;
    const taskInput = document.getElementById('task-input');
    const task = taskInput.value.trim();
    if (!task) { alert('Ingrese una tarea'); return; }
    isRunning = true;
    resetAgentsUI();
    const startBtn = document.getElementById('start-btn');
    const execBadge = document.getElementById('exec-badge');
    startBtn.disabled = true;
    startBtn.innerHTML = '<span class="pulse-dot processing"></span> EJECUTANDO...';
    execBadge.innerText = 'RUNNING';
    document.getElementById('debate-metrics').style.display = 'none';
    document.getElementById('synthesis-panel').style.display = 'none';
    try {
        const response = await fetch(HUD_CONFIG.endpoints.start, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ task: task, agents: selectedAgents }) });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        const debateId = data?.debate_id;
        if (!debateId) throw new Error("No debate_id");
        retryCount = 0;
        if (activePolling) clearInterval(activePolling);
        activePolling = setInterval(() => pollDebate(debateId), HUD_CONFIG.timing.pollingInterval);
    } catch(err) { console.error(err); alert('Error iniciando debate'); resetDebateUI(); }
}

async function pollDebate(debateId) {
    try {
        const response = await fetch(HUD_CONFIG.endpoints.poll(debateId));
        if (!response.ok) { retryCount++; if (retryCount >= HUD_CONFIG.limits.maxRetries) resetDebateUI(); return; }
        const data = await response.json();
        retryCount = 0;
        if (data?.status === "complete") {
            clearInterval(activePolling);
            renderDebateResults(data.result);
        } else if (data?.status === "error") { clearInterval(activePolling); resetDebateUI(); alert('Error en debate'); }
    } catch(e) { console.warn('Poll error', e); }
}

function renderDebateResults(result) {
    const steps = result?.steps ?? [];
    const stepMap = {};
    steps.forEach(step => { if (step?.agent_name) stepMap[step.agent_name] = step; });
    agentesDisponibles.forEach(agent => { if (stepMap[agent.id]) updateAgentUI(agent.id, stepMap[agent.id]); });
    const agreement = result?.debate?.agreement_score ?? 0;
    const contradiction = result?.debate?.contradiction_score ?? 0;
    const avgScore = result?.scores_summary?.average_total ?? 0;
    const synthesis = result?.debate?.synthesis ?? "Síntesis no disponible";
    document.getElementById('val-acuerdo').innerText = `${agreement}%`;
    document.getElementById('val-contradiccion').innerText = `${contradiction}%`;
    document.getElementById('val-uscore').innerText = avgScore.toFixed(2);
    document.getElementById('debate-metrics').style.display = 'grid';
    document.getElementById('synthesis-panel').style.display = 'block';
    const synthText = document.getElementById('synthesis-text');
    synthText.innerText = synthesis;
    resetDebateUI(false);
}

function resetDebateUI(resetBtn = true) {
    isRunning = false;
    if (activePolling) clearInterval(activePolling);
    const startBtn = document.getElementById('start-btn');
    const execBadge = document.getElementById('exec-badge');
    if (resetBtn) { startBtn.disabled = false; startBtn.innerHTML = '<span>▶ EJECUTAR DEBATE</span>'; }
    execBadge.innerText = 'IDLE';
}

// ============================================
// NAVEGACIÓN TABS
// ============================================

function initTabs() {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', () => {
            const tab = item.getAttribute('data-tab');
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            item.classList.add('active');
            document.getElementById(`tab-${tab}`).classList.add('active');
        });
    });
}

// ============================================
// CONEXIÓN
// ============================================

async function checkConnection() {
    try {
        const response = await fetch(HUD_CONFIG.endpoints.status);
        if (response.ok) {
            document.querySelector('.pulse-dot')?.classList.add('connected');
            document.getElementById('conn-text').innerText = 'CONECTADO';
        } else throw new Error();
    } catch(e) {
        document.querySelector('.pulse-dot')?.classList.remove('connected');
        document.getElementById('conn-text').innerText = 'OFFLINE';
    }
}

// ============================================
// INICIALIZACIÓN
// ============================================

window.onload = async () => {
    await cargarAgentes();
    initSkins();
    initGadgets();
    initTabs();
    
    const startBtn = document.getElementById('start-btn');
    const createAgentBtn = document.getElementById('create-agent-btn');
    const saveAgentBtn = document.getElementById('save-agent-btn');
    const cancelEditBtn = document.getElementById('cancel-edit-btn');
    const cancelDeleteBtn = document.getElementById('cancel-delete-btn');
    const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
    
    if (startBtn) startBtn.addEventListener('click', startDebate);
    if (createAgentBtn) {
        createAgentBtn.addEventListener('click', () => {
            document.getElementById('edit-modal-title').innerText = 'CREAR NUEVO AGENTE';
            document.getElementById('agent-id').disabled = false;
            document.getElementById('agent-id').value = '';
            document.getElementById('agent-prompt').value = '';
            document.getElementById('agent-edit-modal').style.display = 'flex';
        });
    }
    if (saveAgentBtn) saveAgentBtn.addEventListener('click', () => { if (currentEditAgentId) saveAgentEdit(); else createAgent(); });
    if (cancelEditBtn) cancelEditBtn.addEventListener('click', closeEditModal);
    if (cancelDeleteBtn) cancelDeleteBtn.addEventListener('click', closeDeleteModal);
    if (confirmDeleteBtn) confirmDeleteBtn.addEventListener('click', confirmDeleteAgent);
    
    document.querySelectorAll('.close-modal').forEach(btn => {
        btn.addEventListener('click', () => {
            document.getElementById('agent-response-modal').style.display = 'none';
            document.getElementById('agent-edit-modal').style.display = 'none';
            document.getElementById('delete-confirm-modal').style.display = 'none';
        });
    });
    
    const providerSelect = document.getElementById('agent-provider');
    if (providerSelect) {
        providerSelect.addEventListener('change', actualizarModelosDisponibles);
        actualizarModelosDisponibles();
    }
    
    checkConnection();
    setInterval(checkConnection, HUD_CONFIG.timing.connectionCheck);
};
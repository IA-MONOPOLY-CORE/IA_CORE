(function () {
    'use strict';

    const SELECTED = 'selected';
    const FOCUSED = 'focused';
    const EXPANDED = 'expanded';
    const COLLAPSED = 'collapsed';

    function stateTokens(element) {
        return new Set((element.dataset.interactionState || '').split(/\s+/).filter(Boolean));
    }

    function setState(element, state, enabled) {
        if (!element) return;
        const states = stateTokens(element);
        if (enabled) states.add(state);
        else states.delete(state);
        element.dataset.interactionState = Array.from(states).join(' ');
    }

    function selectFlowStep(step, moveFocus) {
        const target = document.querySelector(`[data-flow-step="${step}"]`);
        if (!target) return;

        document.querySelectorAll('[data-flow-step]').forEach((panel) => {
            setState(panel, SELECTED, panel === target);
            setState(panel, FOCUSED, false);
        });
        document.querySelectorAll('[data-focus-step]').forEach((control) => {
            control.setAttribute('aria-pressed', String(control.dataset.focusStep === step));
        });

        if (!moveFocus) return;
        setState(target, FOCUSED, true);
        target.setAttribute('tabindex', '-1');
        target.scrollIntoView({
            behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
            block: 'start',
        });
        target.focus({ preventScroll: true });
    }

    function sourceText(sourceId) {
        const source = document.getElementById(sourceId);
        if (!source) return 'not_available';
        const childValues = Array.from(source.children)
            .map((child) => child.textContent.trim())
            .filter(Boolean);
        return childValues.length > 0
            ? childValues.join(', ')
            : source.textContent.trim() || 'not_available';
    }

    function syncInspector() {
        document.querySelectorAll('[data-inspector-source]').forEach((field) => {
            field.textContent = sourceText(field.dataset.inspectorSource);
        });
    }

    function bindFlowFocus() {
        document.querySelectorAll('[data-focus-step]').forEach((control) => {
            control.addEventListener('click', () => selectFlowStep(control.dataset.focusStep, true));
        });
        document.querySelectorAll('[data-flow-step]').forEach((panel) => {
            panel.addEventListener('blur', () => setState(panel, FOCUSED, false));
        });
        selectFlowStep('readiness', false);
    }

    function bindInspector() {
        const inspector = document.getElementById('contract-read-only-inspector');
        if (!inspector) return;

        const disclosure = inspector.querySelector('.inspector-disclosure');
        inspector.addEventListener('toggle', () => {
            setState(inspector, EXPANDED, inspector.open);
            setState(inspector, COLLAPSED, !inspector.open);
            if (disclosure) disclosure.textContent = inspector.open ? 'Ocultar detalle' : 'Ver detalle';
            if (inspector.open) syncInspector();
        });

        const observer = new MutationObserver(syncInspector);
        ['contract-core-rail', 'functional-widgets'].forEach((id) => {
            const source = document.querySelector(`.${id}`) || document.getElementById(id);
            if (source) observer.observe(source, { childList: true, characterData: true, subtree: true });
        });
        window.addEventListener('ia-core-backend-internal-payloads-updated', syncInspector);
        syncInspector();
    }

    function bindRequestDisclosure() {
        const panel = document.getElementById('debate-panel');
        const control = document.getElementById('debate-toggle');
        if (!panel || !control) return;

        const syncDisclosure = () => {
            const collapsed = panel.classList.contains('collapsed');
            control.setAttribute('aria-expanded', String(!collapsed));
            setState(control, COLLAPSED, collapsed);
            setState(control, EXPANDED, !collapsed);
        };
        control.addEventListener('keydown', (event) => {
            if (event.key !== 'Enter' && event.key !== ' ') return;
            event.preventDefault();
            control.click();
        });
        new MutationObserver(syncDisclosure).observe(panel, {
            attributes: true,
            attributeFilter: ['class'],
        });
        syncDisclosure();
    }

    function init() {
        bindFlowFocus();
        bindInspector();
        bindRequestDisclosure();
    }

    window.iaCoreConsoleInteractions = Object.freeze({
        init,
        selectFlowStep,
        syncInspector,
    });

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init, { once: true });
    } else {
        init();
    }
})();

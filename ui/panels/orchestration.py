from __future__ import annotations

import config
import streamlit as st

from ui.i18n import t
from ui.state import cache
from ui.state.manager import UIStateManager

_MODE_VALUES = ["sequential", "debate"]


def render(state: UIStateManager) -> None:
    st.subheader(t("orch.title"))
    ttl = getattr(config, "UI_CACHE_TTL_SAFE", 300) if config.SAFE_MODE else 30
    agents_list = cache.get("agents", state.service.list_agents, ttl=ttl)
    agent_ids = [a["id"] for a in agents_list]

    task = st.text_area(
        t("orch.task"),
        height=120,
        placeholder=t("orch.task_placeholder"),
    )
    mode = st.selectbox(
        t("orch.mode"),
        _MODE_VALUES,
        index=0,
        format_func=lambda value: t(f"orch.mode.{value}"),
    )
    if mode == "debate":
        st.warning(t("orch.debate_warning"))
        st.caption(t("orch.debate_agents_hint"))

    selected = st.multiselect(
        t("orch.agents"),
        agent_ids,
        default=[a for a in ["analyst", "critic", "optimizer"] if a in agent_ids],
        disabled=(mode == "debate"),
    )

    if st.button(t("orch.execute"), type="primary", key="run_orch"):
        if not task.strip():
            st.warning(t("orch.task_empty"))
            return

        with st.spinner(t("orch.running")):
            result = state.service.run_orchestration(
                task.strip(),
                mode,
                selected or None,
            )
        payload = state.service.orchestration_result_to_dict(result)
        state.set_last_orchestration(payload)
        cache.invalidate("overview")
        cache.invalidate("orch_history")

        st.success(
            t(
                "orch.done",
                success=result.success,
                ms=f"{result.duration_ms:.0f}",
                id=result.execution_id,
            )
        )

        if result.scores_summary:
            st.markdown(t("orch.scores"))
            st.json(result.scores_summary)

        for step in result.steps:
            status = t("orch.step.ok") if step.success else t("orch.step.err")
            label = t(
                "orch.step",
                agent=step.agent_name,
                status=status,
                ms=f"{step.duration_ms:.0f}",
            )
            with st.expander(label):
                if step.score:
                    st.write(t("orch.score"), step.score)
                if step.success:
                    out = step.result
                    if isinstance(out, dict) and "output" in out:
                        st.write(out["output"])
                    else:
                        st.json(out)
                else:
                    st.error(step.error or t("orch.step.err"))

        if result.debate and result.debate.final_response:
            st.markdown(t("orch.synthesis"))
            st.write(result.debate.final_response.get("synthesis", ""))

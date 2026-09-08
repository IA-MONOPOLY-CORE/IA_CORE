"""N6 post-direction execution graph tests for UI/UX 1.199."""

from ui_ux_panel_maestro_microcopy_1_199_support import (
    execution_graph_summary,
    post_direction_execution_graph,
    protected_product_is_unchanged,
)


def test_n6_graphs_have_exact_station_counts_and_order():
    graph = post_direction_execution_graph()
    assert len(graph) == 11
    assert [item.station_id for item in graph[:2]] == ["A1", "A2"]
    assert [item.station_index for item in graph[2:]] == list(range(1, 10))
    assert graph[-1].frontier == "HARD_FRONTIER: requiere cambio contractual y owner separado."


def test_n6_graph_summary_is_frozen():
    assert execution_graph_summary() == {
        "CURRENT_AUTOMATABLE_STATION_COUNT": 2,
        "POST_DIRECTION_DETERMINISTIC_STATION_COUNT": 8,
        "PREAUTHORIZED_POST_DIRECTION_STATION_COUNT": 3,
        "SELF_BOOTSTRAPPED_POST_DIRECTION_STATION_COUNT": 1,
        "NEXT_HARD_FRONTIER_INDEX": 9,
    }


def test_n6_every_station_has_operational_guardrails():
    for station in post_direction_execution_graph():
        assert station.files and station.tests
        assert station.gate and station.commit_prefix
        assert station.rollback and station.frontier
        assert station.occurrence_count >= 0


def test_n6_product_is_unchanged():
    assert protected_product_is_unchanged()

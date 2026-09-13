from app.safety.risk_engine import risk_engine

def test_risk_classification():
    # Low risk
    assert risk_engine.assess_risk("restart_service").risk_level == "LOW"
    assert risk_engine.assess_risk("clear_cache").risk_level == "LOW"
    assert risk_engine.assess_risk("get_service_health").risk_level == "LOW"

    # Medium risk
    assert risk_engine.assess_risk("route_traffic").risk_level == "MEDIUM"
    assert risk_engine.assess_risk("scale_service").risk_level == "MEDIUM"
    assert risk_engine.assess_risk("rollback_deployment").risk_level == "MEDIUM"

    # High risk
    assessment_failover = risk_engine.assess_risk("failover_service")
    assert assessment_failover.risk_level == "HIGH"
    assert assessment_failover.requires_approval is True

    assessment_backup = risk_engine.assess_risk("restore_backup")
    assert assessment_backup.risk_level == "HIGH"
    assert assessment_backup.requires_approval is True

    # Critical risk
    assessment_delete = risk_engine.assess_risk("delete_data")
    assert assessment_delete.risk_level == "CRITICAL"
    assert assessment_delete.requires_approval is True

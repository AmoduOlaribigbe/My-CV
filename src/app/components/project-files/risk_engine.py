"""
SecureVigil Risk Engine
Vulnerability risk classification and remediation recommendations
"""

from typing import Dict, List

# Risk classification constants
HIGH_RISK_PORTS = [21, 23, 25, 445, 1433, 3306, 3389, 5432, 5900, 6379]
MEDIUM_RISK_PORTS = [80, 139, 443, 8080, 8443]
HIGH_RISK_SERVICES = ["telnet", "ftp", "smb", "rdp", "mysql", "postgresql", "vnc", "redis"]
UNENCRYPTED_SERVICES = ["http", "ftp", "telnet", "smtp"]


def classify_risk(port: int, service: str, version: str = "") -> str:
    """
    Classify vulnerability risk level based on port, service, and version
    
    Args:
        port: Port number
        service: Service name
        version: Service version (optional)
    
    Returns:
        Risk level: "HIGH", "MEDIUM", or "LOW"
    """
    service_lower = service.lower()
    
    # Check for high-risk ports
    if port in HIGH_RISK_PORTS:
        return "HIGH"
    
    # Check for high-risk services
    if any(risky in service_lower for risky in HIGH_RISK_SERVICES):
        return "HIGH"
    
    # Check for unencrypted protocols on standard ports
    if service_lower in UNENCRYPTED_SERVICES:
        return "MEDIUM"
    
    # Check for medium-risk ports
    if port in MEDIUM_RISK_PORTS:
        return "MEDIUM"
    
    # Check for outdated versions (basic heuristic)
    if version:
        outdated_indicators = ["1.0", "2.0", "legacy", "old", "deprecated"]
        if any(indicator in version.lower() for indicator in outdated_indicators):
            return "MEDIUM"
    
    # Default to low risk
    return "LOW"


def get_recommendation(item: Dict) -> str:
    """
    Provide remediation recommendations based on finding
    
    Args:
        item: Scan result dictionary
    
    Returns:
        Remediation recommendation string
    """
    risk_level = item.get("risk", "LOW")
    service = item.get("service", "unknown")
    port = item.get("port", 0)
    
    recommendations = {
        "HIGH": {
            "telnet": "URGENT: Disable Telnet and use SSH instead",
            "ftp": "URGENT: Disable FTP or use SFTP/FTPS with encryption",
            "smb": "URGENT: Restrict SMB access, apply patches, use SMBv3",
            "rdp": "URGENT: Restrict RDP access, use VPN, enable NLA",
            "mysql": "URGENT: Restrict database access to localhost or VPN only",
            "postgresql": "URGENT: Restrict database access to localhost or VPN only",
            "default": f"URGENT: Disable or restrict {service} on port {port}"
        },
        "MEDIUM": {
            "http": f"Review and consider enabling HTTPS for {service}",
            "default": f"Review and harden {service} configuration"
        },
        "LOW": {
            "default": f"Monitor {service} for updates and security advisories"
        }
    }
    
    risk_recommendations = recommendations.get(risk_level, recommendations["LOW"])
    return risk_recommendations.get(service, risk_recommendations["default"])


def get_cvss_estimate(risk_level: str) -> float:
    """
    Provide estimated CVSS score based on risk level
    
    Args:
        risk_level: "HIGH", "MEDIUM", or "LOW"
    
    Returns:
        Estimated CVSS score (0-10)
    """
    cvss_mapping = {
        "HIGH": 7.5,
        "MEDIUM": 5.0,
        "LOW": 2.0
    }
    return cvss_mapping.get(risk_level, 0.0)


def apply_risk(results: List[Dict]) -> List[Dict]:
    """
    Apply risk classification to all scan results
    
    Args:
        results: List of scan results
    
    Returns:
        Results with risk classification and recommendations added
    """
    for item in results:
        item["risk"] = classify_risk(
            item.get("port", 0),
            item.get("service", ""),
            item.get("version", "")
        )
        item["recommendation"] = get_recommendation(item)
        item["cvss_estimate"] = get_cvss_estimate(item["risk"])
    
    # Sort by risk level (HIGH -> MEDIUM -> LOW)
    risk_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    results.sort(key=lambda x: risk_order.get(x["risk"], 3))
    
    return results


def generate_risk_summary(results: List[Dict]) -> Dict:
    """
    Generate executive summary statistics
    
    Args:
        results: List of scan results with risk classification
    
    Returns:
        Dictionary with summary statistics
    """
    summary = {
        "total": len(results),
        "high": sum(1 for r in results if r.get("risk") == "HIGH"),
        "medium": sum(1 for r in results if r.get("risk") == "MEDIUM"),
        "low": sum(1 for r in results if r.get("risk") == "LOW"),
        "hosts": len(set(r.get("host") for r in results)),
    }
    
    # Calculate risk score (weighted average)
    risk_weights = {"HIGH": 10, "MEDIUM": 5, "LOW": 1}
    total_risk_score = sum(
        risk_weights.get(r.get("risk", "LOW"), 0) for r in results
    )
    summary["risk_score"] = total_risk_score
    
    # Calculate percentages
    if summary["total"] > 0:
        summary["high_percent"] = round(summary["high"] / summary["total"] * 100, 1)
        summary["medium_percent"] = round(summary["medium"] / summary["total"] * 100, 1)
        summary["low_percent"] = round(summary["low"] / summary["total"] * 100, 1)
    else:
        summary["high_percent"] = 0
        summary["medium_percent"] = 0
        summary["low_percent"] = 0
    
    return summary


def get_priority_findings(results: List[Dict], limit: int = 10) -> List[Dict]:
    """
    Get top priority vulnerabilities for immediate attention
    
    Args:
        results: List of scan results
        limit: Maximum number of findings to return
    
    Returns:
        List of highest priority findings
    """
    high_risk = [r for r in results if r.get("risk") == "HIGH"]
    return high_risk[:limit]


if __name__ == "__main__":
    # Example usage
    sample_results = [
        {"host": "192.168.1.10", "port": 23, "service": "telnet", "version": ""},
        {"host": "192.168.1.10", "port": 80, "service": "http", "version": "Apache 2.4"},
        {"host": "192.168.1.10", "port": 443, "service": "https", "version": "nginx 1.18"},
    ]
    
    # Apply risk classification
    classified = apply_risk(sample_results)
    
    # Generate summary
    summary = generate_risk_summary(classified)
    
    print("Risk Summary:")
    print(f"  Total Findings: {summary['total']}")
    print(f"  High Risk: {summary['high']} ({summary['high_percent']}%)")
    print(f"  Medium Risk: {summary['medium']} ({summary['medium_percent']}%)")
    print(f"  Low Risk: {summary['low']} ({summary['low_percent']}%)")
    print(f"  Risk Score: {summary['risk_score']}")
    
    print("\nDetailed Findings:")
    for item in classified:
        print(f"\n[{item['risk']}] {item['host']}:{item['port']} - {item['service']}")
        print(f"  {item['recommendation']}")

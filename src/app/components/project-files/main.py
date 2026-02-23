"""
SecureVigil Main CLI
Command-line interface for vulnerability scanning
"""

import argparse
from datetime import datetime
from scanner import scan_target
from risk_engine import apply_risk, generate_risk_summary, get_priority_findings
from database import init_db, save_scan
from email_alert import send_alert, should_send_alert
import json


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="SecureVigil - Enterprise Vulnerability Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan single host
  python main.py 192.168.1.10

  # Scan network range
  python main.py 192.168.1.0/24

  # Scan with custom Nmap arguments
  python main.py 192.168.1.10 --scan-args "-sV -T5 -p-"

  # Save results to JSON
  python main.py 192.168.1.10 --output results.json

  # Skip email alerts
  python main.py 192.168.1.10 --no-alert

  # Add notes to scan
  python main.py 192.168.1.10 --notes "Monthly security audit"
        """
    )
    
    parser.add_argument(
        "target",
        help="Target IP address or CIDR range (e.g., 192.168.1.10 or 192.168.1.0/24)"
    )
    
    parser.add_argument(
        "--scan-args",
        default="-sV -T4",
        help="Nmap scan arguments (default: -sV -T4)"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Save results to JSON file"
    )
    
    parser.add_argument(
        "--no-db",
        action="store_true",
        help="Skip database storage"
    )
    
    parser.add_argument(
        "--no-alert",
        action="store_true",
        help="Skip email alerts"
    )
    
    parser.add_argument(
        "--notes",
        help="Add notes to scan record"
    )
    
    parser.add_argument(
        "--init-db",
        action="store_true",
        help="Initialize database and exit"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Initialize database if requested
    if args.init_db:
        print("[*] Initializing database...")
        init_db()
        print("[+] Database initialized successfully")
        return
    
    # Print banner
    print_banner()
    
    # Perform scan
    print(f"\n[*] Target: {args.target}")
    print(f"[*] Scan Arguments: {args.scan_args}")
    print(f"[*] Scan started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    start_time = datetime.now()
    
    # Execute scan
    results = scan_target(args.target, args.scan_args)
    
    if not results:
        print("\n[!] No services discovered or scan failed")
        return
    
    # Apply risk classification
    print("\n[*] Analyzing risks...")
    results = apply_risk(results)
    
    # Generate summary
    summary = generate_risk_summary(results)
    
    scan_duration = (datetime.now() - start_time).total_seconds()
    
    # Print results
    print_results(results, summary, scan_duration, args.verbose)
    
    # Save to database
    if not args.no_db:
        print("\n[*] Saving to database...")
        init_db()  # Ensure database exists
        scan_id = save_scan(results, args.target, notes=args.notes)
        print(f"[+] Scan ID: {scan_id}")
    
    # Save to JSON if requested
    if args.output:
        print(f"\n[*] Saving to {args.output}...")
        output_data = {
            "scan_info": {
                "target": args.target,
                "scan_date": datetime.now().isoformat(),
                "scan_duration": scan_duration,
                "notes": args.notes
            },
            "summary": summary,
            "results": results
        }
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"[+] Results saved to {args.output}")
    
    # Send email alert if high-risk findings
    if not args.no_alert and should_send_alert(summary):
        print("\n[!] High-risk vulnerabilities detected - sending alert...")
        priority_findings = get_priority_findings(results, limit=10)
        if send_alert(summary, priority_findings):
            print("[+] Alert email sent successfully")
        else:
            print("[!] Alert email failed (check configuration)")
    
    print("\n" + "=" * 60)
    print("[+] Scan complete!")
    print("=" * 60)


def print_banner():
    """Print application banner"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                      SecureVigil                          ║
║           Enterprise Vulnerability Scanner                ║
║                                                           ║
║              Developed by Olaribigbe Amodu                ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_results(results, summary, duration, verbose=False):
    """Print scan results to console"""
    print("\n" + "=" * 60)
    print("SCAN RESULTS")
    print("=" * 60)
    
    print(f"\n📊 Summary:")
    print(f"  Total Findings: {summary['total']}")
    print(f"  High Risk:      {summary['high']} ({summary['high_percent']}%)")
    print(f"  Medium Risk:    {summary['medium']} ({summary['medium_percent']}%)")
    print(f"  Low Risk:       {summary['low']} ({summary['low_percent']}%)")
    print(f"  Hosts Scanned:  {summary['hosts']}")
    print(f"  Risk Score:     {summary['risk_score']}")
    print(f"  Duration:       {duration:.2f} seconds")
    
    # Print high-risk findings
    high_risk = [r for r in results if r.get("risk") == "HIGH"]
    if high_risk:
        print(f"\n🚨 HIGH RISK FINDINGS ({len(high_risk)}):")
        print("-" * 60)
        for finding in high_risk:
            print(f"\n  [{finding['host']}:{finding['port']}] {finding['service']}")
            if finding.get('product'):
                print(f"    Product: {finding['product']} {finding.get('version', '')}")
            print(f"    ⚠️  {finding.get('recommendation', 'Review immediately')}")
    
    # Print medium-risk findings if verbose
    if verbose:
        medium_risk = [r for r in results if r.get("risk") == "MEDIUM"]
        if medium_risk:
            print(f"\n⚠️  MEDIUM RISK FINDINGS ({len(medium_risk)}):")
            print("-" * 60)
            for finding in medium_risk:
                print(f"\n  [{finding['host']}:{finding['port']}] {finding['service']}")
                if finding.get('product'):
                    print(f"    Product: {finding['product']} {finding.get('version', '')}")
                print(f"    💡 {finding.get('recommendation', 'Review configuration')}")
    
    # Print all findings if very verbose
    if verbose:
        low_risk = [r for r in results if r.get("risk") == "LOW"]
        if low_risk:
            print(f"\n✓ LOW RISK FINDINGS ({len(low_risk)}):")
            print("-" * 60)
            for finding in low_risk:
                print(f"  [{finding['host']}:{finding['port']}] {finding['service']}", end="")
                if finding.get('product'):
                    print(f" - {finding['product']} {finding.get('version', '')}", end="")
                print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        exit(1)

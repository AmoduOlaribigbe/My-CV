"""
SecureVigil Scanner Module
Network vulnerability scanning using Nmap
"""

import nmap
import json
from typing import List, Dict, Optional


class VulnerabilityScanner:
    """Main scanner class for network vulnerability detection"""
    
    def __init__(self):
        self.nm = nmap.PortScanner()
    
    def scan_target(self, target: str, scan_type: str = "-sV -T4") -> List[Dict]:
        """
        Perform network scan on target
        
        Args:
            target: IP address or CIDR range (e.g., "192.168.1.1" or "192.168.1.0/24")
            scan_type: Nmap scan arguments (default: -sV -T4)
        
        Returns:
            List of discovered services with details
        """
        print(f"[*] Starting scan on {target}...")
        
        try:
            self.nm.scan(target, arguments=scan_type)
        except Exception as e:
            print(f"[!] Scan error: {e}")
            return []

        results = []

        for host in self.nm.all_hosts():
            host_info = {
                "state": self.nm[host].state(),
                "hostname": self.nm[host].hostname()
            }
            
            for proto in self.nm[host].all_protocols():
                ports = self.nm[host][proto].keys()

                for port in ports:
                    service = self.nm[host][proto][port]
                    results.append({
                        "host": host,
                        "hostname": host_info["hostname"],
                        "port": port,
                        "protocol": proto,
                        "service": service["name"],
                        "product": service.get("product", ""),
                        "version": service.get("version", ""),
                        "extrainfo": service.get("extrainfo", ""),
                        "state": service["state"]
                    })

        print(f"[+] Scan complete. Found {len(results)} services on {len(self.nm.all_hosts())} hosts")
        return results


def scan_target(target: str, scan_type: str = "-sV -T4") -> List[Dict]:
    """
    Convenience function for quick scanning
    
    Args:
        target: IP address or CIDR range
        scan_type: Nmap scan arguments
    
    Returns:
        List of scan results
    """
    scanner = VulnerabilityScanner()
    return scanner.scan_target(target, scan_type)


def scan_and_save(target: str, output_file: Optional[str] = None) -> List[Dict]:
    """
    Scan target and optionally save results to JSON
    
    Args:
        target: IP address or CIDR range
        output_file: Optional JSON output file path
    
    Returns:
        List of scan results
    """
    results = scan_target(target)
    
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"[+] Results saved to {output_file}")
    
    return results


if __name__ == "__main__":
    # Example usage
    target = input("Enter target IP or CIDR range: ")
    results = scan_target(target)
    
    print("\n" + "="*60)
    print("SCAN RESULTS")
    print("="*60)
    
    for item in results:
        print(f"\n[{item['host']}:{item['port']}] {item['service']}")
        if item['product']:
            print(f"  Product: {item['product']} {item['version']}")

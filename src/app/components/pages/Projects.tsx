import { Shield, Network, Cloud, Code, Lock, Server, Terminal, Database } from "lucide-react";
import { Badge } from "../ui/badge";
import { Link } from "react-router";
import { Button } from "../ui/button";

export function Projects() {
  const projects = [
    {
      title: "SecureVigil - Enterprise Vulnerability Scanner",
      category: "Production-Grade Cybersecurity Platform",
      icon: Shield,
      featured: true,
      description: "Complete enterprise vulnerability scanning system with Flask dashboard, SQLite persistence, automated email alerts, historical trend analysis, and Azure cloud deployment with CI/CD pipeline.",
      technologies: ["Python", "Flask", "Nmap", "SQLite", "Docker", "Azure", "CI/CD"],
      outcomes: [
        "Reduced vulnerability scanning time from 4 hours to 15 minutes",
        "Automated executive reporting with risk prioritization",
        "Implemented real-time email alerting for high-risk findings",
        "Deployed production system on Azure with 99.9% uptime",
        "Created CI/CD pipeline with automated testing",
      ],
      proof: "Full Source Code | Live Demo | Architecture Documentation | Azure Deployment",
      link: "/projects/securevigil"
    },
    {
      title: "Ransomware Simulation & Key Recovery Lab",
      category: "Cybersecurity Education & Training",
      icon: Lock,
      featured: true,
      description: "Educational ransomware simulation demonstrating encryption mechanics, brute force vulnerabilities, and incident response procedures. Validates AIG cyber simulation experience with hands-on cryptography implementation.",
      technologies: ["Python", "Cryptography", "Brute Force", "Incident Response", "CEH"],
      outcomes: [
        "Trained 150+ students in ransomware defense strategies",
        "Demonstrated weak vs. strong key cryptography concepts",
        "Created realistic incident response scenarios",
        "Developed automated decryption and recovery workflows",
        "Integrated into CEH and forensics curriculum",
      ],
      proof: "Lab Documentation | Training Materials | Simulation Screenshots | Student Certification Results",
    },
    {
      title: "Multi-VLAN Enterprise Network Infrastructure",
      category: "Network Security & Infrastructure",
      icon: Network,
      featured: true,
      description: "Complete enterprise network segmentation with router-on-a-stick configuration, DHCP services per VLAN, ACLs for security, and guest network isolation. Demonstrates advanced Cisco networking and security architecture.",
      technologies: ["Cisco IOS", "VLANs", "ACLs", "DHCP", "Network Segmentation", "Packet Tracer"],
      outcomes: [
        "Designed 4-VLAN architecture for 250+ endpoints",
        "Implemented security policies preventing unauthorized inter-VLAN traffic",
        "Isolated guest network from sensitive internal resources",
        "Configured automated DHCP with proper DNS settings",
        "Achieved 99.8% network uptime in production deployment",
      ],
      proof: "Packet Tracer File | Configuration Scripts | Network Diagram | Security Policy Documentation",
    },
    {
      title: "Azure Secure Cloud Architecture",
      category: "Cloud Infrastructure & DevOps",
      icon: Cloud,
      featured: true,
      description: "Production-grade Azure deployment with WAF, NSGs, private endpoints, Azure Bastion, automated backups, and comprehensive monitoring. Demonstrates enterprise cloud security architecture aligned with Azure Solutions Architect certification.",
      technologies: ["Azure", "ARM Templates", "NSGs", "Key Vault", "Bastion", "Log Analytics", "Site Recovery"],
      outcomes: [
        "Deployed secure multi-tier architecture with zero public IPs on VMs",
        "Implemented WAF with OWASP rule sets blocking 500+ attacks/month",
        "Configured automated backup and DR with 2-hour RTO",
        "Reduced infrastructure costs by 40% through reserved instances",
        "Achieved 99.95% uptime with auto-scaling and load balancing",
      ],
      proof: "Architecture Diagrams | Cost Analysis | ARM Templates | Security Assessment Report",
    },
    {
      title: "IT Asset Management Dashboard",
      category: "Enterprise IT Operations",
      icon: Database,
      featured: true,
      description: "Flask-based asset tracking system for 250+ CBT systems with automated maintenance alerts, warranty tracking, CSV export, and comprehensive reporting. Validates IT leadership and systems administration experience.",
      technologies: ["Python", "Flask", "SQLite", "HTML/CSS", "REST API", "Automated Alerts"],
      outcomes: [
        "Tracked 250+ assets across multiple lab locations",
        "Automated maintenance scheduling reducing downtime by 35%",
        "Implemented warranty expiry alerts preventing 12+ support lapses",
        "Generated executive reports for budget planning",
        "Reduced asset procurement time by 50% through accurate inventory",
      ],
      proof: "Live Dashboard | Sample Reports | Database Schema | API Documentation",
    },
  ];

  return (
    <div className="py-8 space-y-8">
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
          Portfolio Projects
        </h1>
        <p className="text-xl text-gray-300 max-w-3xl mx-auto">
          Production-grade projects demonstrating cybersecurity, infrastructure, and automation expertise 
          with real-world business impact and documented proof of work.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {projects.map((project, index) => {
          const Icon = project.icon;
          return (
            <div
              key={index}
              className={`bg-slate-800/50 backdrop-blur-sm border rounded-lg p-6 transition-all hover:scale-[1.02] ${
                project.featured 
                  ? "border-blue-500/60 shadow-lg shadow-blue-500/20 lg:col-span-2" 
                  : "border-blue-500/20 hover:border-blue-500/40"
              }`}
            >
              {project.featured && (
                <div className="mb-4">
                  <Badge className="bg-gradient-to-r from-blue-500 to-purple-500 text-white border-0">
                    ⭐ Featured Project
                  </Badge>
                </div>
              )}
              <div className="flex items-start gap-4 mb-4">
                <div className={`p-3 rounded-lg ${
                  project.featured ? "bg-blue-500/30" : "bg-blue-500/20"
                }`}>
                  <Icon className={`w-8 h-8 ${
                    project.featured ? "text-blue-300" : "text-blue-400"
                  }`} />
                </div>
                <div className="flex-1">
                  <h3 className={`font-semibold text-white mb-2 ${
                    project.featured ? "text-2xl" : "text-xl"
                  }`}>
                    {project.title}
                  </h3>
                  <p className="text-sm text-blue-300">{project.category}</p>
                </div>
              </div>

              <p className="text-gray-300 mb-4">{project.description}</p>

              <div className="mb-4">
                <h4 className="text-sm font-semibold text-white mb-2">Technologies:</h4>
                <div className="flex flex-wrap gap-2">
                  {project.technologies.map((tech, i) => (
                    <Badge key={i} variant="secondary" className="bg-slate-700 text-gray-300">
                      {tech}
                    </Badge>
                  ))}
                </div>
              </div>

              <div className="mb-4">
                <h4 className="text-sm font-semibold text-white mb-2">Key Outcomes:</h4>
                <ul className="space-y-1">
                  {project.outcomes.map((outcome, i) => (
                    <li key={i} className="flex gap-2 text-sm text-gray-300">
                      <span className="text-green-400 mt-1 flex-shrink-0">✓</span>
                      <span>{outcome}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="pt-4 border-t border-slate-700">
                <h4 className="text-xs font-semibold text-gray-400 mb-1">Proof of Work:</h4>
                <p className="text-xs text-gray-500 mb-3">{project.proof}</p>
                {project.link && (
                  <Button asChild className="bg-blue-600 hover:bg-blue-700">
                    <Link to={project.link}>View Full Project Details</Link>
                  </Button>
                )}
              </div>
            </div>
          );
        })}
      </div>

      <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-6 text-center">
        <h3 className="text-xl font-semibold text-white mb-2">
          Additional Projects & Documentation
        </h3>
        <p className="text-gray-300 mb-4">
          Comprehensive project files, code samples, configuration scripts, and technical documentation 
          available on GitHub. All projects include setup instructions, security considerations, and lessons learned.
        </p>
        <div className="flex gap-4 justify-center flex-wrap">
          <a 
            href="https://github.com/olaribigbeamodu" 
            target="_blank" 
            rel="noopener noreferrer"
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
          >
            View GitHub Profile
          </a>
          <Link to="/contact">
            <button className="px-6 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors">
              Request Project Details
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}
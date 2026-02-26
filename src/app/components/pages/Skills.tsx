import { Award, CheckCircle } from "lucide-react";

export function Skills() {
  const skillCategories = [
    {
      category: "Cybersecurity & Forensics Tools",
      skills: [
        "Wireshark", "Nmap", "Burp Suite", "Metasploit", "SQLMap", "FTK Imager",
        "Autopsy", "Nessus", "CEH Toolkit", "OWASP ZAP", "Volatility", "Kali Linux",
        "LAN/WAN Configuration", "TCP/IP, UDP/IP, DNS", "Windows Server Administration"
      ],
    },
    {
      category: "Cloud & Infrastructure",
      skills: [
        "Microsoft Azure (IaaS, PaaS)", "Google Cloud Platform", "Docker", "Kubernetes",
        "Terraform", "Cloud-Based Backup & Recovery", "Planning, Virtualization"
      ],
    },
    {
      category: "Programming & Scripting",
      skills: [
        "Python (Advanced)", "C, C++, Java", "Bash", "PowerShell", "HTML/CSS", "JavaScript"
      ],
    },
    {
      category: "Data & Analytics Tools",
      skills: [
        "Excel (Advanced)", "Pandas", "Seaborn", "Matplotlib", "SQL", "MySQL"
      ],
    },
    {
      category: "Project & Business Tools",
      skills: [
        "Google Suite", "MS Office", "Project Management",
        "Production Tools (Graphics, Animation, Video Editing)",
        "Business Presentations", "Negotiation & Stakeholder Engagement"
      ],
    },
  ];

  const certifications = [
  { name: "Machine Learning for Application in Digital Forensics", issuer: "Codered (EC Council)", status: "In View", year: "2026" },
  { name: "AI for Cybersecurity & Bug Bounty Hunting", issuer: "Codered (EC Council)", status: "In View", year: "2026" },
  { name: "Red Team Mastery: Advanced Offensive Security", issuer: "Codered (EC Council)", status: "Certified", year: "2026" },
  { name: "Cybersecurity for Businesses", issuer: "EC Council", status: "Certified", year: "2025" },
  { name: "Ethical Hacking", issuer: "Cisco", status: "Certified", year: "2025" },

  { name: "Ethical Hacking", issuer: "Aptech Computer Education", status: "Certified", year: "2025" },
  { name: "Security Architecture & Hacking", issuer: "Aptech Computer Education", status: "Certified", year: "2025" },
  { name: "Security Programming with Python (Advanced)", issuer: "Aptech Computer Education", status: "Certified", year: "2025" },
  { name: "Penetration Testing Services", issuer: "Aptech Computer Education", status: "Certified", year: "2025" },
  { name: "Cybersecurity Operations Fundamentals", issuer: "Aptech Computer Education", status: "Certified", year: "2025" },

  { name: "Implementing Network Security", issuer: "Aptech Computer Education", status: "Certified", year: "2025" },
  { name: "Enterprise Network Core Technologies", issuer: "Aptech Computer Education", status: "Certified", year: "2025" },

  { name: "Implementing, Managing & Monitoring Azure Environment", issuer: "Aptech Computer Education", status: "Certified", year: "2025" },
  { name: "Azure Architect Technologies", issuer: "Aptech Computer Education", status: "Certified", year: "2025" },
  { name: "Azure Solutions Architect Design", issuer: "Aptech Computer Education", status: "Certified", year: "2025" },

  { name: "Fundamentals of Red Hat System Administration", issuer: "Aptech Computer Education", status: "Certified", year: "2025" },
  { name: "Securing Mobile Devices", issuer: "Aptech Computer Education", status: "Certified", year: "2025" },
  { name: "Fundamentals of JavaScript", issuer: "Aptech Computer Education", status: "Certified", year: "2025" }
];


  const keySkills = [
    "Applied Python Programming",
    "Vulnerability Triage",
    "Ethical Hacking",
    "Security Analysis",
    "CISA - NIST, Alice",
    "Multimedia Production Tools (Graphics, Animation, Video Editing)",
    "Data Analysis",
    "Problem-Solving",
    "Communication",
    "Strategy"
  ];

  return (
    <div className="py-8 space-y-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
          Technical Skills & Certifications
        </h1>
        <p className="text-xl text-gray-300">
          Comprehensive expertise across cybersecurity, infrastructure, and development
        </p>
      </div>

      {/* Technical Skills */}
      <section>
        <h2 className="text-3xl font-bold text-white mb-6">Technical Skills</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {skillCategories.map((category, index) => (
            <div
              key={index}
              className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6"
            >
              <h3 className="text-xl font-semibold text-blue-300 mb-4">
                {category.category}
              </h3>
              <div className="flex flex-wrap gap-2">
                {category.skills.map((skill, i) => (
                  <span
                    key={i}
                    className="px-3 py-1 bg-slate-700/50 border border-slate-600 rounded-full text-sm text-gray-300 hover:border-blue-500/40 transition-colors"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Key Applied Skills */}
      <section className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6">
        <h2 className="text-2xl font-bold text-white mb-4">Key Applied Skills</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {keySkills.map((skill, index) => (
            <div
              key={index}
              className="flex items-center gap-2 text-gray-300"
            >
              <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0" />
              <span className="text-sm">{skill}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Certifications */}
      <section>
        <h2 className="text-3xl font-bold text-white mb-6 flex items-center gap-3">
          <Award className="w-8 h-8 text-yellow-400" />
          Certifications & Credentials
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {certifications.map((cert, index) => (
            <div
              key={index}
              className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-4 hover:border-blue-500/40 transition-colors"
            >
              <div className="flex items-start gap-3">
                <Award className="w-6 h-6 text-blue-400 mt-1 flex-shrink-0" />
                <div className="flex-1">
                  <h3 className="font-semibold text-white mb-1">{cert.name}</h3>
                  <p className="text-sm text-gray-400 mb-2">{cert.issuer}</p>
                  <div className="flex items-center gap-2">
                    <span
                      className={`text-xs px-2 py-1 rounded ${
                        cert.status === "Certified"
                          ? "bg-green-500/20 text-green-300"
                          : "bg-yellow-500/20 text-yellow-300"
                      }`}
                    >
                      {cert.status}
                    </span>
                    {cert.year && (
                      <span className="text-xs text-gray-500">{cert.year}</span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Education */}
      {/*
      <section className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6">
        <h2 className="text-2xl font-bold text-white mb-4">Education</h2>
        <div className="space-y-4">
          <div>
            <h3 className="text-xl font-semibold text-blue-300">
              Degree in Economics (MIVA Open University) — In View
            </h3>
            <p className="text-gray-400">Undergraduate Studies</p>
          </div>
          <div>
            <h3 className="text-xl font-semibold text-blue-300">
              National Diploma in Accounting (Lagos State Polytechnic)
            </h3>
            <p className="text-gray-400">Technical Education</p>
          </div>
        </div>
      </section>
      */}

      {/* References */}
      <section className="text-center bg-blue-500/10 border border-blue-500/30 rounded-lg p-6">
        <h2 className="text-2xl font-bold text-white mb-2">References</h2>
        <p className="text-gray-300">Available upon request</p>
      </section>
    </div>
  );
}

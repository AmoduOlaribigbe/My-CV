import { Briefcase, Calendar, MapPin } from "lucide-react";

export function Experience() {
  const experiences = [
  {
    title:
      "Centre Academic Head | Network Administrator | CEH & Cybersecurity Instructor",
    organization: "Aptech Computer Education – Maryland Centre",
    location: "Lagos, Nigeria",
    period: "Aug 2023 – Present",
    description:
      "Strategic Leadership, IT Infrastructure Modernization & Cybersecurity Education",
    achievements: [
      "Improved student retention and graduation rates through a structured mentorship and engagement framework",
      "Introduced KPI-driven faculty performance system across Multimedia, Networking & Software departments",
      "Delivered 100% on-time academic project submissions to HQ, eliminating compliance backlogs",
      "Modernized IT systems via preventive server maintenance, automated backups, and cloud migration (Google Drive & OneDrive)",
      "Achieved zero exam disruptions by strengthening system resilience and business continuity",
      "Designed real-world CEH & Digital Forensics labs simulating cyberattack and investigation scenarios",
      "Improved institutional cyber hygiene through structured security awareness and incident response training",
      "Graduated industry-ready cybersecurity professionals aligned with global standards",
    ],
    type: "IT Infrastructure & Cybersecurity Leadership",
  },

  {
    title: "Cyber Security Analyst (Virtual Experience)",
    organization: "AIG Shields Up – Forage (Remote, New York, USA)",
    location: "Remote",
    period: "Jun 2024",
    description:
      "Cyber Threat Intelligence, Vulnerability Triage & Ransomware Simulation",
    achievements: [
      "Conducted enterprise threat analysis aligned with CISA advisories",
      "Applied vulnerability triage methodologies and drafted executive-level security advisories",
      "Developed Python-based ethical hacking script to simulate ransomware key recovery",
      "Translated technical risks into business-impact language for cross-functional stakeholders",
      "Strengthened enterprise-level risk prioritization and incident response coordination",
    ],
    type: "Cybersecurity Risk Analysis",
  },

  {
    title: "Coding & Robotics Training Manager",
    organization: "Nhames Projects Limited",
    location: "Ikeja, Lagos, Nigeria",
    period: "Jul 2022 – Aug 2023",
    description:
      "Technical Leadership, Curriculum Innovation & Revenue Growth",
    achievements: [
      "Designed scalable coding & robotics curriculum (Python, Java, C++)",
      "Led instructor teams using KPI-driven coaching and structured evaluation systems",
      "Collaborated with business development to convert technical presentations into long-term contracts",
      "Achieved 65% revenue growth through strategic stakeholder engagement",
      "Implemented data-driven performance analytics improving instructional ROI",
      "Optimized departmental budgeting, logistics, and resource allocation",
    ],
    type: "Technical Leadership & Business Growth",
  },

  {
    title: "Multimedia & Computer Hardware Instructor",
    organization: "Daleware Institute of Technology",
    location: "Lagos, Nigeria",
    period: "Jul 2021 – Jun 2022",
    description:
      "Multimedia Education & Large-Scale IT Infrastructure Support (250+ Systems)",
    achievements: [
      "Delivered industry-aligned multimedia curriculum (graphics, animation, video production)",
      "Maintained and optimized 250+ CBT systems ensuring seamless academic operations",
      "Reduced system downtime improving exam reliability and institutional credibility",
      "Enhanced student pass rates and project quality through hands-on mentorship",
      "Integrated networking fundamentals into multimedia and hardware training",
    ],
    type: "IT Infrastructure & Instruction",
  },

  {
    title: "IT & Systems Support Intern",
    organization: "Arkounting Business Concepts Limited",
    location: "Lagos, Nigeria",
    period: "Jul 2015 – Jun 2016",
    description:
      "IT Support, Documentation & Disaster Recovery Assistance",
    achievements: [
      "Troubleshot hardware, software, and networking issues minimizing downtime",
      "Improved IT documentation and asset visibility processes",
      "Assisted in implementing backup and disaster recovery procedures",
      "Strengthened operational continuity through structured IT support workflows",
    ],
    type: "IT Support & Systems Administration",
  },
];

  return (
    <div className="py-8 space-y-8">
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
          Professional Experience
        </h1>
        <p className="text-xl text-gray-300">
          7+ Years of Leadership in IT Infrastructure, Cybersecurity, and Education
        </p>
      </div>

      <div className="space-y-8">
        {experiences.map((exp, index) => (
          <div
            key={index}
            className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6 hover:border-blue-500/40 transition-colors"
          >
            <div className="flex flex-col md:flex-row md:items-start md:justify-between mb-4">
              <div className="flex-1">
                <h3 className="text-2xl font-semibold text-white mb-2">
                  {exp.title}
                </h3>
                <div className="flex items-center gap-2 text-blue-300 mb-2">
                  <Briefcase className="w-5 h-5" />
                  <span className="text-lg">{exp.organization}</span>
                </div>
                {exp.location && (
                  <div className="flex items-center gap-2 text-gray-400 mb-2">
                    <MapPin className="w-4 h-4" />
                    <span>{exp.location}</span>
                  </div>
                )}
              </div>
              <div className="flex items-center gap-2 text-gray-400 mt-2 md:mt-0">
                <Calendar className="w-4 h-4" />
                <span>{exp.period}</span>
              </div>
            </div>

            {exp.description && (
              <p className="text-gray-300 mb-4 italic">{exp.description}</p>
            )}

            <div className="space-y-3">
              <h4 className="text-lg font-semibold text-blue-300">Key Achievements:</h4>
              <ul className="space-y-2">
                {exp.achievements.map((achievement, i) => (
                  <li key={i} className="flex gap-3 text-gray-300">
                    <span className="text-blue-400 mt-1.5 flex-shrink-0">•</span>
                    <span>{achievement}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="mt-4">
              <span className="inline-block px-3 py-1 bg-blue-500/20 text-blue-300 rounded-full text-sm">
                {exp.type}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

import { Link } from "react-router";
import { Shield, Server, Cloud, Code, Lock, Network } from "lucide-react";
import { Button } from "../ui/button";
import profilepic from "./profile.jpeg";

export function Home() {
  return (
    <div className="space-y-16 py-8">
      {/* Hero Section */}
      <section className="text-center space-y-6 py-12">
        <div className="flex justify-center mb-6">
          <div className="relative">
            <div className="w-32 h-32 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">
              <img
                src={profilepic}
                alt="Olaribigbe Amodu"
                className="w-full h-full rounded-full object-cover"
              />
            </div>
            <div className="absolute -bottom-2 -right-2 w-12 h-12 bg-green-500 rounded-full border-4 border-slate-900 flex items-center justify-center">
              <Lock className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>
        <h1 className="text-5xl md:text-6xl font-bold text-white">
          Olaribigbe Amodu
        </h1>
        <p className="text-xl md:text-2xl text-blue-300">
          Cybersecurity & IT Support Specialist | Digital Forensics | IT Infrastructure Leadership
        </p>
        <p className="text-lg text-gray-300 max-w-3xl mx-auto">
          Dedicated and detail-oriented Cybersecurity professional with hands-on expertise in 
          system administration, troubleshooting, and network security. Skilled in delivering 
          proactive security measures and bridging technical solutions with organizational needs.
        </p>
        <div className="flex gap-4 justify-center flex-wrap">
          <Button asChild size="lg" className="bg-blue-600 hover:bg-blue-700">
            <Link to="/projects">View Projects</Link>
          </Button>
          <Button asChild size="lg" variant="outline" className="border-blue-400 text-blue-400 hover:bg-blue-400/10">
            <Link to="/contact">Get in Touch</Link>
          </Button>
        </div>
      </section>

      {/* Key Highlights */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6 hover:border-blue-500/40 transition-colors">
          <Shield className="w-12 h-12 text-blue-400 mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">Cybersecurity Expertise</h3>
          <p className="text-gray-300">
            Certified Ethical Hacker (CEH) with extensive experience in vulnerability analysis, 
            penetration testing, and digital forensics.
          </p>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6 hover:border-blue-500/40 transition-colors">
          <Server className="w-12 h-12 text-cyan-400 mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">IT Infrastructure</h3>
          <p className="text-gray-300">
            Expert in designing, implementing, and maintaining enterprise-level IT systems 
            with focus on reliability and scalability.
          </p>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6 hover:border-blue-500/40 transition-colors">
          <Cloud className="w-12 h-12 text-purple-400 mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">DevOps & Cloud</h3>
          <p className="text-gray-300">
            Proficient in Azure, Google Cloud Platform, and implementing automated deployment 
            pipelines for efficient operations.
          </p>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6 hover:border-blue-500/40 transition-colors">
          <Code className="w-12 h-12 text-green-400 mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">Python Scripting</h3>
          <p className="text-gray-300">
            Advanced Python programming for automation, security tools, data analysis, 
            and system administration tasks.
          </p>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6 hover:border-blue-500/40 transition-colors">
          <Network className="w-12 h-12 text-orange-400 mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">Network Security</h3>
          <p className="text-gray-300">
            Skilled in implementing network security solutions, firewalls, VPNs, 
            and securing enterprise networks.
          </p>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6 hover:border-blue-500/40 transition-colors">
          <Lock className="w-12 h-12 text-red-400 mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">Digital Forensics</h3>
          <p className="text-gray-300">
            Experienced in incident response, forensic analysis, threat detection, 
            and security incident investigation.
          </p>
        </div>
      </section>

      {/* Professional Summary */}
      <section className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-8">
        <h2 className="text-3xl font-bold text-white mb-6">Professional Summary</h2>
        <div className="space-y-4 text-gray-300">
          <p>
            <strong className="text-white">7+ years of progressive experience</strong> spanning IT infrastructure management, 
            cybersecurity, digital forensics, system administration, and academic leadership.
          </p>
          <p>
            <strong className="text-white">Acted as VP of Systems</strong>, architect, and systems administrator overseeing 
            technical operations, hardware/software issues, and IT compliance.
          </p>
          <p>
            <strong className="text-white">Partnered with sales and business development teams</strong> to design and deliver 
            technology presentations to schools and parents, increasing company revenue by 65%.
          </p>
          <p>
            <strong className="text-white">Expert in cloud infrastructure</strong>, networking hardware, cloud-based backup 
            solutions, and large-scale computer labs/CBT centers (250+ systems).
          </p>
          <p>
            <strong className="text-white">Delivered specialized training</strong> in CEH, cybersecurity, and digital forensics, 
            managed cross-functional academic teams, and developed coding and robotics curricula.
          </p>
        </div>
      </section>

      {/* Contact CTA */}
      <section className="text-center py-12">
        <h2 className="text-3xl font-bold text-white mb-4">
          Ready to Collaborate?
        </h2>
        <p className="text-lg text-gray-300 mb-6">
          Let's discuss how I can contribute to your organization's security and infrastructure needs.
        </p>
        <Button asChild size="lg" className="bg-blue-600 hover:bg-blue-700">
          <Link to="/contact">Contact Me</Link>
        </Button>
      </section>
    </div>
  );
}

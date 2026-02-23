import { Mail, Phone, MapPin, Linkedin, Github, Send } from "lucide-react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Textarea } from "../ui/textarea";
import { useState } from "react";

export function Contact() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // This is a frontend-only implementation
    // In production, this would connect to a backend service
    alert("Thank you for your message! This is a demo form. In production, your message would be sent.");
    setFormData({ name: "", email: "", subject: "", message: "" });
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="py-8 space-y-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
          Get In Touch
        </h1>
        <p className="text-xl text-gray-300 max-w-2xl mx-auto">
          Interested in collaborating on cybersecurity projects or discussing IT infrastructure solutions? 
          Let's connect and explore opportunities together.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Contact Information */}
        <div className="space-y-6">
          <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-white mb-6">Contact Information</h2>
            
            <div className="space-y-4">
              <div className="flex items-center gap-4 text-gray-300">
                <div className="p-3 bg-blue-500/20 rounded-lg">
                  <Mail className="w-6 h-6 text-blue-400" />
                </div>
                <div>
                  <p className="text-sm text-gray-400">Email</p>
                  <a href="mailto:olaribigbe.amodu@gmail.com" className="hover:text-blue-400 transition-colors">
                    olaribigbe.amodu@gmail.com
                  </a>
                </div>
              </div>

              <div className="flex items-center gap-4 text-gray-300">
                <div className="p-3 bg-blue-500/20 rounded-lg">
                  <Phone className="w-6 h-6 text-blue-400" />
                </div>
                <div>
                  <p className="text-sm text-gray-400">Phone</p>
                  <a href="tel:+2348170339744" className="hover:text-blue-400 transition-colors">
                    +234 817 033 9744
                  </a>
                </div>
              </div>

              <div className="flex items-center gap-4 text-gray-300">
                <div className="p-3 bg-blue-500/20 rounded-lg">
                  <MapPin className="w-6 h-6 text-blue-400" />
                </div>
                <div>
                  <p className="text-sm text-gray-400">Location</p>
                  <p>Lagos, Nigeria</p>
                </div>
              </div>
            </div>
          </div>

          {/* Professional Profiles */}
          <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-white mb-6">Professional Profiles</h2>
            
            <div className="space-y-3">
              <a
                href="https://linkedin.com/in/olaribigbe-amodu-4a611216b"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 p-3 bg-slate-700/50 rounded-lg hover:bg-slate-700 transition-colors"
              >
                <Linkedin className="w-6 h-6 text-blue-400" />
                <div>
                  <p className="text-white font-semibold">LinkedIn</p>
                  <p className="text-sm text-gray-400">Connect professionally</p>
                </div>
              </a>

              <a
                href="https://github.com/AmoduOlaribigbe"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 p-3 bg-slate-700/50 rounded-lg hover:bg-slate-700 transition-colors"
              >
                <Github className="w-6 h-6 text-blue-400" />
                <div>
                  <p className="text-white font-semibold">GitHub</p>
                  <p className="text-sm text-gray-400">View my code and projects</p>
                </div>
              </a>
            </div>
          </div>

          {/* Areas of Interest */}
          <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-white mb-4">Open to Opportunities In:</h2>
            <ul className="space-y-2 text-gray-300">
              <li className="flex items-center gap-2">
                <span className="text-blue-400">•</span>
                <span>Cybersecurity Consulting & Penetration Testing</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="text-blue-400">•</span>
                <span>IT Infrastructure Architecture & Management</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="text-blue-400">•</span>
                <span>DevOps & Cloud Security Implementation</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="text-blue-400">•</span>
                <span>Digital Forensics & Incident Response</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="text-blue-400">•</span>
                <span>Technical Training & Workshop Facilitation</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Contact Form */}
        <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6">
          <h2 className="text-2xl font-bold text-white mb-6">Send a Message</h2>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-300 mb-2">
                Your Name *
              </label>
              <Input
                id="name"
                name="name"
                type="text"
                required
                value={formData.name}
                onChange={handleChange}
                placeholder="John Doe"
                className="bg-slate-700/50 border-slate-600 text-white placeholder:text-gray-500"
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
                Email Address *
              </label>
              <Input
                id="email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={handleChange}
                placeholder="john@example.com"
                className="bg-slate-700/50 border-slate-600 text-white placeholder:text-gray-500"
              />
            </div>

            <div>
              <label htmlFor="subject" className="block text-sm font-medium text-gray-300 mb-2">
                Subject *
              </label>
              <Input
                id="subject"
                name="subject"
                type="text"
                required
                value={formData.subject}
                onChange={handleChange}
                placeholder="Collaboration Opportunity"
                className="bg-slate-700/50 border-slate-600 text-white placeholder:text-gray-500"
              />
            </div>

            <div>
              <label htmlFor="message" className="block text-sm font-medium text-gray-300 mb-2">
                Message *
              </label>
              <Textarea
                id="message"
                name="message"
                required
                value={formData.message}
                onChange={handleChange}
                placeholder="Tell me about your project or opportunity..."
                rows={6}
                className="bg-slate-700/50 border-slate-600 text-white placeholder:text-gray-500"
              />
            </div>

            <Button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-700 text-white"
              size="lg"
            >
              <Send className="w-5 h-5 mr-2" />
              Send Message
            </Button>

            <p className="text-xs text-gray-400 text-center">
              * This is a demo form. In production, messages would be sent to the email address.
            </p>
          </form>
        </div>
      </div>

      {/* Download CV Section */}
      <div className="text-center bg-blue-500/10 border border-blue-500/30 rounded-lg p-8">
        <h2 className="text-2xl font-bold text-white mb-4">
          Download My Complete CV
        </h2>
        <p className="text-gray-300 mb-6">
          Get the full details of my experience, certifications, and project portfolio
        </p>
        <a href="/Ola-Amodu-CV.pdf" download>
          <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
            Download CV (PDF)
          </Button>
        </a>
      </div>
    </div>
  );
}

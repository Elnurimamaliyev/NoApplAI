import React from 'react';

/**
 * Footer Component - Responsive three-column footer
 * 
 * To modify:
 * - Edit the footerData object below to change section titles and links
 * - Adjust Tailwind classes for spacing, colors, or typography
 * - Links are placeholders - replace href values with actual routes
 */

const Footer = () => {
  const footerData = {
    product: {
      title: "Product",
      links: [
        { label: "Features", href: "#features" },
        { label: "Pricing", href: "#pricing" },
        { label: "Universities", href: "#universities" },
        { label: "Success Stories", href: "#success-stories" }
      ]
    },
    company: {
      title: "Company",
      links: [
        { label: "About Us", href: "#about" },
        { label: "Careers", href: "#careers" },
        { label: "Blog", href: "#blog" },
        { label: "Contact", href: "#contact" }
      ]
    },
    legal: {
      title: "Legal",
      links: [
        { label: "Privacy Policy", href: "#privacy" },
        { label: "Terms of Service", href: "#terms" },
        { label: "Cookie Policy", href: "#cookie" },
        { label: "Support", href: "#support" }
      ]
    }
  };

  return (
    <footer 
      className="bg-white border-t border-gray-200 px-6 py-16 md:py-20 lg:py-24" 
      role="contentinfo"
    >
      <div className="max-w-7xl mx-auto">
        <nav 
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-12 sm:gap-10 lg:gap-20"
          aria-label="Footer Navigation"
        >
          {/* Product Column */}
          <div className="flex flex-col gap-4">
            <h3 className="text-lg font-bold text-gray-900 tracking-tight mb-2">
              {footerData.product.title}
            </h3>
            <ul className="flex flex-col gap-3">
              {footerData.product.links.map((link, index) => (
                <li key={index}>
                  <a
                    href={link.href}
                    className="text-[15px] text-gray-600 hover:text-gray-900 transition-colors duration-200 inline-block focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Company Column */}
          <div className="flex flex-col gap-4">
            <h3 className="text-lg font-bold text-gray-900 tracking-tight mb-2">
              {footerData.company.title}
            </h3>
            <ul className="flex flex-col gap-3">
              {footerData.company.links.map((link, index) => (
                <li key={index}>
                  <a
                    href={link.href}
                    className="text-[15px] text-gray-600 hover:text-gray-900 transition-colors duration-200 inline-block focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal Column */}
          <div className="flex flex-col gap-4">
            <h3 className="text-lg font-bold text-gray-900 tracking-tight mb-2">
              {footerData.legal.title}
            </h3>
            <ul className="flex flex-col gap-3">
              {footerData.legal.links.map((link, index) => (
                <li key={index}>
                  <a
                    href={link.href}
                    className="text-[15px] text-gray-600 hover:text-gray-900 transition-colors duration-200 inline-block focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </nav>
      </div>
    </footer>
  );
};

export default Footer;

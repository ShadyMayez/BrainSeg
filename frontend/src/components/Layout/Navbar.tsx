import { NavLink } from 'react-router-dom';
import { Brain, Activity, BarChart3, Info } from 'lucide-react';

const navItems = [
  { path: '/', label: 'Prediction', icon: Activity },
  { path: '/analysis', label: 'Data Analysis', icon: BarChart3 },
  { path: '/about', label: 'About', icon: Info },
];

export function Navbar() {
  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-medical-500 to-medical-700 rounded-xl flex items-center justify-center">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-gray-900">Brain Tumor Segmentation</h1>
              <p className="text-xs text-gray-500">BraTS 2020</p>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="flex items-center gap-1">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `nav-link ${isActive ? 'nav-link-active' : ''}`
                }
              >
                <item.icon className="w-5 h-5" />
                <span className="hidden sm:inline">{item.label}</span>
              </NavLink>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
}

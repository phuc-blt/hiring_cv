'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { FileText, Users, ClipboardCheck, Sun, Moon } from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';

const navItems = [
  { href: '/', label: 'Tạo JD', icon: FileText },
  { href: '/apply', label: 'Ứng tuyển', icon: Users },
  { href: '/evaluate', label: 'Đánh giá CV', icon: ClipboardCheck },
];

export default function Navigation() {
  const pathname = usePathname();
  const { theme, toggleTheme } = useTheme();
  
  console.log('Navigation render, theme:', theme);
  
  const handleThemeToggle = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    toggleTheme();
  };

  return (
    <nav className="nav">
      <div className="container mx-auto">
        <div className="flex justify-between items-center h-20">
          <div className="flex items-center space-x-8">
            <div className="flex-shrink-0 flex items-center">
              <h1 className="text-2xl md:text-3xl font-extrabold gradient-text">
                Hiring CV System
              </h1>
            </div>
            <div className="hidden lg:flex space-x-2">
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = pathname === item.href;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`nav-link glass-effect rounded-lg px-4 py-2 ${
                      isActive ? 'active' : ''
                    }`}
                  >
                    <Icon className="w-5 h-5 mr-2" />
                    <span className="font-medium">{item.label}</span>
                  </Link>
                );
              })}
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <button
              onClick={handleThemeToggle}
              className="p-3 rounded-full glass-effect hover-lift"
              title={theme === 'dark' ? 'Chuyển sang light mode' : 'Chuyển sang dark mode'}
            >
              {theme === 'dark' ? (
                <Sun className="w-5 h-5" style={{color: '#fbbf24'}} />
              ) : (
                <Moon className="w-5 h-5" style={{color: '#3b82f6'}} />
              )}
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}

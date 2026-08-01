'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';

export default function DashboardPage() {
  const router = useRouter();
  const { isAuthenticated, logout, restore, token } = useAuth();

  useEffect(() => {
    restore();
  }, [restore]);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">ForwardAI CRM</h1>
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-12">
        <div className="bg-white rounded-lg shadow p-8">
          <h2 className="text-3xl font-bold mb-4">Welcome to ForwardAI CRM</h2>
          <p className="text-gray-600 mb-6">
            You're authenticated and ready to start managing clients, projects, and proposals.
          </p>

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div className="bg-blue-50 p-6 rounded-lg">
              <div className="text-3xl font-bold text-blue-600">0</div>
              <div className="text-gray-600">Total Clients</div>
            </div>
            <div className="bg-green-50 p-6 rounded-lg">
              <div className="text-3xl font-bold text-green-600">0</div>
              <div className="text-gray-600">Active Projects</div>
            </div>
            <div className="bg-purple-50 p-6 rounded-lg">
              <div className="text-3xl font-bold text-purple-600">0</div>
              <div className="text-gray-600">Pipeline Value</div>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="space-y-3">
            <h3 className="text-lg font-semibold mb-4">Next Steps:</h3>
            <ul className="list-disc list-inside space-y-2 text-gray-700">
              <li>Create your first client</li>
              <li>Add team members</li>
              <li>Start tracking projects</li>
              <li>Manage proposals and revenue</li>
            </ul>
          </div>
        </div>
      </main>
    </div>
  );
}

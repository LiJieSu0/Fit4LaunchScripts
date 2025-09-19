import React from 'react';

function Header() {
  return (
    <header className="bg-[#f0f0f0] shadow-lg print-header">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <img src="/logo192.png" alt="ATMCL Logo" className="h-10 mr-4" /> {/* Placeholder for ATMCL logo */}
            <div>
              <h1 className="text-xl font-bold text-gray-800">Fit4Launch | ATMCL</h1>
              <p className="text-xs text-gray-600">T-Mobile Device Test Plan: 5G Auto Call Performance Report | Wingtech Plunkett</p>
            </div>
          </div>
          <div>
            <img src="/ATMCL-logo.png" alt="ATMCL" className="h-10" /> {/* Placeholder for ATMCL logo on the right */}
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;

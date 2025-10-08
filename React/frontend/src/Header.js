import React from 'react';

function Header() {
  return (
    <header className="">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <img src="/atmclogo.jpg" alt="ATMCL Logo" className="h-10 mr-4" /> {/* Placeholder for ATMCL logo */}
            <div>
              <h1 className="text-xl font-bold text-gray-800">Field Test Report</h1>
            </div>
          </div>
        </div>
    </header>
  );
}

export default Header;

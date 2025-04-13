import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";

import FileUpload from './components/FileUpload'; // Import the component
import ReconciliationPage from './pages/ReconciliationPage'; // Import the new page

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
        {/* Simple Navigation Header */}
        <nav className="bg-white dark:bg-gray-800 shadow p-4">
          <ul className="flex space-x-4">
            <li>
              <Link to="/" className="hover:text-blue-500 dark:hover:text-blue-400">Upload</Link>
            </li>
            <li>
              <Link to="/reconciliation" className="hover:text-blue-500 dark:hover:text-blue-400">Reconciliation</Link>
            </li>
            {/* Add more links as needed (Dashboard, Trends, etc.) */}
          </ul>
        </nav>

        {/* Main Content Area */}
        <main className="flex-grow container mx-auto p-4">
          <Routes>
            {/* Route for the Upload page (now at root) */}
            <Route path="/" element={<FileUpload />} />
            {/* Route for the Reconciliation page */}
            <Route path="/reconciliation" element={<ReconciliationPage />} />
            {/* Define other routes here */}
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-white">
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="md:flex md:items-center md:justify-between">
          <div className="flex justify-center md:justify-start">
            <p className="text-sm text-gray-500">
              &copy; {currentYear} Multi-User Todo Web Application. All rights reserved.
            </p>
          </div>
          <div className="mt-4 md:mt-0 flex justify-center md:justify-end space-x-6">
            <a href="/privacy" className="text-gray-400 hover:text-gray-500">
              Privacy Policy
            </a>
            <a href="/terms" className="text-gray-400 hover:text-gray-500">
              Terms of Service
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
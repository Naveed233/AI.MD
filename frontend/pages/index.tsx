import Link from 'next/link'

export default function Home() {
  return (
    <div className="container mx-auto p-6">
      <h1 className="text-4xl font-bold mb-6">AI Merchandising System</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Link href="/predict">
          <div className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-10 px-6 rounded text-center cursor-pointer">
            Predict Demand
          </div>
        </Link>
        
        <Link href="/analytics">
          <div className="bg-green-500 hover:bg-green-700 text-white font-bold py-10 px-6 rounded text-center cursor-pointer">
            View Analytics
          </div>
        </Link>
        
        <Link href="/models">
          <div className="bg-purple-500 hover:bg-purple-700 text-white font-bold py-10 px-6 rounded text-center cursor-pointer">
            Manage Models
          </div>
        </Link>
      </div>

      <div className="mt-8">
        <h2 className="text-2xl font-semibold mb-4">System Status</h2>
        <div className="bg-gray-100 p-4 rounded">
          <p>✓ ML Service: Connected</p>
          <p>✓ Database: Connected</p>
          <p>✓ Cloud Storage: Ready</p>
        </div>
      </div>
    </div>
  )
}


import { useState } from 'react'
import axios from 'axios'

interface ModelInfo {
  name: string
  version: string
  accuracy: number
  status: string
  last_trained: string
}

export default function Models() {
  const [models, setModels] = useState<ModelInfo[]>([
    {
      name: 'Random Forest Regressor',
      version: 'v1.0',
      accuracy: 0.97,
      status: 'Active',
      last_trained: 'Oct 28, 2024'
    }
  ])
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState<string | null>(null)

  const handleRetrain = async () => {
    setLoading(true)
    setMessage(null)
    
    try {
      const response = await axios.post('http://localhost:8080/reload')
      setMessage(`Model reloaded successfully! Status: ${response.data.status}`)
      setTimeout(() => setMessage(null), 5000)
    } catch (err: any) {
      setMessage(`Error: ${err.response?.data?.detail || 'Failed to reload model'}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto p-6 max-w-6xl">
      <h1 className="text-3xl font-bold mb-6">Model Management</h1>
      
      <div className="bg-white shadow-md rounded p-6 mb-6">
        <h2 className="text-2xl font-semibold mb-4">Current Model</h2>
        
        {models.map((model, index) => (
          <div key={index} className="border-b pb-4 mb-4">
            <div className="flex justify-between items-start mb-2">
              <div>
                <h3 className="text-xl font-bold">{model.name}</h3>
                <p className="text-sm text-gray-600">Version: {model.version}</p>
              </div>
              <span className={`px-3 py-1 rounded text-sm font-semibold ${
                model.status === 'Active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
              }`}>
                {model.status}
              </span>
            </div>
            
            <div className="grid grid-cols-2 gap-4 mt-4">
              <div>
                <p className="text-sm text-gray-600">Accuracy (R²)</p>
                <p className="text-2xl font-bold text-blue-600">{(model.accuracy * 100).toFixed(1)}%</p>
              </div>
              
              <div>
                <p className="text-sm text-gray-600">Last Trained</p>
                <p className="text-lg font-semibold">{model.last_trained}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-white shadow-md rounded p-6 mb-6">
        <h2 className="text-2xl font-semibold mb-4">Model Information</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="border rounded p-4">
            <h3 className="font-semibold mb-2">Algorithm</h3>
            <p className="text-gray-700">Random Forest Regressor</p>
          </div>
          
          <div className="border rounded p-4">
            <h3 className="font-semibold mb-2">Number of Trees</h3>
            <p className="text-gray-700">100 decision trees</p>
          </div>
          
          <div className="border rounded p-4">
            <h3 className="font-semibold mb-2">Training Data</h3>
            <p className="text-gray-700">541,909 transactions</p>
          </div>
          
          <div className="border rounded p-4">
            <h3 className="font-semibold mb-2">Features</h3>
            <p className="text-gray-700">6 input features</p>
          </div>
        </div>
      </div>

      <div className="bg-white shadow-md rounded p-6">
        <h2 className="text-2xl font-semibold mb-4">Model Actions</h2>
        
        <button
          onClick={handleRetrain}
          disabled={loading}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded disabled:opacity-50"
        >
          {loading ? 'Reloading...' : 'Reload Model from Storage'}
        </button>
        
        {message && (
          <div className={`mt-4 p-3 rounded ${
            message.includes('Error') ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'
          }`}>
            {message}
          </div>
        )}
        
        <div className="mt-6 p-4 bg-yellow-50 rounded">
          <p className="text-sm text-yellow-800">
            💡 <strong>Note:</strong> To retrain with new data, upload a CSV file to Cloud Storage 
            (training/ folder). The system will automatically retrain.
          </p>
        </div>
      </div>
    </div>
  )
}


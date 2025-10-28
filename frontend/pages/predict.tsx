import { useState, FormEvent } from 'react'
import axios from 'axios'

interface PredictionResult {
  predicted_demand: number
  category: string
  optimal_stock: number
  confidence: number
}

export default function Predict() {
  const [form, setForm] = useState({
    customer_id: '',
    age: '',
    purchase_history: '',
    avg_order_value: '',
    last_purchase_days: '',
    region: '',
    seasonality_factor: '1.0'
  })
  const [result, setResult] = useState<PredictionResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    
    try {
      const response = await axios.post(
        `http://localhost:8080/predict`,
        {
          customer_id: form.customer_id,
          age: parseFloat(form.age),
          purchase_history: parseInt(form.purchase_history),
          avg_order_value: parseFloat(form.avg_order_value),
          last_purchase_days: parseInt(form.last_purchase_days),
          region: form.region,
          seasonality_factor: parseFloat(form.seasonality_factor)
        }
      )
      
      setResult(response.data)
    } catch (err: any) {
      setError(err.response?.data?.error || 'An error occurred')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto p-6 max-w-2xl">
      <h1 className="text-3xl font-bold mb-6">AI Merchandising Dashboard</h1>
      
      <form onSubmit={handleSubmit} className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Customer ID
            </label>
            <input
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              type="text"
              name="customer_id"
              value={form.customer_id}
              onChange={handleChange}
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Age
            </label>
            <input
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              type="number"
              name="age"
              value={form.age}
              onChange={handleChange}
              required
              min="0"
              max="120"
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Purchase History (count)
            </label>
            <input
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              type="number"
              name="purchase_history"
              value={form.purchase_history}
              onChange={handleChange}
              required
              min="0"
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Avg Order Value ($)
            </label>
            <input
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              type="number"
              name="avg_order_value"
              value={form.avg_order_value}
              onChange={handleChange}
              required
              min="0"
              step="0.01"
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Last Purchase (days ago)
            </label>
            <input
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              type="number"
              name="last_purchase_days"
              value={form.last_purchase_days}
              onChange={handleChange}
              required
              min="0"
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Region
            </label>
            <select
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              name="region"
              value={form.region}
              onChange={handleChange}
              required
            >
              <option value="">Select a region</option>
              <option value="North America">North America</option>
              <option value="South America">South America</option>
              <option value="Europe">Europe</option>
              <option value="Asia">Asia</option>
              <option value="Africa">Africa</option>
              <option value="Oceania">Oceania</option>
            </select>
          </div>

          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Seasonality Factor
            </label>
            <input
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              type="number"
              name="seasonality_factor"
              value={form.seasonality_factor}
              onChange={handleChange}
              required
              min="0.1"
              max="5"
              step="0.1"
            />
          </div>
        </div>

        <div className="flex items-center justify-between">
          <button
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:opacity-50"
            type="submit"
            disabled={loading}
          >
            {loading ? 'Processing...' : 'Predict Demand'}
          </button>
        </div>
      </form>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {result && (
        <div className="bg-green-50 border border-green-400 text-gray-800 px-6 py-4 rounded">
          <h2 className="text-2xl font-bold mb-4">Prediction Results</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="font-semibold">Predicted Demand:</p>
              <p className="text-xl text-blue-600">{result.predicted_demand.toFixed(2)}</p>
            </div>
            <div>
              <p className="font-semibold">Category:</p>
              <p className="text-xl text-green-600">{result.category}</p>
            </div>
            <div>
              <p className="font-semibold">Optimal Stock:</p>
              <p className="text-xl text-purple-600">{result.optimal_stock}</p>
            </div>
            <div>
              <p className="font-semibold">Confidence:</p>
              <p className="text-xl text-orange-600">{(result.confidence * 100).toFixed(1)}%</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}


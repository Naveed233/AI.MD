import { useState, useEffect } from 'react'
import axios from 'axios'

interface AnalyticsData {
  total_predictions: number
  avg_predicted_demand: number
  avg_confidence: number
  high_demand_count: number
  medium_demand_count: number
  low_demand_count: number
}

export default function Analytics() {
  const [data, setData] = useState<AnalyticsData | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadAnalytics()
  }, [])

  const loadAnalytics = async () => {
    setLoading(true)
    try {
      // Simulated analytics data - in real app, fetch from backend
      const mockData: AnalyticsData = {
        total_predictions: 1523,
        avg_predicted_demand: 856.42,
        avg_confidence: 0.87,
        high_demand_count: 892,
        medium_demand_count: 487,
        low_demand_count: 144
      }
      setData(mockData)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto p-6 max-w-6xl">
      <h1 className="text-3xl font-bold mb-6">Analytics Dashboard</h1>
      
      {loading ? (
        <div className="text-center py-12">
          <p className="text-gray-600">Loading analytics...</p>
        </div>
      ) : data ? (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <div className="bg-white shadow-md rounded p-6">
              <h3 className="text-gray-600 text-sm font-semibold mb-2">Total Predictions</h3>
              <p className="text-3xl font-bold text-blue-600">{data.total_predictions.toLocaleString()}</p>
            </div>
            
            <div className="bg-white shadow-md rounded p-6">
              <h3 className="text-gray-600 text-sm font-semibold mb-2">Avg Predicted Demand</h3>
              <p className="text-3xl font-bold text-green-600">{Math.round(data.avg_predicted_demand)}</p>
            </div>
            
            <div className="bg-white shadow-md rounded p-6">
              <h3 className="text-gray-600 text-sm font-semibold mb-2">Avg Confidence</h3>
              <p className="text-3xl font-bold text-purple-600">{(data.avg_confidence * 100).toFixed(1)}%</p>
            </div>
            
            <div className="bg-white shadow-md rounded p-6">
              <h3 className="text-gray-600 text-sm font-semibold mb-2">Success Rate</h3>
              <p className="text-3xl font-bold text-orange-600">94.2%</p>
            </div>
          </div>

          <div className="bg-white shadow-md rounded p-6 mb-6">
            <h2 className="text-2xl font-semibold mb-4">Demand Distribution</h2>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-sm font-medium text-gray-700">High Demand</span>
                  <span className="text-sm text-gray-700">{data.high_demand_count}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-4">
                  <div 
                    className="bg-green-600 h-4 rounded-full"
                    style={{ width: `${(data.high_demand_count / data.total_predictions) * 100}%` }}
                  ></div>
                </div>
              </div>
              
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-sm font-medium text-gray-700">Medium Demand</span>
                  <span className="text-sm text-gray-700">{data.medium_demand_count}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-4">
                  <div 
                    className="bg-yellow-600 h-4 rounded-full"
                    style={{ width: `${(data.medium_demand_count / data.total_predictions) * 100}%` }}
                  ></div>
                </div>
              </div>
              
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-sm font-medium text-gray-700">Low Demand</span>
                  <span className="text-sm text-gray-700">{data.low_demand_count}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-4">
                  <div 
                    className="bg-red-600 h-4 rounded-full"
                    style={{ width: `${(data.low_demand_count / data.total_predictions) * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white shadow-md rounded p-6">
            <h2 className="text-2xl font-semibold mb-4">Recent Activity</h2>
            <div className="space-y-2">
              <p className="text-gray-600">Last 24 hours: 47 predictions</p>
              <p className="text-gray-600">Last 7 days: 312 predictions</p>
              <p className="text-gray-600">Last 30 days: {data.total_predictions} predictions</p>
            </div>
          </div>
        </>
      ) : (
        <div className="text-center py-12">
          <p className="text-gray-600">No analytics data available</p>
        </div>
      )}
    </div>
  )
}


<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Validator;

class PredictionController extends Controller
{
    protected $mlApiUrl;

    public function __construct()
    {
        $this->mlApiUrl = env('ML_API_URL', 'http://ml_service:8080');
    }

    /**
     * Get prediction from ML service
     *
     * @param Request $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function predict(Request $request)
    {
        // Validate input
        $validator = Validator::make($request->all(), [
            'customer_id' => 'required|string',
            'age' => 'required|numeric|min:0|max:120',
            'purchase_history' => 'required|integer|min:0',
            'avg_order_value' => 'required|numeric|min:0',
            'last_purchase_days' => 'required|integer|min:0',
            'region' => 'required|string',
            'seasonality_factor' => 'sometimes|numeric|min:0.1|max:5',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'error' => 'Validation failed',
                'details' => $validator->errors()
            ], 422);
        }

        $data = $request->all();

        try {
            // Call ML service
            $response = Http::timeout(30)
                ->post($this->mlApiUrl . '/predict', $data);

            if (!$response->successful()) {
                Log::error('ML service error', [
                    'status' => $response->status(),
                    'body' => $response->body()
                ]);

                return response()->json([
                    'error' => 'ML service error',
                    'message' => 'Failed to get prediction'
                ], 500);
            }

            $prediction = $response->json();

            // Store prediction in database
            DB::table('predictions')->insert([
                'customer_id' => $data['customer_id'],
                'customer_data' => json_encode($data),
                'predicted_demand' => $prediction['predicted_demand'] ?? 0,
                'category' => $prediction['category'] ?? 'Unknown',
                'optimal_stock' => $prediction['optimal_stock'] ?? 0,
                'confidence' => $prediction['confidence'] ?? 0,
                'created_at' => now(),
                'updated_at' => now(),
            ]);

            Log::info('Prediction completed', [
                'customer_id' => $data['customer_id'],
                'predicted_demand' => $prediction['predicted_demand']
            ]);

            return response()->json($prediction);

        } catch (\Exception $e) {
            Log::error('Prediction error', [
                'error' => $e->getMessage(),
                'trace' => $e->getTraceAsString()
            ]);

            return response()->json([
                'error' => 'Internal server error',
                'message' => $e->getMessage()
            ], 500);
        }
    }

    /**
     * Get prediction history
     *
     * @param Request $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function history(Request $request)
    {
        $customerId = $request->input('customer_id');
        $limit = $request->input('limit', 10);

        $query = DB::table('predictions');

        if ($customerId) {
            $query->where('customer_id', $customerId);
        }

        $predictions = $query->orderBy('created_at', 'desc')
            ->limit($limit)
            ->get();

        return response()->json([
            'predictions' => $predictions
        ]);
    }

    /**
     * Trigger model reload
     *
     * @return \Illuminate\Http\JsonResponse
     */
    public function reloadModel()
    {
        try {
            $response = Http::timeout(30)
                ->post($this->mlApiUrl . '/reload');

            if (!$response->successful()) {
                return response()->json([
                    'error' => 'Failed to reload model'
                ], 500);
            }

            return response()->json($response->json());

        } catch (\Exception $e) {
            return response()->json([
                'error' => $e->getMessage()
            ], 500);
        }
    }

    /**
     * Health check
     *
     * @return \Illuminate\Http\JsonResponse
     */
    public function health()
    {
        return response()->json([
            'status' => 'healthy',
            'service' => 'Backend API',
            'timestamp' => now()->toIso8601String()
        ]);
    }
}


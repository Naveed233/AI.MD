<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\PredictionController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
*/

Route::prefix('v1')->group(function () {
    // Health check
    Route::get('/health', [PredictionController::class, 'health']);

    // Predictions
    Route::post('/predict', [PredictionController::class, 'predict']);
    Route::get('/predictions', [PredictionController::class, 'history']);
    
    // Model management
    Route::post('/model/reload', [PredictionController::class, 'reloadModel']);
});


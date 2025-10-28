<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('predictions', function (Blueprint $table) {
            $table->id();
            $table->string('customer_id')->index();
            $table->json('customer_data');
            $table->decimal('predicted_demand', 10, 2);
            $table->string('category', 50);
            $table->integer('optimal_stock');
            $table->decimal('confidence', 5, 4);
            $table->timestamps();

            $table->index('created_at');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('predictions');
    }
};


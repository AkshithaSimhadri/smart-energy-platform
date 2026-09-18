-- Smart Household Energy Management System - MySQL Database Schema
CREATE DATABASE IF NOT EXISTS `smart_energy` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `smart_energy`;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `email` VARCHAR(255) NOT NULL UNIQUE,
  `password_hash` VARCHAR(255) NOT NULL,
  `full_name` VARCHAR(255) NOT NULL,
  `role` ENUM('household', 'provider') NOT NULL DEFAULT 'household',
  `phone` VARCHAR(50) DEFAULT '',
  `address` TEXT DEFAULT '',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_users_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Households Table
CREATE TABLE IF NOT EXISTS `households` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `home_type` VARCHAR(100) DEFAULT 'Apartment',
  `size_sqft` INT DEFAULT 1200,
  `occupants` INT DEFAULT 4,
  `location` VARCHAR(150) DEFAULT 'Mumbai',
  `monthly_budget` DECIMAL(10, 2) DEFAULT 3500.00,
  `solar_available` TINYINT(1) DEFAULT 0,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Providers Table
CREATE TABLE IF NOT EXISTS `providers` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `business_name` VARCHAR(255) NOT NULL,
  `categories` VARCHAR(255) NOT NULL,
  `experience_years` INT DEFAULT 5,
  `location` VARCHAR(150) DEFAULT 'Mumbai',
  `base_price` VARCHAR(100) DEFAULT '₹500 - ₹2000',
  `description` TEXT,
  `availability_status` VARCHAR(50) DEFAULT 'Available',
  `rating` DECIMAL(3, 2) DEFAULT 4.80,
  `verified` TINYINT(1) DEFAULT 1,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Appliances Table
CREATE TABLE IF NOT EXISTS `appliances` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `household_id` INT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `category` VARCHAR(100) NOT NULL DEFAULT 'General',
  `quantity` INT DEFAULT 1,
  `power_rating_watts` DECIMAL(10, 2) DEFAULT 500.00,
  `usage_hours_per_day` DECIMAL(5, 2) DEFAULT 4.00,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_appliances_household` (`household_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Household Bills Table
CREATE TABLE IF NOT EXISTS `household_bills` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `household_id` INT NOT NULL,
  `amount` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
  `units` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
  `billing_period` VARCHAR(100) NOT NULL DEFAULT 'Current Utility Bill',
  `tariff_rate` DECIMAL(6, 2) DEFAULT 7.50,
  `fixed_charges` DECIMAL(8, 2) DEFAULT 250.00,
  `taxes` DECIMAL(8, 2) DEFAULT 0.00,
  `other_charges` DECIMAL(8, 2) DEFAULT 0.00,
  `discom` VARCHAR(255) DEFAULT 'Utility Provider',
  `source` VARCHAR(100) DEFAULT 'bill_analyzer',
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_bills_household` (`household_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Energy Readings Table
CREATE TABLE IF NOT EXISTS `energy_readings` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `household_id` INT NOT NULL,
  `date` VARCHAR(10) NOT NULL,
  `kwh` DECIMAL(8, 3) NOT NULL,
  `source` VARCHAR(100) DEFAULT 'Grid Meter',
  `notes` VARCHAR(255) DEFAULT '',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_readings_hh_date` (`household_id`, `date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Service Requests Table
CREATE TABLE IF NOT EXISTS `service_requests` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `provider_id` INT NOT NULL,
  `service_type` VARCHAR(150) NOT NULL,
  `description` TEXT,
  `requested_date` VARCHAR(50) NOT NULL,
  `address` TEXT,
  `status` VARCHAR(50) DEFAULT 'Pending',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`provider_id`) REFERENCES `providers`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. Chat Messages Table
CREATE TABLE IF NOT EXISTS `chat_messages` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `conversation_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `sender` ENUM('user', 'assistant') NOT NULL,
  `content` TEXT NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. ML Forecast Logs Table
CREATE TABLE IF NOT EXISTS `ml_forecast_logs` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `household_id` INT NOT NULL,
  `best_model` VARCHAR(100) NOT NULL,
  `linear_regression_rmse` DECIMAL(8, 4),
  `random_forest_rmse` DECIMAL(8, 4),
  `xgboost_rmse` DECIMAL(8, 4),
  `forecast_days` INT DEFAULT 30,
  `predicted_total_kwh` DECIMAL(10, 3),
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

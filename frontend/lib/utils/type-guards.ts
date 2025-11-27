/**
 * Type Guards - Runtime Type Validation
 * Backend'den gelen veriyi güvenle dönüştürmek için
 */

import { VALID_TOPIC_STATUSES, ValidTopicStatus } from '../constants';

/**
 * Backend'den gelen status'un geçerli olup olmadığını kontrol eder
 */
export function isValidTopicStatus(status: string): status is ValidTopicStatus {
  return VALID_TOPIC_STATUSES.includes(status as ValidTopicStatus);
}

/**
 * Güvenli status dönüşümü - Geçersizse fallback döner
 */
export function parseTopicStatus(status: string): ValidTopicStatus {
  if (isValidTopicStatus(status)) {
    return status;
  }
  
  console.warn(`⚠️ Invalid topic status received: "${status}". Falling back to "warning"`);
  return 'warning'; // Fallback
}

/**
 * Number validation - NaN kontrolü
 */
export function safeNumber(value: number | undefined | null, fallback: number = 0): number {
  if (typeof value === 'number' && !isNaN(value)) {
    return value;
  }
  return fallback;
}

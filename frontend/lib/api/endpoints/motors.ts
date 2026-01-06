/**
 * Motor API Endpoints
 * End.STP - Motor v2 Integration
 */

import { api } from '../client';

// ============================================
// TYPES
// ============================================

export interface MotorResponse<T = any> {
  data: T;
  meta: {
    motor_version: string;
    fallback_used: boolean;
    tier: string;
  };
}

export interface BSModelResult {
  status: string;
  next_ef: number;
  next_ia: number;
  next_repetition: number;
  score: number;
  analysis: string;
  v2_features?: {
    k_forget: number;
    segment_risk_factor: number;
    integrity_score: number;
    evidence_confidence: number;
    behavioral_multiplier: number;
    archetype: string;
  };
  adjusted_interval: number;
  why_this_interval: string;
  motor_version: string;
}

export interface DifficultyResult {
  topic_id: string;
  difficulty_score: number;
  difficulty_level: string;
  factors: {
    blank_contribution: number;
    wrong_contribution: number;
    volatility_contribution: number;
    misconception_contribution: number;
  };
  analysis: string;
  archetype_context: {
    archetype: string;
    expected_difficulty: string;
    urgency: string;
    note: string | null;
  };
  prerequisite_health: {
    has_prerequisites: boolean;
    weak_prerequisites: any[];
  };
  segment_context: {
    level: string;
    confidence: number;
  };
}

// ============================================
// MOTOR CALCULATIONS
// ============================================

/**
 * Calculate all motors for a test result
 */
export async function calculateAllMotors(params: {
  student_id: string;
  topic_id: string;
  correct: number;
  incorrect: number;
  blank: number;
  total: number;
  time_spent: number; // seconds
  test_date: string; // YYYY-MM-DD
  user_tier?: string;
}) {
  const tier = params.user_tier || 'free';

  try {
    // Call all 4 motors in parallel
    const [bsModel, difficulty, priority, time] = await Promise.allSettled([
      // BS-Model
      api.post<MotorResponse<BSModelResult>>(
        `/motors/bs-model/calculate?topic_id=${params.topic_id}&correct=${params.correct}&incorrect=${params.incorrect}&blank=${params.blank}&total=${params.total}&user_tier=${tier}`,
        null
      ),

      // Difficulty
      api.post<MotorResponse<DifficultyResult>>(
        `/motors/difficulty/calculate?student_id=${params.student_id}&topic_id=${params.topic_id}&questions_total=${params.total}&questions_correct=${params.correct}&questions_wrong=${params.incorrect}&questions_blank=${params.blank}&user_tier=${tier}`,
        null
      ),

      // Priority
      api.post<MotorResponse>(
        `/motors/priority/calculate?topic_id=${params.topic_id}&test_date=${params.test_date}&user_tier=${tier}`,
        null
      ),

      // Time
      api.post<MotorResponse>(
        `/motors/time/calculate?topic_id=${params.topic_id}&time_spent=${params.time_spent}&total=${params.total}&user_tier=${tier}`,
        null
      ),
    ]);

    return {
      bsModel: bsModel.status === 'fulfilled' ? bsModel.value : null,
      difficulty: difficulty.status === 'fulfilled' ? difficulty.value : null,
      priority: priority.status === 'fulfilled' ? priority.value : null,
      time: time.status === 'fulfilled' ? time.value : null,
      errors: {
        bsModel: bsModel.status === 'rejected' ? bsModel.reason : null,
        difficulty: difficulty.status === 'rejected' ? difficulty.reason : null,
        priority: priority.status === 'rejected' ? priority.reason : null,
        time: time.status === 'rejected' ? time.reason : null,
      },
    };
  } catch (error) {
    console.error('Motor calculation error:', error);
    throw error;
  }
}

/**
 * Individual motor functions (for separate calls)
 */

export async function calculateBSModel(params: {
  topic_id: string;
  correct: number;
  incorrect: number;
  blank: number;
  total: number;
  user_tier?: string;
}) {
  const tier = params.user_tier || 'free';
  return api.post<MotorResponse<BSModelResult>>(
    `/motors/bs-model/calculate?topic_id=${params.topic_id}&correct=${params.correct}&incorrect=${params.incorrect}&blank=${params.blank}&total=${params.total}&user_tier=${tier}`,
    null
  );
}

export async function calculateDifficulty(params: {
  student_id: string;
  topic_id: string;
  questions_total: number;
  questions_correct: number;
  questions_wrong: number;
  questions_blank: number;
  user_tier?: string;
}) {
  const tier = params.user_tier || 'free';
  return api.post<MotorResponse<DifficultyResult>>(
    `/motors/difficulty/calculate?student_id=${params.student_id}&topic_id=${params.topic_id}&questions_total=${params.questions_total}&questions_correct=${params.questions_correct}&questions_wrong=${params.questions_wrong}&questions_blank=${params.questions_blank}&user_tier=${tier}`,
    null
  );
}

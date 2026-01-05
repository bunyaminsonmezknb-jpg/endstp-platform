"""
Master Difficulty Engine v2.6 (Production-Hardened)
====================================================
mevcut v2 ile birleştirerek v3 yapabiliriz. bunu bracha al log temelli veri topla
CHANGELOG v2.5 → v2.6:
- FIX #1: All datetime handling now UTC-based
- FIX #2: HIGH_RISK requires 3-test average negative net
- FIX #3: Prerequisite adjustment uses ceiling, not multiplication
- FIX #4: Speed warning added for standard segment (soft message)
- FIX #5: Circadian uses entry_timestamp.hour, not current time
- FIX #6: Low confidence flagged in message, not difficulty reduction
- FIX #7: Comprehensive edge-case guards added

15 Features Integrated:
1. Prerequisite Awareness
2. BS-Model Integration (Personalized Decay)
3. Course Context Weight
4. Statistical Confidence
5. Volatility Improvement (Outlier Detection)
6. Bidirectional Sentinel (Positive + Negative Anomaly)
7. Speed Normalization (Topic Benchmarks)
8. Metacognition Gap (Feedback Loop Calibration)
9. Exam System Awareness (Global-First)
10. Version Handling (API Evolution)
11. Digital Exhaust Integration
12. Recovery Velocity
13. Contextual Sentiment
14. Circadian Alignment
15. Trust-Weighted Feedback

Author: End.STP Team
Date: 2024-12-27
Version: 2.6.0
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta, date, timezone
from decimal import Decimal
import statistics
from dataclasses import dataclass, field
from enum import Enum


# ============================================
# ENUMS & CONSTANTS
# ============================================

class StudentSegment(str, Enum):
    """Student performance segments"""
    STRUGGLING = "struggling"      # <50% success
    STANDARD = "standard"          # 50-90% success
    ELITE = "elite"                # 90%+ success


class BehaviorMode(str, Enum):
    """Student behavior patterns"""
    NORMAL = "normal"
    HIGH_PRECISION = "high_precision"      # Elite, stable
    AT_RISK = "at_risk"                    # High blank rate
    PLATEAU = "plateau"                    # Stuck in range
    ANOMALOUS_DECAY = "anomalous_decay"    # Elite collapse
    POSITIVE_BREAKTHROUGH = "positive_breakthrough"  # Struggling improvement
    ERRATIC_WITH_ANOMALY = "erratic_with_anomaly"   # Outlier detected
    HIGH_RISK = "high_risk"                # Negative net score (3-test avg)


class TrendDirection(str, Enum):
    """Performance trend"""
    IMPROVING = "improving"
    DECLINING = "declining"
    STABLE = "stable"


# Constants
FIRST_CONTACT_HOURS = 8          # Hours between tests to count as new session
TIME_DECAY_THRESHOLD_DAYS = 15   # Days before decay risk kicks in
NEGATIVE_NET_THRESHOLD = 0       # Net < 0 = high risk
ELITE_THRESHOLD = 90             # Elite segment threshold
STRUGGLING_THRESHOLD = 50        # Struggling segment threshold
CONFIDENCE_MIN_QUESTIONS = 5     # Minimum questions for confidence
CONFIDENCE_MIN_TESTS = 3         # Minimum tests for confidence
CONFIDENCE_MIN_DAYS = 7          # Minimum day span for confidence
HIGH_RISK_TEST_COUNT = 3         # Number of tests for HIGH_RISK pattern


# ============================================
# HELPER FUNCTIONS
# ============================================

def utc_now() -> datetime:
    """Get current UTC time - centralized for consistency"""
    return datetime.now(timezone.utc)


def safe_mean(values: List[float], default: float = 0.0) -> float:
    """Safe mean calculation with fallback"""
    if not values:
        return default
    try:
        return statistics.mean(values)
    except statistics.StatisticsError:
        return default


def safe_stdev(values: List[float], default: float = 0.0) -> float:
    """Safe standard deviation with fallback"""
    if len(values) < 2:
        return default
    try:
        return statistics.stdev(values)
    except statistics.StatisticsError:
        return default


# ============================================
# DATA CLASSES
# ============================================

@dataclass
class TestData:
    """Single test record"""
    test_id: str
    topic_id: str
    test_date: date
    total_questions: int
    correct: int
    wrong: int
    blank: int
    time_seconds: int
    entry_timestamp: datetime  # MUST be UTC
    
    def __post_init__(self):
        """Validate and ensure UTC"""
        # Ensure entry_timestamp is timezone-aware UTC
        if self.entry_timestamp.tzinfo is None:
            self.entry_timestamp = self.entry_timestamp.replace(tzinfo=timezone.utc)
        
        # Validation
        if self.total_questions <= 0:
            raise ValueError("total_questions must be positive")
        if self.correct + self.wrong + self.blank != self.total_questions:
            raise ValueError("correct + wrong + blank must equal total_questions")
    
    @property
    def success_rate(self) -> float:
        """Success rate percentage"""
        return (self.correct / self.total_questions) * 100
    
    @property
    def net_score(self) -> float:
        """Net = Correct - (Wrong + Blank)"""
        return self.correct - (self.wrong + self.blank)
    
    @property
    def blank_rate(self) -> float:
        """Blank rate percentage"""
        return (self.blank / self.total_questions) * 100
    
    @property
    def wrong_rate(self) -> float:
        """Wrong rate percentage"""
        return (self.wrong / self.total_questions) * 100
    
    @property
    def speed_per_question(self) -> float:
        """Average seconds per question"""
        return self.time_seconds / self.total_questions


@dataclass
class PrerequisiteGap:
    """Prerequisite analysis result"""
    gap_exists: bool
    missing_prerequisites: List[Dict]
    max_difficulty_ceiling: float  # FIX #3: Ceiling, not multiplier
    recommendation: str


@dataclass
class SpeedAnalysis:
    """Speed factor analysis"""
    avg_speed: float  # seconds per question
    benchmark_speed: float
    is_slow: bool
    penalty: float  # 0-0.15
    segment: StudentSegment
    warning_message: Optional[str] = None  # FIX #4: Soft warning for standard


@dataclass
class MetacognitionAnalysis:
    """Metacognition gap analysis"""
    perceived_difficulty: Optional[float]
    calculated_difficulty: float
    gap: float
    pattern: str  # "dunning_kruger", "low_confidence", "well_calibrated"
    trust_score: float
    recommendation: str


@dataclass
class DifficultyFactors:
    """All difficulty calculation factors"""
    # Core metrics
    base_difficulty: float
    blank_weight: float
    wrong_weight: float
    volatility: float
    
    # Enhancements
    prerequisite_ceiling: Optional[float] = None  # FIX #3: Ceiling instead of adjustment
    bs_model_decay_risk: float = 0.0
    course_context_multiplier: float = 1.0
    speed_penalty: float = 0.0
    speed_warning: Optional[str] = None  # FIX #4: Soft warning
    time_decay_bonus: float = 0.0
    
    # Statistical
    confidence_score: float = 1.0
    confidence_warning: Optional[str] = None  # FIX #6: Flag instead of reduction
    sample_size: int = 0
    
    # Metacognition
    metacognitive_gap: float = 0.0
    trust_weighted_adjustment: float = 0.0
    
    # Behavioral
    digital_exhaust_factor: float = 1.0
    recovery_velocity_bonus: float = 0.0
    
    # Context
    exam_system_multiplier: float = 1.0
    circadian_penalty: float = 0.0
    circadian_timestamp: Optional[datetime] = None  # FIX #5: Track actual test time
    
    # Counts
    daily_discarded_tests_count: int = 0
    outliers_detected: int = 0


@dataclass
class DifficultyResult:
    """Final difficulty calculation result"""
    difficulty_percentage: float  # 0-100
    difficulty_level: int  # 1-5
    student_segment: StudentSegment
    behavior_mode: BehaviorMode
    trend: TrendDirection
    factors: DifficultyFactors
    student_message: str
    coach_message: str
    recommendations: List[str]
    confidence_level: str  # "low", "medium", "high"
    warnings: List[str] = field(default_factory=list)  # FIX #6: Explicit warnings
    api_version: str = "2.0"
    engine_version: str = "master_v2.6"


# ============================================
# MASTER DIFFICULTY ENGINE
# ============================================

class MasterDifficultyEngine:
    """
    Master Difficulty Engine v2.6 (Production-Hardened)
    
    Combines pedagogical soundness with engineering precision.
    Includes 15 advanced features for accurate difficulty assessment.
    """
    
    def __init__(
        self,
        enable_prerequisite: bool = True,
        enable_bs_model: bool = True,
        enable_course_context: bool = True,
        enable_speed: bool = True,
        enable_metacognition: bool = True,
        enable_digital_exhaust: bool = True,
        enable_circadian: bool = True
    ):
        """
        Initialize engine with feature flags.
        
        Args:
            enable_*: Feature toggles for modular functionality
        """
        self.enable_prerequisite = enable_prerequisite
        self.enable_bs_model = enable_bs_model
        self.enable_course_context = enable_course_context
        self.enable_speed = enable_speed
        self.enable_metacognition = enable_metacognition
        self.enable_digital_exhaust = enable_digital_exhaust
        self.enable_circadian = enable_circadian
    
    def calculate_difficulty(
        self,
        student_id: str,
        topic_id: str,
        tests: List[TestData],
        prerequisite_data: Optional[Dict] = None,
        bs_model_data: Optional[Dict] = None,
        course_data: Optional[Dict] = None,
        speed_benchmark: Optional[Dict] = None,
        feedback_data: Optional[Dict] = None,
        learning_profile: Optional[Dict] = None,
        exam_system: Optional[Dict] = None
    ) -> DifficultyResult:
        """
        Master calculation method.
        
        Args:
            student_id: Student UUID
            topic_id: Topic UUID
            tests: List of test records
            prerequisite_data: Prerequisite analysis
            bs_model_data: BS-Model forgetting curve data
            course_data: Subject-level performance
            speed_benchmark: Topic speed benchmarks
            feedback_data: Student feedback history
            learning_profile: Student behavioral profile
            exam_system: Exam system configuration
            
        Returns:
            DifficultyResult with comprehensive analysis
        """
        
        # Step 1: Filter tests (First-Contact Rule)
        filtered_tests, discarded_count = self._filter_first_contact_tests(tests)
        
        if not filtered_tests:
            return self._create_insufficient_data_result(discarded_count)
        
        # Step 2: Determine student segment
        avg_success = safe_mean([t.success_rate for t in filtered_tests])
        segment = self._determine_segment(avg_success)
        
        # Step 3: Calculate base difficulty
        base_difficulty = self._calculate_base_difficulty(filtered_tests, segment)
        
        # Step 4: Calculate volatility (with outlier detection)
        volatility, outliers_count = self._calculate_volatility_advanced(filtered_tests)
        
        # Step 5: Calculate trend
        trend = self._calculate_trend(filtered_tests)
        
        # Step 6: Initialize factors
        factors = DifficultyFactors(
            base_difficulty=base_difficulty,
            blank_weight=self._get_blank_weight(segment),
            wrong_weight=self._get_wrong_weight(segment),
            volatility=volatility,
            sample_size=len(filtered_tests),
            daily_discarded_tests_count=discarded_count,
            outliers_detected=outliers_count
        )
        
        # Step 7: Apply enhancements
        
        # Enhancement 1: Prerequisite Awareness (FIX #3: Ceiling, not multiplication)
        if self.enable_prerequisite and prerequisite_data:
            prereq_gap = self._calculate_prerequisite_gap(prerequisite_data)
            if prereq_gap.gap_exists:
                factors.prerequisite_ceiling = prereq_gap.max_difficulty_ceiling
        
        # Enhancement 2: BS-Model Integration (FIX #1: UTC-based)
        if self.enable_bs_model and bs_model_data:
            days_since_last = (utc_now().date() - filtered_tests[-1].test_date).days
            factors.bs_model_decay_risk = self._calculate_bs_model_decay(
                bs_model_data,
                days_since_last
            )
        
        # Enhancement 3: Course Context Weight
        if self.enable_course_context and course_data:
            factors.course_context_multiplier = self._calculate_course_multiplier(
                course_data,
                avg_success
            )
        
        # Enhancement 4: Statistical Confidence (FIX #6: Flag, not reduction)
        days_span = (utc_now().date() - filtered_tests[0].test_date).days
        confidence_score, confidence_level, confidence_warning = self._calculate_confidence(
            filtered_tests,
            days_span
        )
        factors.confidence_score = confidence_score
        factors.confidence_warning = confidence_warning
        
        # Enhancement 5: Time Decay (FIX #1: UTC-based)
        days_since_last = (utc_now().date() - filtered_tests[-1].test_date).days
        if days_since_last >= TIME_DECAY_THRESHOLD_DAYS:
            factors.time_decay_bonus = min(0.10, days_since_last * 0.004)
        
        # Enhancement 7: Speed Normalization (FIX #4: Warning for standard)
        if self.enable_speed and speed_benchmark:
            speed_analysis = self._analyze_speed(filtered_tests, speed_benchmark, segment)
            factors.speed_penalty = speed_analysis.penalty
            factors.speed_warning = speed_analysis.warning_message
        
        # Enhancement 8: Metacognition Gap
        metacog_analysis = None
        if self.enable_metacognition and feedback_data:
            metacog_analysis = self._analyze_metacognition(
                feedback_data,
                avg_success,
                learning_profile
            )
            factors.metacognitive_gap = metacog_analysis.gap
            factors.trust_weighted_adjustment = metacog_analysis.trust_score
        
        # Enhancement 9: Exam System Awareness
        if exam_system:
            factors.exam_system_multiplier = exam_system.get('difficulty_multiplier', 1.0)
        
        # Enhancement 11: Digital Exhaust
        if self.enable_digital_exhaust and feedback_data:
            factors.digital_exhaust_factor = self._calculate_digital_exhaust_factor(
                feedback_data
            )
        
        # Enhancement 12: Recovery Velocity
        if learning_profile:
            factors.recovery_velocity_bonus = self._calculate_recovery_bonus(
                learning_profile
            )
        
        # Enhancement 14: Circadian Alignment (FIX #5: Use entry_timestamp)
        if self.enable_circadian and learning_profile and filtered_tests:
            # Use most recent test's timestamp
            latest_test_timestamp = filtered_tests[-1].entry_timestamp
            factors.circadian_penalty = self._calculate_circadian_penalty(
                learning_profile,
                latest_test_timestamp
            )
            factors.circadian_timestamp = latest_test_timestamp
        
        # Step 8: Determine behavior mode (FIX #2: 3-test average for HIGH_RISK)
        behavior_mode = self._determine_behavior_mode(
            segment,
            filtered_tests,
            volatility,
            trend,
            outliers_count,
            avg_success
        )
        
        # Step 9: Calculate final difficulty
        final_difficulty = self._calculate_final_difficulty(factors, segment)
        difficulty_level = self._difficulty_to_level(final_difficulty)
        
        # Step 10: Collect warnings
        warnings = self._collect_warnings(factors, confidence_level)
        
        # Step 11: Generate messages
        student_message, coach_message, recommendations = self._generate_messages(
            segment,
            behavior_mode,
            trend,
            final_difficulty,
            factors,
            metacog_analysis,
            warnings
        )
        
        # Step 12: Build result
        return DifficultyResult(
            difficulty_percentage=final_difficulty,
            difficulty_level=difficulty_level,
            student_segment=segment,
            behavior_mode=behavior_mode,
            trend=trend,
            factors=factors,
            student_message=student_message,
            coach_message=coach_message,
            recommendations=recommendations,
            confidence_level=confidence_level,
            warnings=warnings
        )
    
    # ============================================
    # CORE CALCULATIONS
    # ============================================
    
    def _filter_first_contact_tests(
        self,
        tests: List[TestData]
    ) -> Tuple[List[TestData], int]:
        """
        Enhancement #0: First-Contact Rule
        
        Only keep first test of each day OR tests 8+ hours apart.
        Exclude blank tests entirely.
        
        Returns:
            (filtered_tests, discarded_count)
        """
        if not tests:
            return [], 0
        
        # Sort by test_date, then entry_timestamp
        sorted_tests = sorted(tests, key=lambda t: (t.test_date, t.entry_timestamp))
        
        filtered = []
        discarded = 0
        last_timestamp = None
        
        for test in sorted_tests:
            # Exclude blank tests
            if test.blank == test.total_questions:
                discarded += 1
                continue
            
            # First test always included
            if not filtered:
                filtered.append(test)
                last_timestamp = test.entry_timestamp
                continue
            
            # Check time gap
            time_gap = test.entry_timestamp - last_timestamp
            hours_gap = time_gap.total_seconds() / 3600
            
            # Different day OR 8+ hours apart
            if test.test_date != filtered[-1].test_date or hours_gap >= FIRST_CONTACT_HOURS:
                filtered.append(test)
                last_timestamp = test.entry_timestamp
            else:
                discarded += 1
        
        return filtered, discarded
    
    def _determine_segment(self, avg_success: float) -> StudentSegment:
        """Determine student segment based on success rate"""
        if avg_success >= ELITE_THRESHOLD:
            return StudentSegment.ELITE
        elif avg_success < STRUGGLING_THRESHOLD:
            return StudentSegment.STRUGGLING
        else:
            return StudentSegment.STANDARD
    
    def _calculate_base_difficulty(
        self,
        tests: List[TestData],
        segment: StudentSegment
    ) -> float:
        """
        Calculate base difficulty using weighted formula.
        
        Formula: (Blank × 0.55) + (Wrong × 0.30) + (Volatility × 0.10)
        """
        if not tests:
            return 50.0
        
        # Calculate averages
        avg_blank_rate = safe_mean([t.blank_rate for t in tests])
        avg_wrong_rate = safe_mean([t.wrong_rate for t in tests])
        
        # Segment-specific coefficients
        blank_coef = self._get_blank_weight(segment)
        wrong_coef = self._get_wrong_weight(segment)
        
        # Base formula
        base = (avg_blank_rate * blank_coef) + (avg_wrong_rate * wrong_coef)
        
        return min(100.0, max(0.0, base))
    
    def _get_blank_weight(self, segment: StudentSegment) -> float:
        """Blank coefficient by segment"""
        if segment == StudentSegment.STRUGGLING:
            return 0.60  # Blanks more critical
        elif segment == StudentSegment.ELITE:
            return 0.45  # Errors more critical
        else:
            return 0.55  # Balanced
    
    def _get_wrong_weight(self, segment: StudentSegment) -> float:
        """Wrong coefficient by segment"""
        if segment == StudentSegment.STRUGGLING:
            return 0.25  # Blanks weighted higher
        elif segment == StudentSegment.ELITE:
            return 0.40  # Errors very critical
        else:
            return 0.30  # Balanced
    
    def _calculate_volatility_advanced(
        self,
        tests: List[TestData]
    ) -> Tuple[float, int]:
        """
        Enhancement #5: Volatility with Outlier Detection
        
        Returns:
            (volatility_score, outliers_count)
        """
        if len(tests) < 2:
            return 0.0, 0
        
        success_rates = [t.success_rate for t in tests]
        
        # Simple range for < 5 tests
        if len(tests) < 5:
            return max(success_rates) - min(success_rates), 0
        
        # 2-sigma outlier detection
        mean = safe_mean(success_rates)
        std_dev = safe_stdev(success_rates)
        
        if std_dev == 0:
            return 0.0, 0
        
        outliers = [rate for rate in success_rates if abs(rate - mean) > 2 * std_dev]
        clean_data = [rate for rate in success_rates if rate not in outliers]
        
        if len(clean_data) < 2:
            return max(success_rates) - min(success_rates), len(outliers)
        
        clean_std_dev = safe_stdev(clean_data)
        volatility_score = min(100.0, clean_std_dev * 2)
        
        return volatility_score, len(outliers)
    
    def _calculate_trend(self, tests: List[TestData]) -> TrendDirection:
        """Calculate performance trend"""
        if len(tests) < 3:
            return TrendDirection.STABLE
        
        # Compare recent 3 vs previous 3
        recent_avg = safe_mean([t.success_rate for t in tests[-3:]])
        
        if len(tests) >= 6:
            previous_avg = safe_mean([t.success_rate for t in tests[-6:-3]])
        else:
            previous_avg = safe_mean([t.success_rate for t in tests[:-3]])
        
        delta = recent_avg - previous_avg
        
        if delta > 5:
            return TrendDirection.IMPROVING
        elif delta < -5:
            return TrendDirection.DECLINING
        else:
            return TrendDirection.STABLE
    
    # ============================================
    # ENHANCEMENTS
    # ============================================
    
    def _calculate_prerequisite_gap(
        self,
        prerequisite_data: Dict
    ) -> PrerequisiteGap:
        """
        Enhancement #1: Prerequisite Awareness (FIX #3: Ceiling instead of multiplier)
        
        If prerequisite gaps exist, sets MAX difficulty ceiling.
        Doesn't multiply difficulty (prevents double-counting).
        
        Returns PrerequisiteGap with ceiling.
        """
        gap_exists = prerequisite_data.get('gap_exists', False)
        
        if not gap_exists:
            return PrerequisiteGap(
                gap_exists=False,
                missing_prerequisites=[],
                max_difficulty_ceiling=100.0,  # No ceiling
                recommendation=""
            )
        
        missing = prerequisite_data.get('missing_prerequisites', [])
        
        if not missing:
            return PrerequisiteGap(
                gap_exists=False,
                missing_prerequisites=[],
                max_difficulty_ceiling=100.0,
                recommendation=""
            )
        
        # Calculate weighted gap
        total_gap = sum(p.get('gap_percentage', 0) * p.get('strength', 1.0) for p in missing)
        
        # Set ceiling based on gap severity
        # Large gap = low ceiling (e.g., max 60% difficulty)
        # Small gap = high ceiling (e.g., max 85% difficulty)
        ceiling = max(50.0, 100.0 - (total_gap / 2))
        
        prereq_names = [p.get('name', 'Unknown') for p in missing]
        recommendation = f"Complete prerequisites first: {', '.join(prereq_names[:3])}"
        
        return PrerequisiteGap(
            gap_exists=True,
            missing_prerequisites=missing,
            max_difficulty_ceiling=ceiling,
            recommendation=recommendation
        )
    
    def _calculate_bs_model_decay(
        self,
        bs_model_data: Dict,
        days_since_last: int
    ) -> float:
        """
        Enhancement #2: BS-Model Integration (Personalized Decay)
        
        Instead of fixed decay, use student's remembering rate.
        """
        if days_since_last < TIME_DECAY_THRESHOLD_DAYS:
            return 0.0
        
        remembering_rate = bs_model_data.get('current_remembering_rate', 70)
        
        # Guard against invalid values
        remembering_rate = max(0, min(100, remembering_rate))
        
        # Decay risk based on forgetting
        # Low remembering = high decay risk
        decay_risk = (100 - remembering_rate) * 0.002
        
        return min(0.15, decay_risk)
    
    def _calculate_course_multiplier(
        self,
        course_data: Dict,
        topic_success: float
    ) -> float:
        """
        Enhancement #3: Course Context Weight
        
        Topic difficulty relative to subject performance.
        """
        subject_avg = course_data.get('subject_avg_success', 70)
        
        # Guard against invalid values
        subject_avg = max(0, min(100, subject_avg))
        
        if subject_avg < 50:
            return 1.3  # Weak overall → Every topic critical
        elif subject_avg < 70:
            return 1.1  # Developing
        elif subject_avg >= 85:
            return 0.9  # Strong overall → Less critical
        else:
            return 1.0  # Standard
    
    def _calculate_confidence(
        self,
        tests: List[TestData],
        days_span: int
    ) -> Tuple[float, str, Optional[str]]:
        """
        Enhancement #4: Statistical Confidence (FIX #6: Flag instead of reduction)
        
        Returns:
            (confidence_score 0-1, confidence_level string, warning_message)
        """
        total_questions = sum(t.total_questions for t in tests)
        num_tests = len(tests)
        
        # Sample size confidence
        if total_questions < CONFIDENCE_MIN_QUESTIONS:
            sample_conf = 0.2
        elif total_questions >= 20:
            sample_conf = 1.0
        else:
            sample_conf = total_questions / 20
        
        # Test frequency confidence
        if num_tests < CONFIDENCE_MIN_TESTS:
            freq_conf = 0.3
        elif num_tests >= 5:
            freq_conf = 1.0
        else:
            freq_conf = num_tests / 5
        
        # Time span confidence
        if days_span < CONFIDENCE_MIN_DAYS:
            time_conf = 0.5
        elif days_span >= 30:
            time_conf = 1.0
        else:
            time_conf = days_span / 30
        
        # Weighted average
        overall_conf = (sample_conf * 0.4) + (freq_conf * 0.4) + (time_conf * 0.2)
        
        # Level
        if overall_conf >= 0.7:
            level = "high"
            warning = None
        elif overall_conf >= 0.4:
            level = "medium"
            warning = "ℹ️ Moderate confidence - more data recommended"
        else:
            level = "low"
            warning = f"⚠️ Low confidence - Need {CONFIDENCE_MIN_QUESTIONS - total_questions}+ questions, {CONFIDENCE_MIN_TESTS - num_tests}+ tests"
        
        return overall_conf, level, warning
    
    def _analyze_speed(
        self,
        tests: List[TestData],
        speed_benchmark: Dict,
        segment: StudentSegment
    ) -> SpeedAnalysis:
        """
        Enhancement #7: Speed Normalization (FIX #4: Warning for standard segment)
        
        For elite students, slow speed = penalty.
        For standard students, slow speed = soft warning.
        """
        avg_speed = safe_mean([t.speed_per_question for t in tests])
        
        # Guard: No benchmark data
        if not speed_benchmark:
            return SpeedAnalysis(
                avg_speed=avg_speed,
                benchmark_speed=0,
                is_slow=False,
                penalty=0.0,
                segment=segment,
                warning_message=None
            )
        
        # Elite: Speed critical, apply penalty
        if segment == StudentSegment.ELITE:
            benchmark = speed_benchmark.get('elite_threshold_seconds', 60)
            tolerance = 1.15  # 15% slower = problem
            
            is_slow = avg_speed > (benchmark * tolerance)
            
            if not is_slow:
                penalty = 0.0
                warning = None
            else:
                slowness_ratio = avg_speed / benchmark
                penalty = min(0.15, (slowness_ratio - tolerance) * 0.1)
                warning = f"⚠️ Speed issue: {avg_speed:.1f}s vs {benchmark:.1f}s benchmark"
        
        # Standard: Speed informative, soft warning only (FIX #4)
        elif segment == StudentSegment.STANDARD:
            benchmark = speed_benchmark.get('standard_threshold_seconds', 90)
            tolerance = 1.25  # 25% slower = soft warning
            
            is_slow = avg_speed > (benchmark * tolerance)
            penalty = 0.0  # No penalty for standard
            
            if is_slow:
                warning = f"ℹ️ Consider speed practice: {avg_speed:.1f}s vs {benchmark:.1f}s recommended"
            else:
                warning = None
        
        # Struggling: Speed not relevant
        else:
            return SpeedAnalysis(
                avg_speed=avg_speed,
                benchmark_speed=0,
                is_slow=False,
                penalty=0.0,
                segment=segment,
                warning_message=None
            )
        
        return SpeedAnalysis(
            avg_speed=avg_speed,
            benchmark_speed=benchmark,
            is_slow=is_slow,
            penalty=penalty,
            segment=segment,
            warning_message=warning
        )
    
    def _analyze_metacognition(
        self,
        feedback_data: Dict,
        actual_success: float,
        learning_profile: Optional[Dict]
    ) -> MetacognitionAnalysis:
        """
        Enhancement #8: Metacognition Gap (Feedback Loop Calibration)
        
        Analyzes student's self-assessment vs actual performance.
        """
        feedbacks = feedback_data.get('recent_feedbacks', [])
        
        if not feedbacks:
            return MetacognitionAnalysis(
                perceived_difficulty=None,
                calculated_difficulty=actual_success,
                gap=0.0,
                pattern="well_calibrated",
                trust_score=1.0,
                recommendation=""
            )
        
        avg_perceived = safe_mean([f.get('perceived_difficulty', 0) for f in feedbacks])
        avg_calculated = safe_mean([f.get('calculated_difficulty', 0) for f in feedbacks])
        
        # Gap (positive = thinks harder, negative = thinks easier)
        gap = avg_perceived - avg_calculated
        
        # Trust score from profile
        trust_score = 1.0
        if learning_profile:
            trust_score = learning_profile.get('trust_score', 1.0)
            trust_score = max(0.0, min(1.0, trust_score))  # Guard
        
        # Detect pattern
        if gap < -1.5 and actual_success < 60:
            pattern = "dunning_kruger"
            recommendation = "⚠️ Overconfidence risk! Performance low but you think it's easy."
        elif gap > 1.5 and actual_success > 75:
            pattern = "low_confidence"
            recommendation = "💪 Trust yourself more! You're performing well."
        else:
            pattern = "well_calibrated"
            recommendation = ""
        
        return MetacognitionAnalysis(
            perceived_difficulty=avg_perceived,
            calculated_difficulty=avg_calculated,
            gap=gap,
            pattern=pattern,
            trust_score=trust_score,
            recommendation=recommendation
        )
    
    def _calculate_digital_exhaust_factor(self, feedback_data: Dict) -> float:
        """
        Enhancement #11: Digital Exhaust Integration
        
        Low trust feedback = weighted down.
        """
        avg_dwell = feedback_data.get('avg_dwell_time', 30)
        
        # Guard against invalid values
        avg_dwell = max(0, avg_dwell)
        
        # Rushed feedback (<2 seconds) = low trust
        if avg_dwell < 2:
            return 0.5  # 50% weight
        elif avg_dwell < 5:
            return 0.7  # 70% weight
        else:
            return 1.0  # Full weight
    
    def _calculate_recovery_bonus(self, learning_profile: Dict) -> float:
        """
        Enhancement #12: Recovery Velocity
        
        High resilience = small positive adjustment.
        """
        resilience = learning_profile.get('resilience_score', 0.5)
        
        # Guard
        resilience = max(0.0, min(1.0, resilience))
        
        if resilience > 0.8:
            return -0.05  # Reduce difficulty slightly
        else:
            return 0.0
    
    def _calculate_circadian_penalty(
        self,
        learning_profile: Dict,
        test_timestamp: datetime  # FIX #5: Use actual test time
    ) -> float:
        """
        Enhancement #14: Circadian Alignment (FIX #5: Use entry_timestamp)
        
        Studying at low-energy time = small penalty.
        """
        # Get hour from test timestamp (FIX #5)
        test_hour = test_timestamp.hour
        
        # Determine time of day
        if 6 <= test_hour < 12:
            time_period = "morning"
        elif 12 <= test_hour < 18:
            time_period = "afternoon"
        elif 18 <= test_hour < 22:
            time_period = "evening"
        else:
            time_period = "night"
        
        energy_peaks = learning_profile.get('energy_peak_hours', {})
        current_energy = energy_peaks.get(time_period, 0.7)
        
        # Guard
        current_energy = max(0.0, min(1.0, current_energy))
        
        # Low energy = small penalty
        if current_energy < 0.5:
            return 0.05
        else:
            return 0.0
    
    # ============================================
    # BEHAVIOR MODES
    # ============================================
    
    def _determine_behavior_mode(
        self,
        segment: StudentSegment,
        tests: List[TestData],
        volatility: float,
        trend: TrendDirection,
        outliers_count: int,
        avg_success: float
    ) -> BehaviorMode:
        """
        Enhancement #6: Bidirectional Sentinel (FIX #2: 3-test average for HIGH_RISK)
        
        Detects both positive and negative anomalies.
        """
        # FIX #2: Check for negative net score (3-test average)
        if len(tests) >= HIGH_RISK_TEST_COUNT:
            recent_net_scores = [t.net_score for t in tests[-HIGH_RISK_TEST_COUNT:]]
            avg_recent_net = safe_mean(recent_net_scores)
            
            if avg_recent_net < NEGATIVE_NET_THRESHOLD:
                return BehaviorMode.HIGH_RISK
        
        # Anomalous decay (Elite collapse)
        if segment == StudentSegment.ELITE and len(tests) >= 3:
            recent_avg = safe_mean([t.success_rate for t in tests[-3:]])
            if recent_avg < 60:
                return BehaviorMode.ANOMALOUS_DECAY
        
        # Positive breakthrough (Struggling improvement)
        if segment == StudentSegment.STRUGGLING and len(tests) >= 6:
            recent_avg = safe_mean([t.success_rate for t in tests[-3:]])
            historical_avg = safe_mean([t.success_rate for t in tests[:-3]])
            delta = recent_avg - historical_avg
            
            if delta > 20:
                return BehaviorMode.POSITIVE_BREAKTHROUGH
        
        # High precision (Elite + stable)
        if segment == StudentSegment.ELITE and volatility < 5 and len(tests) >= 10:
            return BehaviorMode.HIGH_PRECISION
        
        # At-risk (3 consecutive high blank rate)
        if len(tests) >= 3:
            recent_blanks = [t.blank_rate for t in tests[-3:]]
            if all(b > 50 for b in recent_blanks):
                return BehaviorMode.AT_RISK
        
        # Plateau (stuck in range)
        if len(tests) >= 5:
            recent_rates = [t.success_rate for t in tests[-5:]]
            if all(60 <= r <= 70 for r in recent_rates):
                return BehaviorMode.PLATEAU
        
        # Erratic with outliers
        if outliers_count > 0:
            return BehaviorMode.ERRATIC_WITH_ANOMALY
        
        return BehaviorMode.NORMAL
    
    # ============================================
    # FINAL CALCULATION
    # ============================================
    
    def _calculate_final_difficulty(
        self,
        factors: DifficultyFactors,
        segment: StudentSegment
    ) -> float:
        """
        Combine all factors into final difficulty score.
        
        FIX #3: Prerequisite uses ceiling, not multiplication.
        FIX #6: Confidence doesn't reduce difficulty.
        """
        # Start with base
        difficulty = factors.base_difficulty
        
        # Add volatility contribution
        difficulty += factors.volatility * 0.10
        
        # Add BS-Model decay risk
        difficulty += factors.bs_model_decay_risk * 100
        
        # Apply course context multiplier
        difficulty *= factors.course_context_multiplier
        
        # Add speed penalty
        difficulty += factors.speed_penalty * 100
        
        # Add time decay bonus
        difficulty += factors.time_decay_bonus * 100
        
        # Add metacognition adjustment
        if factors.trust_weighted_adjustment < 0.7:
            difficulty *= factors.trust_weighted_adjustment
        
        # Apply digital exhaust factor
        difficulty *= factors.digital_exhaust_factor
        
        # Add recovery bonus
        difficulty += factors.recovery_velocity_bonus * 100
        
        # Apply exam system multiplier
        difficulty *= factors.exam_system_multiplier
        
        # Add circadian penalty
        difficulty += factors.circadian_penalty * 100
        
        # FIX #3: Apply prerequisite CEILING (not multiplication)
        if factors.prerequisite_ceiling is not None:
            difficulty = min(difficulty, factors.prerequisite_ceiling)
        
        # Bounds
        difficulty = min(100.0, max(0.0, difficulty))
        
        return round(difficulty, 2)
    
    def _difficulty_to_level(self, difficulty: float) -> int:
        """Convert percentage to 1-5 level"""
        if difficulty >= 80:
            return 5  # Very difficult
        elif difficulty >= 60:
            return 4  # Difficult
        elif difficulty >= 40:
            return 3  # Moderate
        elif difficulty >= 20:
            return 2  # Easy
        else:
            return 1  # Very easy
    
    # ============================================
    # WARNINGS & MESSAGES
    # ============================================
    
    def _collect_warnings(
        self,
        factors: DifficultyFactors,
        confidence_level: str
    ) -> List[str]:
        """
        FIX #6: Collect all warnings explicitly
        """
        warnings = []
        
        if factors.confidence_warning:
            warnings.append(factors.confidence_warning)
        
        if factors.speed_warning:
            warnings.append(factors.speed_warning)
        
        if factors.prerequisite_ceiling and factors.prerequisite_ceiling < 70:
            warnings.append("⚠️ Prerequisites missing - topic difficulty capped")
        
        if factors.circadian_penalty > 0:
            warnings.append("ℹ️ Tested at low-energy time - consider optimal study hours")
        
        return warnings
    
    def _generate_messages(
        self,
        segment: StudentSegment,
        behavior_mode: BehaviorMode,
        trend: TrendDirection,
        difficulty: float,
        factors: DifficultyFactors,
        metacog: Optional[MetacognitionAnalysis],
        warnings: List[str]
    ) -> Tuple[str, str, List[str]]:
        """
        Generate student message, coach message, and recommendations.
        """
        # Student message
        if behavior_mode == BehaviorMode.POSITIVE_BREAKTHROUGH:
            student_msg = "🎉 Excellent! Significant progress detected!"
        elif behavior_mode == BehaviorMode.ANOMALOUS_DECAY:
            student_msg = "🚨 Unexpected drop detected. Conceptual review needed."
        elif behavior_mode == BehaviorMode.HIGH_RISK:
            student_msg = "⚠️ High risk - Misconceptions detected (avg net < 0 in last 3 tests)."
        elif behavior_mode == BehaviorMode.AT_RISK:
            student_msg = "⚠️ High blank rate - Review prerequisites."
        elif behavior_mode == BehaviorMode.PLATEAU:
            student_msg = "📊 Plateau detected - Try different methods."
        elif difficulty >= 70:
            student_msg = f"Challenging topic ({difficulty:.0f}%). Focus on fundamentals."
        elif difficulty <= 30:
            student_msg = f"Doing well ({100-difficulty:.0f}% mastery). Maintain consistency."
        else:
            student_msg = f"Moderate difficulty ({difficulty:.0f}%). Continue practicing."
        
        # Coach message
        coach_msg = f"Segment: {segment.value} | Mode: {behavior_mode.value} | Trend: {trend.value}"
        
        # Recommendations
        recs = []
        
        if factors.prerequisite_ceiling and factors.prerequisite_ceiling < 80:
            recs.append("Complete prerequisites first")
        
        if factors.speed_penalty > 0.05:
            recs.append("Practice speed - too slow for elite level")
        
        if factors.bs_model_decay_risk > 0.05:
            recs.append("Review soon - forgetting curve active")
        
        if metacog and metacog.recommendation:
            recs.append(metacog.recommendation)
        
        if behavior_mode == BehaviorMode.POSITIVE_BREAKTHROUGH:
            recs.append("Maintain momentum, apply to other topics")
        
        return student_msg, coach_msg, recs
    
    # ============================================
    # HELPERS
    # ============================================
    
    def _create_insufficient_data_result(self, discarded_count: int) -> DifficultyResult:
        """Return result when insufficient data"""
        return DifficultyResult(
            difficulty_percentage=50.0,
            difficulty_level=3,
            student_segment=StudentSegment.STANDARD,
            behavior_mode=BehaviorMode.NORMAL,
            trend=TrendDirection.STABLE,
            factors=DifficultyFactors(
                base_difficulty=50.0,
                blank_weight=0.55,
                wrong_weight=0.30,
                volatility=0.0,
                daily_discarded_tests_count=discarded_count
            ),
            student_message="Insufficient test data. Complete 3+ tests for accurate analysis.",
            coach_message="Needs more data for difficulty calculation.",
            recommendations=["Complete at least 3 tests", "Space tests over 7+ days"],
            confidence_level="low",
            warnings=["⚠️ Insufficient data - need minimum 3 tests"]
        )
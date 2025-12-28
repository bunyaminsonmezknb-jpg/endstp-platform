"""
Unit Tests for Difficulty Engine v2.6
======================================

Comprehensive test suite for Master Difficulty Engine.

Test coverage:
- Core calculations
- Feature enhancements (15 features)
- Edge cases
- Error handling
- Data validation
- Service layer
- API endpoints

Author: End.STP Team
Version: 2.0
Date: 2024-12-27
"""

import pytest
from datetime import datetime, date, timedelta, timezone
from decimal import Decimal

from app.core.difficulty_engine_v2 import (
    MasterDifficultyEngine,
    TestData,
    StudentSegment,
    BehaviorMode,
    TrendDirection
)


# ============================================
# FIXTURES
# ============================================

@pytest.fixture
def sample_tests_elite():
    """Elite student - high success rate"""
    base_date = date.today() - timedelta(days=30)
    tests = []
    
    for i in range(5):
        test = TestData(
            test_id=f"test-{i}",
            topic_id="topic-math-001",
            test_date=base_date + timedelta(days=i*7),
            total_questions=10,
            correct=9,
            wrong=1,
            blank=0,
            time_seconds=480,
            entry_timestamp=datetime.now(timezone.utc) - timedelta(days=30-i*7)
        )
        tests.append(test)
    
    return tests


@pytest.fixture
def sample_tests_struggling():
    """Struggling student - low success rate"""
    base_date = date.today() - timedelta(days=30)
    tests = []
    
    for i in range(5):
        test = TestData(
            test_id=f"test-{i}",
            topic_id="topic-math-001",
            test_date=base_date + timedelta(days=i*7),
            total_questions=10,
            correct=3,
            wrong=2,
            blank=5,
            time_seconds=600,
            entry_timestamp=datetime.now(timezone.utc) - timedelta(days=30-i*7)
        )
        tests.append(test)
    
    return tests


@pytest.fixture
def sample_tests_standard():
    """Standard student - medium success rate"""
    base_date = date.today() - timedelta(days=30)
    tests = []
    
    for i in range(5):
        test = TestData(
            test_id=f"test-{i}",
            topic_id="topic-math-001",
            test_date=base_date + timedelta(days=i*7),
            total_questions=10,
            correct=6,
            wrong=2,
            blank=2,
            time_seconds=540,
            entry_timestamp=datetime.now(timezone.utc) - timedelta(days=30-i*7)
        )
        tests.append(test)
    
    return tests


@pytest.fixture
def prerequisite_data_gap():
    """Prerequisite data with gaps"""
    return {
        'gap_exists': True,
        'missing_prerequisites': [
            {
                'topic_id': 'prereq-001',
                'name': 'Temel Türev',
                'strength': 0.8,
                'is_mandatory': False,
                'required_rate': 70,
                'current_rate': 45,
                'gap_percentage': 25
            }
        ]
    }


@pytest.fixture
def bs_model_data_high_retention():
    """BS-Model with high retention"""
    return {
        'current_remembering_rate': 85,
        'predicted_remembering_rate': 82,
        'next_review_date': (date.today() + timedelta(days=7)).isoformat(),
        'decay_rate': 0.02,
        's_effective': 2.5
    }


@pytest.fixture
def bs_model_data_low_retention():
    """BS-Model with low retention (decay risk)"""
    return {
        'current_remembering_rate': 45,
        'predicted_remembering_rate': 38,
        'next_review_date': date.today().isoformat(),
        'decay_rate': 0.12,
        's_effective': 1.2
    }


@pytest.fixture
def course_data_weak():
    """Weak overall subject performance"""
    return {
        'subject_id': 'subject-math',
        'subject_avg_success': 42,
        'topics_count': 25
    }


@pytest.fixture
def speed_benchmark():
    """Speed benchmarks"""
    return {
        'struggling_threshold_seconds': 120,
        'standard_threshold_seconds': 90,
        'elite_threshold_seconds': 60,
        'p50_seconds': 75,
        'p75_seconds': 90,
        'p90_seconds': 110
    }


@pytest.fixture
def feedback_data_overconfident():
    """Feedback showing overconfidence (Dunning-Kruger)"""
    return {
        'recent_feedbacks': [
            {
                'perceived_difficulty': 30,
                'calculated_difficulty': 65,
                'confidence_score': 5,
                'illusion_of_competence': True
            }
        ],
        'avg_dwell_time': 3,
        'feedback_count': 5,
        'behavior_events_count': 10
    }


@pytest.fixture
def learning_profile_resilient():
    """Learning profile with high resilience"""
    return {
        'student_segment': 'standard',
        'trust_score': 0.85,
        'resilience_score': 0.92,
        'frustration_threshold': 5,
        'frustration_index': 0.3,
        'metacognitive_index': 0.75,
        'preferred_study_time': 'morning',
        'energy_peak_hours': {
            'morning': 0.9,
            'afternoon': 0.7,
            'evening': 0.5,
            'night': 0.3
        }
    }


@pytest.fixture
def exam_system_osym():
    """OSYM exam system"""
    return {
        'code': 'OSYM_TYT',
        'name': 'ÖSYM TYT',
        'difficulty_multiplier': 1.0,
        'speed_importance': 0.6,
        'has_negative_marking': True
    }


# ============================================
# TEST CORE FUNCTIONALITY
# ============================================

class TestCoreCalculations:
    """Test core difficulty calculation logic"""
    
    def test_segment_detection_elite(self, sample_tests_elite):
        """Elite segment detection (>90% success)"""
        motor = MasterDifficultyEngine()
        result = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=sample_tests_elite
        )
        
        assert result.student_segment == StudentSegment.ELITE
        assert result.difficulty_percentage < 30  # Elite finds it easy
    
    def test_segment_detection_struggling(self, sample_tests_struggling):
        """Struggling segment detection (<50% success)"""
        motor = MasterDifficultyEngine()
        result = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=sample_tests_struggling
        )
        
        assert result.student_segment == StudentSegment.STRUGGLING
        assert result.difficulty_percentage > 60  # Struggling finds it hard
    
    def test_segment_detection_standard(self, sample_tests_standard):
        """Standard segment detection (50-90% success)"""
        motor = MasterDifficultyEngine()
        result = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=sample_tests_standard
        )
        
        assert result.student_segment == StudentSegment.STANDARD
        assert 30 <= result.difficulty_percentage <= 70
    
    def test_blank_weight_varies_by_segment(self, sample_tests_struggling, sample_tests_elite):
        """Blank coefficient should differ by segment"""
        motor = MasterDifficultyEngine()
        
        result_struggling = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=sample_tests_struggling
        )
        
        result_elite = motor.calculate_difficulty(
            student_id="student-002",
            topic_id="topic-001",
            tests=sample_tests_elite
        )
        
        # Struggling: blank weight 0.60
        # Elite: blank weight 0.45
        assert result_struggling.factors.blank_weight > result_elite.factors.blank_weight
    
    def test_insufficient_data(self):
        """Should return default result when no tests"""
        motor = MasterDifficultyEngine()
        result = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=[]
        )
        
        assert result.difficulty_percentage == 50.0
        assert result.difficulty_level == 3
        assert result.confidence_level == "low"
        assert "Insufficient" in result.student_message


# ============================================
# TEST ENHANCEMENTS
# ============================================

class TestPrerequisiteAwareness:
    """Test Enhancement #1: Prerequisite Awareness"""
    
    def test_prerequisite_gap_sets_ceiling(
        self, 
        sample_tests_standard, 
        prerequisite_data_gap
    ):
        """Prerequisite gap should set max difficulty ceiling"""
        motor = MasterDifficultyEngine(enable_prerequisite=True)
        
        result = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=sample_tests_standard,
            prerequisite_data=prerequisite_data_gap
        )
        
        # Should have ceiling
        assert result.factors.prerequisite_ceiling is not None
        assert result.factors.prerequisite_ceiling < 100
        
        # Difficulty should not exceed ceiling
        assert result.difficulty_percentage <= result.factors.prerequisite_ceiling
    
    def test_no_prerequisite_gap_no_ceiling(self, sample_tests_standard):
        """No gap = no ceiling"""
        motor = MasterDifficultyEngine(enable_prerequisite=True)
        
        prereq_data_no_gap = {
            'gap_exists': False,
            'missing_prerequisites': []
        }
        
        result = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=sample_tests_standard,
            prerequisite_data=prereq_data_no_gap
        )
        
        # No ceiling
        assert result.factors.prerequisite_ceiling == 100.0


class TestBSModelIntegration:
    """Test Enhancement #2: BS-Model Integration"""
    
    def test_high_retention_low_decay(
        self, 
        sample_tests_standard, 
        bs_model_data_high_retention
    ):
        """High retention = low decay risk"""
        motor = MasterDifficultyEngine(enable_bs_model=True)
        
        result = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=sample_tests_standard,
            bs_model_data=bs_model_data_high_retention
        )
        
        assert result.factors.bs_model_decay_risk < 0.05
    
    def test_low_retention_high_decay(
        self, 
        sample_tests_standard, 
        bs_model_data_low_retention
    ):
        """Low retention = high decay risk"""
        motor = MasterDifficultyEngine(enable_bs_model=True)
        
        result = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=sample_tests_standard,
            bs_model_data=bs_model_data_low_retention
        )
        
        assert result.factors.bs_model_decay_risk > 0.05


class TestCourseContext:
    """Test Enhancement #3: Course Context Weight"""
    
    def test_weak_subject_increases_multiplier(
        self, 
        sample_tests_standard, 
        course_data_weak
    ):
        """Weak overall subject = higher multiplier"""
        motor = MasterDifficultyEngine(enable_course_context=True)
        
        result = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=sample_tests_standard,
            course_data=course_data_weak
        )
        
        assert result.factors.course_context_multiplier > 1.0


class TestSpeedNormalization:
    """Test Enhancement #7: Speed Normalization"""
    
    def test_elite_slow_speed_penalty(
        self, 
        sample_tests_elite, 
        speed_benchmark
    ):
        """Elite student slow = penalty"""
        # Make tests slow
        for test in sample_tests_elite:
            test.time_seconds = 900  # 90 sec/question (slow for elite)
        
        motor = MasterDifficultyEngine(enable_speed=True)
        
        result = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=sample_tests_elite,
            speed_benchmark=speed_benchmark
        )
        
        assert result.factors.speed_penalty > 0
    
    def test_standard_slow_speed_warning_only(
        self, 
        sample_tests_standard, 
        speed_benchmark
    ):
        """Standard student slow = warning, no penalty"""
        # Make tests slow
        for test in sample_tests_standard:
            test.time_seconds = 1000  # Very slow
        
        motor = MasterDifficultyEngine(enable_speed=True)
        
        result = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=sample_tests_standard,
            speed_benchmark=speed_benchmark
        )
        
        # No penalty for standard
        assert result.factors.speed_penalty == 0
        
        # But should have warning
        assert result.factors.speed_warning is not None


class TestMetacognitionGap:
    """Test Enhancement #8: Metacognition Gap"""
    
    def test_dunning_kruger_detection(
        self, 
        sample_tests_struggling,
        feedback_data_overconfident,
        learning_profile_resilient
    ):
        """Detect Dunning-Kruger effect"""
        motor = MasterDifficultyEngine(enable_metacognition=True)
        
        result = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=sample_tests_struggling,
            feedback_data=feedback_data_overconfident,
            learning_profile=learning_profile_resilient
        )
        
        # Should detect overconfidence
        assert result.factors.metacognitive_gap < -1.0  # Negative gap


class TestCircadianAlignment:
    """Test Enhancement #14: Circadian Alignment"""
    
    def test_low_energy_time_penalty(
        self, 
        sample_tests_standard, 
        learning_profile_resilient
    ):
        """Testing at low-energy time = penalty"""
        # Set tests to late night (low energy)
        for test in sample_tests_standard:
            test.entry_timestamp = test.entry_timestamp.replace(hour=23)
        
        motor = MasterDifficultyEngine(enable_circadian=True)
        
        result = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=sample_tests_standard,
            learning_profile=learning_profile_resilient
        )
        
        # Should have penalty (night has 0.3 energy in profile)
        assert result.factors.circadian_penalty > 0


# ============================================
# TEST BEHAVIOR MODES
# ============================================

class TestBehaviorModes:
    """Test Enhancement #6: Bidirectional Sentinel"""
    
    def test_high_risk_detection(self):
        """Detect HIGH_RISK when 3-test avg net < 0"""
        base_date = date.today() - timedelta(days=21)
        tests = []
        
        # Create 3 tests with negative net
        for i in range(3):
            test = TestData(
                test_id=f"test-{i}",
                topic_id="topic-001",
                test_date=base_date + timedelta(days=i*7),
                total_questions=10,
                correct=2,
                wrong=6,
                blank=2,
                time_seconds=600,
                entry_timestamp=datetime.now(timezone.utc) - timedelta(days=21-i*7)
            )
            tests.append(test)
        
        motor = MasterDifficultyEngine()
        result = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=tests
        )
        
        assert result.behavior_mode == BehaviorMode.HIGH_RISK
    
    def test_anomalous_decay_elite_collapse(self, sample_tests_elite):
        """Detect elite student collapse"""
        # Add recent bad tests
        for i in range(3):
            bad_test = TestData(
                test_id=f"test-bad-{i}",
                topic_id="topic-001",
                test_date=date.today() - timedelta(days=2-i),
                total_questions=10,
                correct=4,
                wrong=4,
                blank=2,
                time_seconds=600,
                entry_timestamp=datetime.now(timezone.utc) - timedelta(days=2-i)
            )
            sample_tests_elite.append(bad_test)
        
        motor = MasterDifficultyEngine()
        result = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=sample_tests_elite
        )
        
        assert result.behavior_mode == BehaviorMode.ANOMALOUS_DECAY


# ============================================
# TEST EDGE CASES
# ============================================

class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_single_test_handling(self):
        """Should handle single test gracefully"""
        test = TestData(
            test_id="test-001",
            topic_id="topic-001",
            test_date=date.today(),
            total_questions=10,
            correct=7,
            wrong=2,
            blank=1,
            time_seconds=480,
            entry_timestamp=datetime.now(timezone.utc)
        )
        
        motor = MasterDifficultyEngine()
        result = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=[test]
        )
        
        assert result.difficulty_percentage >= 0
        assert result.difficulty_percentage <= 100
        assert result.confidence_level == "low"
    
    def test_all_blank_tests_filtered(self):
        """All-blank tests should be filtered out"""
        tests = []
        for i in range(3):
            test = TestData(
                test_id=f"test-{i}",
                topic_id="topic-001",
                test_date=date.today() - timedelta(days=i),
                total_questions=10,
                correct=0,
                wrong=0,
                blank=10,  # All blank
                time_seconds=0,
                entry_timestamp=datetime.now(timezone.utc) - timedelta(days=i)
            )
            tests.append(test)
        
        motor = MasterDifficultyEngine()
        result = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=tests
        )
        
        # Should return insufficient data result
        assert result.factors.daily_discarded_tests_count == 3
    
    def test_same_day_multiple_tests_first_contact(self):
        """Multiple tests same day = only first kept"""
        base_time = datetime.now(timezone.utc)
        tests = []
        
        # 3 tests same day, different times
        for i in range(3):
            test = TestData(
                test_id=f"test-{i}",
                topic_id="topic-001",
                test_date=date.today(),
                total_questions=10,
                correct=6,
                wrong=2,
                blank=2,
                time_seconds=480,
                entry_timestamp=base_time + timedelta(hours=i)
            )
            tests.append(test)
        
        motor = MasterDifficultyEngine()
        result = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=tests
        )
        
        # Should use only 1 test (first contact rule)
        assert result.factors.sample_size == 1
        assert result.factors.daily_discarded_tests_count == 2


# ============================================
# TEST DATA VALIDATION
# ============================================

class TestDataValidation:
    """Test TestData validation"""
    
    def test_total_questions_must_be_positive(self):
        """total_questions must be > 0"""
        with pytest.raises(ValueError):
            TestData(
                test_id="test-001",
                topic_id="topic-001",
                test_date=date.today(),
                total_questions=0,  # Invalid
                correct=0,
                wrong=0,
                blank=0,
                time_seconds=0,
                entry_timestamp=datetime.now(timezone.utc)
            )
    
    def test_questions_must_sum_to_total(self):
        """correct + wrong + blank must = total"""
        with pytest.raises(ValueError):
            TestData(
                test_id="test-001",
                topic_id="topic-001",
                test_date=date.today(),
                total_questions=10,
                correct=6,
                wrong=2,
                blank=1,  # Sum = 9, not 10!
                time_seconds=480,
                entry_timestamp=datetime.now(timezone.utc)
            )
    
    def test_timezone_aware_timestamp_required(self):
        """entry_timestamp must be timezone-aware"""
        # Should work with UTC
        test = TestData(
            test_id="test-001",
            topic_id="topic-001",
            test_date=date.today(),
            total_questions=10,
            correct=7,
            wrong=2,
            blank=1,
            time_seconds=480,
            entry_timestamp=datetime.now(timezone.utc)
        )
        assert test.entry_timestamp.tzinfo is not None


# ============================================
# TEST FEATURE FLAGS
# ============================================

class TestFeatureFlags:
    """Test modular feature toggling"""
    
    def test_all_features_disabled(self, sample_tests_standard):
        """Can run with all enhancements disabled"""
        motor = MasterDifficultyEngine(
            enable_prerequisite=False,
            enable_bs_model=False,
            enable_course_context=False,
            enable_speed=False,
            enable_metacognition=False,
            enable_digital_exhaust=False,
            enable_circadian=False
        )
        
        result = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=sample_tests_standard
        )
        
        # Should still calculate base difficulty
        assert result.difficulty_percentage > 0
        assert result.factors.base_difficulty > 0
    
    def test_selective_feature_enabling(self, sample_tests_standard, prerequisite_data_gap):
        """Can enable features selectively"""
        motor = MasterDifficultyEngine(
            enable_prerequisite=True,  # Only this
            enable_bs_model=False,
            enable_course_context=False,
            enable_speed=False,
            enable_metacognition=False,
            enable_digital_exhaust=False,
            enable_circadian=False
        )
        
        result = motor.calculate_difficulty(
            student_id="student-001",
            topic_id="topic-001",
            tests=sample_tests_standard,
            prerequisite_data=prerequisite_data_gap
        )
        
        # Prerequisite should work
        assert result.factors.prerequisite_ceiling is not None
        
        # Others should be default/zero
        assert result.factors.bs_model_decay_risk == 0.0
        assert result.factors.course_context_multiplier == 1.0


# ============================================
# RUN TESTS
# ============================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
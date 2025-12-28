"""
BS-Model Test Suite
Test field mapping ve calculation accuracy
"""
import pytest
from datetime import date, timedelta
from app.core.bs_model import BSModel, ReviewInput

class TestBSModelFieldMapping:
    """BS-Model field mapping testleri"""
    
    def test_review_input_fields(self):
        """ReviewInput doğru field'ları kabul etmeli"""
        review = ReviewInput(
            topic_id=1,
            test_date=date.today(),
            correct_rate=0.75,
            total_questions=10,
            correct_count=7,
            wrong_count=2,
            blank_count=1
        )
        
        assert review.topic_id == 1
        assert review.test_date == date.today()
        assert review.correct_rate == 0.75
        assert review.total_questions == 10
    
    def test_calculate_next_review_basic(self):
        """BS-Model basit next review hesaplaması"""
        bs_model = BSModel()
        
        # İlk review (yeni konu)
        review = ReviewInput(
            topic_id=1,
            test_date=date.today(),
            correct_rate=0.80,
            total_questions=10,
            correct_count=8,
            wrong_count=2,
            blank_count=0
        )
        
        result = bs_model.calculate_next_review(review)
        
        # Assertions
        assert result is not None
        assert 'next_review_date' in result
        assert 'ease_factor' in result
        assert 'interval_days' in result
        assert 'repetitions' in result
        
        # Next review date gelecekte olmalı
        assert result['next_review_date'] > date.today()
        
        # Ease factor 1.3-2.5 arasında olmalı
        assert 1.3 <= result['ease_factor'] <= 2.5
        
        # İlk tekrar için interval 1-7 gün arası olmalı
        assert 1 <= result['interval_days'] <= 7
    
    def test_high_success_increases_interval(self):
        """Yüksek başarı interval'ı artırmalı"""
        bs_model = BSModel()
        
        # Yüksek başarılı review
        review_high = ReviewInput(
            topic_id=1,
            test_date=date.today(),
            correct_rate=0.95,  # %95 başarı
            total_questions=10,
            correct_count=9,
            wrong_count=1,
            blank_count=0
        )
        
        result_high = bs_model.calculate_next_review(review_high)
        
        # Düşük başarılı review
        review_low = ReviewInput(
            topic_id=2,
            test_date=date.today(),
            correct_rate=0.60,  # %60 başarı
            total_questions=10,
            correct_count=6,
            wrong_count=3,
            blank_count=1
        )
        
        result_low = bs_model.calculate_next_review(review_low)
        
        # Yüksek başarı daha uzun interval vermeli
        assert result_high['interval_days'] >= result_low['interval_days']
        assert result_high['ease_factor'] >= result_low['ease_factor']
    
    def test_field_names_compatibility(self):
        """Eski field isimleri KULLANILMAMALI"""
        with pytest.raises((TypeError, AttributeError)):
            # ❌ Eski isimler artık çalışmamalı
            ReviewInput(
                topic_code="MAT-001",  # Yanlış: topic_id olmalı
                attempt_date=date.today(),  # Yanlış: test_date olmalı
                success_rate=0.75  # Yanlış: correct_rate olmalı
            )


class TestBSModelIntegration:
    """BS-Model entegrasyon testleri"""
    
    def test_multiple_reviews_progression(self):
        """Ardışık review'lar interval'ı artırmalı"""
        bs_model = BSModel()
        
        reviews = []
        for i in range(3):
            review = ReviewInput(
                topic_id=1,
                test_date=date.today() + timedelta(days=i*7),
                correct_rate=0.85,
                total_questions=10,
                correct_count=8,
                wrong_count=2,
                blank_count=0
            )
            result = bs_model.calculate_next_review(review)
            reviews.append(result)
        
        # Her review sonrası interval artmalı
        assert reviews[1]['interval_days'] > reviews[0]['interval_days']
        assert reviews[2]['interval_days'] > reviews[1]['interval_days']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

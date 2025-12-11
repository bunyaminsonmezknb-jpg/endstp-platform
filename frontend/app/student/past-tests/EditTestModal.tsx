'use client';

import { useState } from 'react';

interface EditTestModalProps {
  test: {
    id: string;
    test_date: string;
    correct_count: number;
    wrong_count: number;
    empty_count: number;
    topic?: {
      name_tr: string;
    };
    subject?: {
      name_tr: string;
    };
  };
  onClose: () => void;
  onSave: (updatedData: any) => Promise<void>; // ✅ PARAMETRE ALIYOR
}

export default function EditTestModal({ test, onClose, onSave }: EditTestModalProps) {
  const [formData, setFormData] = useState({
    test_date: test.test_date.split('T')[0],
    correct_count: test.correct_count,
    wrong_count: test.wrong_count,
    empty_count: test.empty_count
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const calculateMetrics = () => {
    const { correct_count, wrong_count, empty_count } = formData;
    const total = correct_count + wrong_count + empty_count;
    const net = correct_count - (wrong_count * 0.25);
    const successRate = total > 0 ? (correct_count / total) * 100 : 0;
    
    return { net, successRate, total };
  };

  // ✅ TOPLAM SORU KONTROLÜ
  const isValidTotal = () => {
    const { total } = calculateMetrics();
    return total === 12;
  };

  const metrics = calculateMetrics();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      // ✅ TOPLAM SORU KONTROLÜ
      if (!isValidTotal()) {
        throw new Error('Toplam soru sayısı tam olarak 12 olmalıdır!');
      }

      const { net, successRate } = calculateMetrics();

      // Backend'e gönderilecek veri
      const updatedTest = {
        id: test.id,
        test_date: formData.test_date,
        correct_count: formData.correct_count,
        wrong_count: formData.wrong_count,
        empty_count: formData.empty_count,
        net_score: net,
        success_rate: successRate
      };

      // Parent component'e gönder (backend isteği orada yapılacak)
      await onSave(updatedTest);
      
      onClose(); // Başarılı olursa kapat
    } catch (err: any) {
      console.error('Güncelleme hatası:', err);
      setError(err.message || 'Kaydedilirken hata oluştu');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (field: string, value: number | string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-t-2xl">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold">✏️ Test Düzenle</h2>
              <p className="text-sm opacity-90 mt-1">
                {test.subject?.name_tr} - {test.topic?.name_tr}
              </p>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:bg-white/20 w-10 h-10 rounded-full transition-colors"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {error && (
            <div className="bg-red-50 border-2 border-red-200 rounded-xl p-4">
              <div className="flex items-center gap-2 text-red-600">
                <span className="text-xl">⚠️</span>
                <div className="text-sm font-semibold">{error}</div>
              </div>
            </div>
          )}

          {/* Test Tarihi */}
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-2">
              📅 Test Tarihi ve Saati
            </label>
            <input
              type="datetime-local"
              value={formData.test_date.includes('T') ? formData.test_date.slice(0, 16) : `${formData.test_date}T12:00`}
              onChange={(e) => handleChange('test_date', e.target.value)}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition-all"
              required
            />
          </div>

          {/* Soru Sayıları */}
          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-bold text-green-700 mb-2">✓ Doğru</label>
              <input
                type="number"
                min="0"
                value={formData.correct_count}
                onChange={(e) => handleChange('correct_count', parseInt(e.target.value) || 0)}
                className="w-full px-4 py-3 border-2 border-green-300 rounded-xl focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all text-center text-lg font-bold"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-bold text-red-700 mb-2">✗ Yanlış</label>
              <input
                type="number"
                min="0"
                value={formData.wrong_count}
                onChange={(e) => handleChange('wrong_count', parseInt(e.target.value) || 0)}
                className="w-full px-4 py-3 border-2 border-red-300 rounded-xl focus:border-red-500 focus:ring-2 focus:ring-red-200 transition-all text-center text-lg font-bold"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-700 mb-2">○ Boş</label>
              <input
                type="number"
                min="0"
                value={formData.empty_count}
                onChange={(e) => handleChange('empty_count', parseInt(e.target.value) || 0)}
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-gray-500 focus:ring-2 focus:ring-gray-200 transition-all text-center text-lg font-bold"
                required
              />
            </div>
          </div>

          {/* Hesaplanan Değerler */}
          <div className={`rounded-xl p-6 border-2 ${
            isValidTotal() 
              ? 'bg-gradient-to-br from-purple-50 to-blue-50 border-purple-200' 
              : 'bg-gradient-to-br from-red-50 to-orange-50 border-red-300'
          }`}>
            <h3 className="text-lg font-bold text-gray-800 mb-4">
              📊 Hesaplanan Değerler
              {!isValidTotal() && (
                <span className="ml-3 text-sm bg-red-500 text-white px-3 py-1 rounded-full animate-pulse">
                  ⚠️ Toplam 12 soru olmalı!
                </span>
              )}
            </h3>
            <div className="grid grid-cols-3 gap-4">
              <div className="text-center">
                <div className="text-sm text-gray-600 mb-1">Toplam Soru</div>
                <div className={`text-3xl font-bold ${
                  metrics.total === 12 ? 'text-green-600' : 
                  metrics.total < 12 ? 'text-orange-600' : 
                  'text-red-600'
                }`}>
                  {metrics.total} / 12
                </div>
              </div>
              <div className="text-center">
                <div className="text-sm text-gray-600 mb-1">Net</div>
                <div className="text-3xl font-bold text-purple-600">
                  {metrics.net.toFixed(2)}
                </div>
              </div>
              <div className="text-center">
                <div className="text-sm text-gray-600 mb-1">Başarı Oranı</div>
                <div className={`text-3xl font-bold ${
                  metrics.successRate >= 80 ? 'text-green-600' :
                  metrics.successRate >= 60 ? 'text-yellow-600' :
                  'text-red-600'
                }`}>
                  %{metrics.successRate.toFixed(0)}
                </div>
              </div>
            </div>
          </div>

          {/* Buttons */}
          <div className="flex gap-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-700 px-6 py-3 rounded-xl font-bold transition-colors"
              disabled={isSubmitting}
            >
              İptal
            </button>
            <button
              type="submit"
              disabled={isSubmitting || !isValidTotal()}
              className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-6 py-3 rounded-xl font-bold transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? '⏳ Kaydediliyor...' : 
               !isValidTotal() ? '❌ Toplam 12 soru olmalı' : 
               '💾 Kaydet'}
            </button>
          </div>

          {/* Uyarı */}
          <div className="bg-yellow-50 border-2 border-yellow-200 rounded-xl p-4">
            <div className="flex items-start gap-2 text-yellow-800 text-sm">
              <span className="text-xl">⚠️</span>
              <div>
                <div className="font-bold mb-1">Dikkat!</div>
                <div>
                  Test verilerini değiştirdiğinizde, 4 motor analizi yeniden hesaplanacaktır.
                  Bu işlem geri alınamaz!
                </div>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
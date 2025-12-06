'use client';

import { useState } from 'react';

export default function FeedbackWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [satisfaction, setSatisfaction] = useState<number | null>(null);
  const [issues, setIssues] = useState<string[]>([]);
  const [message, setMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showThankYou, setShowThankYou] = useState(false);

  const issueOptions = [
    { id: 'slow_page', label: '🐌 Sayfa yavaş yüklendi' },
    { id: 'error', label: '❌ Hata mesajı aldım' },
    { id: 'confusing', label: '❓ Anlamadığım bir şey var' },
    { id: 'data_issue', label: '📊 Verilerim yanlış görünüyor' },
    { id: 'mobile_issue', label: '📱 Mobil sorunu' },
  ];

  const handleIssueToggle = (issueId: string) => {
    setIssues(prev =>
      prev.includes(issueId)
        ? prev.filter(i => i !== issueId)
        : [...prev, issueId]
    );
  };

  const handleSubmit = async () => {
    if (!satisfaction && issues.length === 0 && !message) {
      alert('Lütfen en az bir seçenek işaretleyin veya mesaj yazın');
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await fetch('http://localhost:8000/api/v1/support-feedback/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          page_url: window.location.pathname,
          satisfaction_score: satisfaction,
          issue_categories: issues,
          message: message,
          browser_info: {
            userAgent: navigator.userAgent,
            screenSize: `${window.innerWidth}x${window.innerHeight}`,
          },
        }),
      });

      const data = await response.json();

      if (data.success) {
        setShowThankYou(true);
        setTimeout(() => {
          setIsOpen(false);
          setShowThankYou(false);
          setSatisfaction(null);
          setIssues([]);
          setMessage('');
        }, 2000);
      }
    } catch (error) {
      console.error('Feedback error:', error);
      alert('Bir hata oluştu. Lütfen tekrar deneyin.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      {/* Floating Button */}
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 bg-purple-600 text-white p-4 rounded-full shadow-lg hover:bg-purple-700 hover:scale-110 transition-all z-40"
        title="Geri Bildirim Gönder"
      >
        <span className="text-2xl">💬</span>
      </button>

      {/* Modal */}
      {isOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl p-6 max-w-md w-full max-h-[90vh] overflow-y-auto">
            {showThankYou ? (
              <div className="text-center py-8">
                <span className="text-6xl">🙏</span>
                <h3 className="text-2xl font-bold text-gray-800 mt-4">Teşekkürler!</h3>
                <p className="text-gray-600 mt-2">Geri bildiriminiz alındı</p>
              </div>
            ) : (
              <>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold text-gray-800">💬 Geri Bildirim</h3>
                  <button
                    onClick={() => setIsOpen(false)}
                    className="text-gray-400 hover:text-gray-600 text-2xl"
                  >
                    ×
                  </button>
                </div>

                <div className="mb-6">
                  <p className="text-sm font-medium text-gray-700 mb-3">
                    Bu sayfayı nasıl buldunuz?
                  </p>
                  <div className="flex gap-2 justify-center">
                    {[
                      { score: 1, emoji: '😞', label: 'Kötü' },
                      { score: 2, emoji: '😕', label: 'Vasat' },
                      { score: 3, emoji: '😐', label: 'İyi' },
                      { score: 4, emoji: '😊', label: 'Harika' },
                      { score: 5, emoji: '🤩', label: 'Mükemmel' },
                    ].map(({ score, emoji, label }) => (
                      <button
                        key={score}
                        onClick={() => setSatisfaction(score)}
                        className={`flex flex-col items-center p-2 rounded-lg transition-all ${
                          satisfaction === score
                            ? 'bg-purple-100 ring-2 ring-purple-600'
                            : 'bg-gray-100 hover:bg-gray-200'
                        }`}
                      >
                        <span className="text-2xl">{emoji}</span>
                        <span className="text-xs text-gray-600 mt-1">{label}</span>
                      </button>
                    ))}
                  </div>
                </div>

                <div className="mb-6">
                  <p className="text-sm font-medium text-gray-700 mb-3">
                    Bir sorun mu yaşadınız?
                  </p>
                  <div className="space-y-2">
                    {issueOptions.map(option => (
                      <label
                        key={option.id}
                        className="flex items-center gap-2 p-2 rounded-lg hover:bg-gray-50 cursor-pointer"
                      >
                        <input
                          type="checkbox"
                          checked={issues.includes(option.id)}
                          onChange={() => handleIssueToggle(option.id)}
                          className="w-4 h-4 text-purple-600 rounded"
                        />
                        <span className="text-sm text-gray-700">{option.label}</span>
                      </label>
                    ))}
                  </div>
                </div>

                <div className="mb-6">
                  <p className="text-sm font-medium text-gray-700 mb-2">
                    Detaylı açıklama (opsiyonel)
                  </p>
                  <textarea
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Bize daha fazla bilgi verin..."
                    className="w-full border border-gray-300 rounded-lg p-3 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-purple-500"
                    rows={4}
                    maxLength={500}
                  />
                  <p className="text-xs text-gray-500 mt-1">{message.length}/500</p>
                </div>

                <button
                  onClick={handleSubmit}
                  disabled={isSubmitting}
                  className="w-full bg-purple-600 text-white py-3 rounded-lg font-semibold hover:bg-purple-700 transition disabled:opacity-50"
                >
                  {isSubmitting ? 'Gönderiliyor...' : 'Gönder'}
                </button>
              </>
            )}
          </div>
        </div>
      )}
    </>
  );
}

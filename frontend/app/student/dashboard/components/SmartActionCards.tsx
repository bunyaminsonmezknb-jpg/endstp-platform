'use client';

interface ActionCard {
  id: string;
  icon: string;
  title: string;
  subtitle: string;
  urgency: 'critical' | 'high' | 'medium' | 'low';
  action: string;
  source: string; // Hangi motordan geldiği
}

interface SmartActionCardsProps {
  actions?: ActionCard[];
}

// DEMO DATA - 4 motordan gelecek
const DEMO_ACTIONS: ActionCard[] = [
  {
    id: '1',
    icon: '🆘',
    title: 'ACİL TEKRAR',
    subtitle: 'Türev (2 gün kaldı)',
    urgency: 'critical',
    action: 'Hemen Başla',
    source: 'Akıllı Tekrar Planlayıcı'
  },
  {
    id: '2',
    icon: '⚡',
    title: 'BU HAFTA ÇALIŞ',
    subtitle: 'İntegral (Öncelik: Yüksek)',
    urgency: 'high',
    action: 'Plan Yap',
    source: 'Öncelik Motoru'
  },
  {
    id: '3',
    icon: '🐢',
    title: 'HIZ SORUNU',
    subtitle: 'Limit (Tempo: 1.8x yavaş)',
    urgency: 'medium',
    action: 'Pratik Yap',
    source: 'Hız Analizi'
  },
  {
    id: '4',
    icon: '📊',
    title: 'ZORLUK VAR',
    subtitle: 'Fizik (%75 zorluk)',
    urgency: 'medium',
    action: 'Tekrar Et',
    source: 'Zorluk Motoru'
  }
];

export default function SmartActionCards({ actions = DEMO_ACTIONS }: SmartActionCardsProps) {
  const getUrgencyColor = (urgency: string) => {
    switch (urgency) {
      case 'critical': return 'from-red-500 to-red-600';
      case 'high': return 'from-orange-500 to-orange-600';
      case 'medium': return 'from-yellow-500 to-yellow-600';
      case 'low': return 'from-green-500 to-green-600';
      default: return 'from-gray-500 to-gray-600';
    }
  };

  const getUrgencyBorder = (urgency: string) => {
    switch (urgency) {
      case 'critical': return 'border-red-300';
      case 'high': return 'border-orange-300';
      case 'medium': return 'border-yellow-300';
      case 'low': return 'border-green-300';
      default: return 'border-gray-300';
    }
  };

  return (
    <div className="mb-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
        ⚡ Hızlı Aksiyonlar
        <span className="text-xs text-purple-600 bg-purple-100 px-2 py-1 rounded-full">
          4 Motor Önerisi
        </span>
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {actions.map((action) => (
          <div
            key={action.id}
            className={`bg-white rounded-2xl p-5 border-2 ${getUrgencyBorder(action.urgency)} shadow-lg hover:shadow-xl transition-all hover:scale-105 cursor-pointer group`}
          >
            {/* Icon ve Kaynak */}
            <div className="flex items-center justify-between mb-3">
              <div className="text-4xl">{action.icon}</div>
              <div className="text-xs text-gray-500 italic">
                {action.source}
              </div>
            </div>

            {/* Başlık */}
            <div className={`bg-gradient-to-r ${getUrgencyColor(action.urgency)} text-white px-3 py-1 rounded-lg text-xs font-bold mb-2 text-center`}>
              {action.title}
            </div>

            {/* Alt Başlık */}
            <div className="text-sm text-gray-700 font-semibold mb-3 text-center">
              {action.subtitle}
            </div>

            {/* Aksiyon Butonu */}
            <button className={`w-full bg-gradient-to-r ${getUrgencyColor(action.urgency)} text-white py-2 rounded-lg text-sm font-bold hover:shadow-lg transition-all group-hover:scale-105`}>
              {action.action} →
            </button>
          </div>
        ))}
      </div>

      {/* Alt Bilgi */}
      <div className="mt-4 text-xs text-gray-500 text-center">
        💡 Bu öneriler 4 motor tarafından gerçek zamanlı olarak belirleniyor
      </div>
    </div>
  );
}
